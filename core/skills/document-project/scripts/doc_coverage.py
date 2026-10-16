#!/usr/bin/env python3
"""Doc comment coverage of a repository, and a proposal of documentation areas
(/document-project, fi-sdd-standard). No AI.

Usage (from the repository root):
    python doc_coverage.py [--root .] [--out <file.md>] [--json <file.json>] [--areas]
                           [--build-log <build output>] [--files <file> ...]

- Without --files: coverage by folder (symbols, documented, %), production code and tests apart.
- --areas: also proposes documentation areas and blocks: one area per ASP.NET controller with the
  services injected only into it and the types only it uses; base controllers, shared services, the
  remaining backend folders and the frontend folders as their own areas. Areas over the limits are
  split without separating an entity from its EF configuration, an interface from its class or the
  parts of a partial class. Blocks group consecutive areas of the same type. Ordered by dependency
  and by the changes of the last 6 months (git).
- --check-plan <plan.md>: checks a written plan against the code: every file with something to
  document in exactly one area, no unknown files, areas and blocks within the limits. Exit code 1
  when there are errors.
- --files: detail for those files: every public symbol without a doc comment (line, kind, name).
  Used to build the doc-writer package and to compare before and after.
- --build-log: a build output with CS1591 warnings (GenerateDocumentationFile): counted per file.
- --warnings <build log> [--compare <previous report>]: the warnings of a build by code and file,
  NuGet audit warnings (NU19xx) apart; with --compare, the warnings that are new against an earlier
  report (exit code 1 if any). Counting by code and file, not by line, survives added comments.

Heuristic and line based (no compiler): good enough to plan and to measure, not a proof. Symbols:
C# public and protected types and members, and the members of interfaces; TypeScript and
JavaScript exported declarations. A symbol is documented when a `///` (C#) or a `/** */` block
(TS/JS) ends right above it, attributes and decorators aside. Generated code (Migrations,
*.Designer.cs, *.g.cs, *.d.ts, *.generated.*) and submodules are skipped.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXCLUDED = {"node_modules", "bin", "obj", ".git", "dist", "build", "_site", "TestResults", ".vs",
            "packages", "coverage", ".next", ".angular", "wwwroot", ".idea", "__pycache__",
            "Migrations", ".agents", ".claude", ".github", "docs"}
CODE = {".cs", ".ts", ".tsx", ".js", ".jsx"}
GENERATED = re.compile(r"(\.Designer\.cs|\.g\.cs|\.g\.i\.cs|AssemblyInfo\.cs|\.d\.ts|\.generated\.\w+"
                       r"|\.min\.js|setupProxy\.js|reportWebVitals\.\w+|serviceWorker\.\w+)$", re.I)
FEATURE_DIRS = {"pages", "views", "features", "modules", "screens", "routes", "containers", "app"}
AREA_MAX_FILES, AREA_MAX_UNDOC = 15, 60

CS_TYPE = re.compile(r"^\s*(?:(?:public|protected|internal|private|static|sealed|abstract|partial|readonly"
                     r"|unsafe|new|file|ref)\s+)*(class|record\s+struct|record\s+class|record|struct|interface"
                     r"|enum|delegate)\s+(?:[\w<>\[\],.?]+\s+)?(\w+)")
CS_VISIBLE = re.compile(r"^\s*(?:public|protected)\b(?!\s+private)")
CS_MEMBER = re.compile(r"^\s*(?:(?:public|protected|internal|private|static|virtual|override|abstract|sealed"
                       r"|async|new|readonly|extern|unsafe|partial|required|const|event|volatile)\s+)*"
                       r"(?:(?P<type>[\w<>\[\],.?()\s]+?)\s+)?(?P<name>\w+)\s*(?P<tail><[^>]*>\s*\(|\(|\{|=>|=|;)")
TS_EXPORT = re.compile(r"^\s*export\s+(?:default\s+)?(?:declare\s+)?(?:abstract\s+)?(?:async\s+)?"
                       r"(function\*?|class|interface|type|enum|const|let|var)\s+(\w+)")
TS_DEFAULT_FN = re.compile(r"^\s*export\s+default\s+(?:async\s+)?(function|class)\b\s*(\w*)")
STRING = re.compile(r'@"(?:[^"]|"")*"|\$?"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])\'')
ATTRS = re.compile(r'^\s*(?:\[(?:[^\]"]|"[^"]*")*\]\s*)+')
CS1591 = re.compile(r"([^\s(]+\.cs)\((\d+),\d+\)\s*:\s*warning CS1591", re.I)


def walk(root: Path, skip: set[str]):
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = sorted(d.iterdir(), key=lambda p: p.name.lower())
        except OSError:
            continue
        for p in entries:
            r = p.relative_to(root).as_posix()
            if p.is_dir():
                if p.name not in EXCLUDED and not p.is_symlink() and r not in skip:
                    stack.append(p)
            elif p.suffix.lower() in CODE and not GENERATED.search(p.name):
                yield p


def read(p: Path) -> str:
    return p.read_bytes().decode("utf-8-sig", errors="replace")


def submodules(root: Path) -> set[str]:
    gm = root / ".gitmodules"
    if not gm.exists():
        return set()
    return {m.strip().strip("/") for m in re.findall(r"^\s*path\s*=\s*(.+)$", read(gm), re.M)}


def is_test(rel: str) -> bool:
    parts = rel.split("/")
    name = parts[-1]
    return (any(re.search(r"(^|\.)(Tests?|UnitTests|IntegrationTests)$", p, re.I) for p in parts[:-1])
            or "__tests__" in parts or re.search(r"\.(test|spec)\.[jt]sx?$", name) is not None
            or re.search(r"Tests?\.cs$", name) is not None)


# ---------------------------------------------------------------- C#

def cs_symbols(text: str) -> list[dict]:
    """Public/protected symbols of a C# file: line, kind, name, documented."""
    lines = text.splitlines()
    symbols: list[dict] = []
    depth = 0
    stack: list[tuple[str, str, int]] = []  # (kind, name, body depth)
    pending: tuple[str, str] | None = None
    in_block_comment = False
    for i, raw in enumerate(lines):
        line = raw
        if in_block_comment:
            if "*/" not in line:
                continue
            line = line.split("*/", 1)[1]
            in_block_comment = False
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#") or not stripped:
            continue
        code = STRING.sub('""', line)
        code = code.split("//", 1)[0]
        if "/*" in code:
            before, after = code.split("/*", 1)
            if "*/" not in after:
                in_block_comment = True
            code = before + (after.split("*/", 1)[1] if "*/" in after else "")
        attr_only = re.fullmatch(r'\s*(?:\[(?:[^\]"]|"[^"]*")*\]\s*)+', code) is not None
        decl = ATTRS.sub("", code)
        container = stack[-1] if stack else None
        in_body = container is not None and depth == container[2]
        at_type_level = container is None or (in_body and container[0] in {"class", "record", "struct", "interface"})
        t = CS_TYPE.match(decl) if not attr_only else None
        if t and at_type_level:
            kind = t.group(1).split()[0]
            name = t.group(2)
            visible = CS_VISIBLE.match(decl) or (container is not None and container[0] == "interface")
            if visible:
                symbols.append({"line": i + 1, "kind": kind, "name": name, "doc": documented_cs(lines, i),
                                "partial": " partial " in f" {decl} "})
            if kind != "delegate":
                pending = (kind, name)
        elif in_body and container[0] != "enum" and not attr_only:
            visible = CS_VISIBLE.match(decl) or container[0] == "interface"
            m = CS_MEMBER.match(decl)
            if visible and m and m.group("name") not in {"get", "set", "init", "add", "remove", "return",
                                                           "if", "else", "new", "base", "this"}:
                tail = m.group("tail")
                name = m.group("name")
                if name == container[1] and "(" in tail:
                    kind = "ctor"
                elif "(" in tail:
                    kind = "method"
                elif tail in {"{", "=>"}:
                    kind = "property"
                else:
                    kind = "event" if re.search(r"\bevent\b", decl) else "field"
                if m.group("type") or kind == "ctor":
                    symbols.append({"line": i + 1, "kind": kind, "name": name, "doc": documented_cs(lines, i)})
        for ch in code:
            if ch == "{":
                depth += 1
                if pending:
                    stack.append((pending[0], pending[1], depth))
                    pending = None
            elif ch == "}":
                if stack and depth == stack[-1][2]:
                    stack.pop()
                depth -= 1
        if pending and code.rstrip().endswith(";"):
            pending = None  # record Foo(...); or file-scoped declaration without body
    # a partial type is documented when any of its parts is
    documented_partials = {s["name"] for s in symbols if s.get("partial") and s["doc"]}
    for s in symbols:
        if s.get("partial") and s["name"] in documented_partials:
            s["doc"] = True
        s.pop("partial", None)
    return symbols


def documented_cs(lines: list[str], i: int) -> bool:
    j = i - 1
    while j >= 0:
        s = lines[j].strip()
        if s.startswith("///"):
            return True
        if not s or s.startswith("[") or (s.endswith("]") and not s.startswith("//")) or \
                (s.startswith("//") and not s.startswith("///")):
            j -= 1  # blank lines, attributes and plain // comments do not detach a /// block
            continue
        return False
    return False


# ---------------------------------------------------------------- TS / JS

def ts_symbols(text: str) -> list[dict]:
    lines = text.splitlines()
    symbols = []
    for i, line in enumerate(lines):
        m = TS_EXPORT.match(line)
        if m:
            kind, name = m.group(1), m.group(2)
        else:
            d = TS_DEFAULT_FN.match(line)
            if not d:
                continue
            kind, name = d.group(1), d.group(2) or "default"
        symbols.append({"line": i + 1, "kind": kind.rstrip("*"), "name": name, "doc": documented_ts(lines, i)})
    return symbols


def documented_ts(lines: list[str], i: int) -> bool:
    j = i - 1
    while j >= 0 and (not lines[j].strip() or lines[j].strip().startswith("@")):
        j -= 1
    if j < 0 or not lines[j].strip().endswith("*/"):
        return False
    while j >= 0:
        if lines[j].strip().startswith("/**"):
            return True
        if lines[j].strip().startswith("/*"):
            return False
        j -= 1
    return False


# ---------------------------------------------------------------- analysis

def analyse(root: Path) -> dict[str, dict]:
    files = {}
    for p in walk(root, submodules(root)):
        rel = p.relative_to(root).as_posix()
        text = read(p)
        syms = cs_symbols(text) if p.suffix.lower() == ".cs" else ts_symbols(text)
        test = is_test(rel)
        if test:  # tests: only the classes (C#) or the whole file (TS) count
            syms = [s for s in syms if s["kind"] in {"class", "record"}] if p.suffix.lower() == ".cs" else []
        files[rel] = {"symbols": syms, "test": test, "text": text}
    return files


def cs1591(build_log: Path | None, files: dict) -> Counter:
    counts: Counter = Counter()
    if not build_log:
        return counts
    seen = set()
    for path, line in CS1591.findall(read(build_log)):
        norm = path.replace("\\", "/")
        match = next((f for f in files if norm.endswith("/" + f) or norm == f), None)
        if match and (match, line) not in seen:
            seen.add((match, line))
            counts[match] += 1
    return counts


def changes(root: Path) -> Counter:
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "--since=6.months", "--name-only", "--format="],
                             capture_output=True, text=True, timeout=60, encoding="utf-8", errors="replace")
        return Counter(l.strip() for l in out.stdout.splitlines() if l.strip())
    except (OSError, subprocess.SubprocessError):
        return Counter()


def stats(paths: list[str], files: dict) -> tuple[int, int]:
    total = sum(len(files[p]["symbols"]) for p in paths)
    doc = sum(1 for p in paths for s in files[p]["symbols"] if s["doc"])
    return total, doc


def pct(doc: int, total: int) -> str:
    return f"{100 * doc // total} %" if total else "—"


def folder_of(rel: str, depth: int = 2) -> str:
    parts = rel.split("/")[:-1]
    return "/".join(parts[:depth]) or "(raíz)"


def declared_types(text: str) -> set[str]:
    return set(re.findall(r"^[ \t]*(?:\[[^\]]*\][ \t]*)*(?:[a-z]+[ \t]+)*(?:class|record|struct|interface|enum)"
                          r"[ \t]+(\w+)", text, re.M))


INFRA_DIRS = {"Authorization", "Middlewares", "Middleware", "Startup", "Filters", "Configuration",
              "HealthChecks", "Telemetry", "DependencyInjection", "Hubs"}
BLOCK_MAX_AREAS, BLOCK_MAX_FILES = 5, 40
# order of the backend transversal areas: what the rest builds on goes first
TRANSVERSAL_RANK = [({"Controladores base", "Authorization", "Exceptions", "Middlewares", "Middleware", "Startup",
                      "Configuration", "Filters"}, 0),
                    ({"Data", "Entities", "Domain"}, 1),
                    ({"Enums", "Models", "Dtos", "DTOs", "Constants"}, 2),
                    ({"Servicios compartidos", "Services", "Utils", "Helpers", "Extensions"}, 3)]


def transversal_rank(a: dict) -> int:
    if a["type"] != "transversal":
        return 0
    last = a["name"].split("/")[-1]
    if "/" not in a["name"] and a["name"] not in {"Controladores base", "Servicios compartidos"}:
        return 0  # files at the project root (Program.cs)
    return next((r for names, r in TRANSVERSAL_RANK if last in names), 4)


def units_of(paths: list[str]) -> dict[str, list[str]]:
    """Files that are documented together: an entity and its EF configuration, IFoo and Foo,
    the parts of a partial class (Foo.cs, Foo.Query.cs)."""
    keyed: dict[str, list[str]] = defaultdict(list)
    present = {(str(Path(p).parent), Path(p).stem.split(".")[0]) for p in paths}
    for p in paths:
        folder, stem = str(Path(p).parent), Path(p).stem.split(".")[0]
        if p.endswith(".cs"):
            if Path(folder).name == "Configurations" and stem.endswith("Configuration"):
                folder, stem = str(Path(folder).parent), stem.removesuffix("Configuration")
            elif re.match(r"I[A-Z]", stem) and (folder, stem[1:]) in present:
                stem = stem[1:]
        keyed[f"{folder}/{stem}"].append(p)
    return {k: sorted(v) for k, v in keyed.items()}


def is_infra(path: str) -> bool:
    return any(part in INFRA_DIRS for part in path.split("/")[:-1])


def propose_areas(files: dict) -> list[dict]:
    cs = {f: d for f, d in files.items() if f.endswith(".cs") and not d["test"]}
    units = units_of(sorted(cs))
    unit_of = {f: k for k, fs in units.items() for f in fs}
    controllers = sorted(f for f in cs if f.endswith("Controller.cs"))
    class_name = {f: m.group(1) for f in controllers
                  if (m := re.search(r"\bclass\s+(\w+Controller)\b", cs[f]["text"]))}
    inherited = {m.group(1) for f in controllers
                 for m in re.finditer(r"\bclass\s+\w+Controller\b[^{;]*?:\s*(\w+Controller)\b", cs[f]["text"])}
    base = {f for f in controllers if re.search(r"\babstract\s+class\b", cs[f]["text"])
            or class_name.get(f) in inherited}
    implementers: dict[str, set[str]] = defaultdict(set)
    for f, d in cs.items():
        for m in re.finditer(r"\binterface\s+(I\w+)", d["text"]):
            implementers[m.group(1)].add(f)
        for m in re.finditer(r"\bclass\s+\w+[^{;]*?:\s*([^{]+)", d["text"]):
            for iface in re.findall(r"\b(I[A-Z]\w*)\b", m.group(1)):
                implementers[iface].add(f)
    injected: dict[str, set[str]] = {}
    for c in controllers:
        if c in base:
            continue
        m = re.search(rf"\b{Path(c).stem}\s*\(([^)]*)\)", cs[c]["text"], re.S)
        params = m.group(1) if m else ""
        injected[c] = {unit_of[f] for iface in re.findall(r"\b(I[A-Z]\w*)\b", params)
                       for f in implementers.get(iface, ()) if f != c and not is_infra(f)}
    usage = Counter(u for us in injected.values() for u in us)
    areas: list[dict] = []
    taken: set[str] = set()
    for c in sorted(injected):
        own = [u for u in sorted(injected[c]) if usage[u] == 1]
        fs = [c] + [f for u in own for f in units[u] if f != c]
        areas.append({"name": Path(c).stem.removesuffix("Controller"), "type": "backend", "files": fs})
        taken.update([unit_of[c]] + own)
    shared = sorted(u for u, n in usage.items() if n > 1 and u not in taken)
    taken.update(shared)
    # a type used by exactly one controller area goes with it (not infrastructure, not controllers)
    tokens = [set(re.findall(r"\b[A-Z]\w+\b", "\n".join(cs[f]["text"] for f in a["files"]))) for a in areas]
    for u, fs in sorted(units.items()):
        if u in taken or any(f in base or f.endswith("Controller.cs") or is_infra(f) for f in fs):
            continue
        names = set().union(*(declared_types(cs[f]["text"]) for f in fs))
        names |= {n.removesuffix("Attribute") for n in names if n.endswith("Attribute")}
        owners = [i for i, t in enumerate(tokens) if names & t]
        if len(owners) == 1 and names:
            areas[owners[0]]["files"] += fs
            taken.add(u)
    transversal: list[dict] = []
    if base:
        transversal.append({"name": "Controladores base", "type": "transversal", "files": sorted(base)})
        taken.update(unit_of[f] for f in base)
    if shared:
        transversal.append({"name": "Servicios compartidos", "type": "transversal",
                            "files": [f for u in shared for f in units[u]]})
    by_folder: dict[str, list[str]] = defaultdict(list)
    for u, fs in sorted(units.items()):
        if u not in taken:
            by_folder[folder_of(fs[0])] += fs
    for folder, fs in sorted(by_folder.items()):
        transversal.append({"name": folder, "type": "transversal", "files": fs})
    front: dict[str, list[str]] = defaultdict(list)
    front_t: dict[str, list[str]] = defaultdict(list)
    for f, d in files.items():
        if f.endswith(".cs") or d["test"]:
            continue
        parts = f.split("/")
        if "src" in parts:
            k = parts.index("src")
            rest = parts[k + 1:]
            prefix = "/".join(parts[:k + 1])
            if len(rest) >= 3 and rest[0] in FEATURE_DIRS:
                front[f"{prefix}/{rest[0]}/{rest[1]}"].append(f)
            elif len(rest) >= 2:
                front_t[f"{prefix}/{rest[0]}"].append(f)
            else:
                front_t[f"{prefix} (raíz)"].append(f)
        else:
            front_t[folder_of(f)].append(f)
    fe_t = [{"name": k, "type": "frontend-transversal", "files": sorted(v)} for k, v in sorted(front_t.items())]
    fe = [{"name": k, "type": "frontend", "files": sorted(v)} for k, v in sorted(front.items())]
    return transversal + areas + fe_t + fe


def split_area(a: dict, files: dict) -> list[dict]:
    """Splits an area over the limits into parts, keeping units and subfolders together."""
    undoc = lambda fs: sum(1 for f in fs for s in files[f]["symbols"] if not s["doc"])
    if len(a["files"]) <= AREA_MAX_FILES and undoc(a["files"]) <= AREA_MAX_UNDOC:
        return [a]
    head = a["files"][0] if a["type"] == "backend" else None
    units = sorted(units_of([f for f in a["files"] if f != head]).items(),
                   key=lambda kv: kv[0])  # the key carries the entity's folder, not Configurations/
    parts: list[list[str]] = [[head]] if head else []
    names: list[list[str]] = [[Path(head).stem]] if head else []
    for key, fs in units:
        cur = parts[-1] if parts else None
        if cur is None or (len(cur) + len(fs) > AREA_MAX_FILES or undoc(cur + fs) > AREA_MAX_UNDOC) and cur:
            parts.append(list(fs))
            names.append([key.rsplit("/", 1)[-1]])
        else:
            cur.extend(fs)
            names[-1].append(key.rsplit("/", 1)[-1])
    n = len(parts)
    return [{**a, "name": f"{a['name']} ({i}/{n}: {nm[0]}…{nm[-1]})" if len(nm) > 1 else f"{a['name']} ({i}/{n}: {nm[0]})",
             "files": p, "part": f"{i}/{n}"} for i, (p, nm) in enumerate(zip(parts, names), 1)]


def attach_tests(areas: list[dict], files: dict) -> list[dict]:
    stems: dict[str, dict] = {}
    for a in areas:
        for f in a["files"]:
            stems.setdefault(Path(f).stem.split(".")[0], a)
    orphan = []
    for f, d in sorted(files.items()):
        if not d["test"]:
            continue
        name = Path(f).stem.split(".")[0] if f.endswith(".cs") else Path(f).name.split(".")[0]
        subject = re.sub(r"(Tests?)$", "", name)
        a = stems.get(subject) or next((stems[s] for s in sorted(stems, key=len, reverse=True)
                                        if len(s) > 3 and subject.startswith(s)), None)
        (a.setdefault("tests", []) if a else orphan).append(f)
    if orphan:
        areas.append({"name": "Pruebas sin área", "type": "pruebas", "files": [], "tests": orphan})
    return areas


def make_blocks(areas: list[dict]) -> list[dict]:
    blocks: list[dict] = []
    for a in areas:
        if a["type"] == "pruebas" or a.get("complete"):
            continue
        cur = blocks[-1] if blocks else None
        group = (a["type"], transversal_rank(a))
        if (cur is None or cur["group"] != group or len(cur["areas"]) >= BLOCK_MAX_AREAS
                or cur["files"] + len(a["files"]) > BLOCK_MAX_FILES):
            cur = {"id": f"B-{len(blocks) + 1:02d}", "group": group, "areas": [], "files": 0, "undoc": 0}
            blocks.append(cur)
        cur["areas"].append(a["id"])
        cur["files"] += len(a["files"])
        cur["undoc"] += a["symbols"] - a["documented"]
        a["block"] = cur["id"]
    return blocks


WARN_LINE = re.compile(r"^\s*(.+?)(?:\((\d+),(\d+)\))?\s*:\s*warning\s+([A-Za-z]+\d+)\s*:", re.I)


def build_warnings(log: Path, root: Path) -> tuple[Counter, Counter]:
    """Warnings of a build log, deduplicated, counted by (code, file): code warnings and NuGet audit
    warnings (NU19xx, which depend on the advisory database, not on the code) apart."""
    seen, code, nuget = set(), Counter(), Counter()
    marker = root.name.lower() + "/"
    for line in read(log).splitlines():
        m = WARN_LINE.match(line)
        if not m:
            continue
        path = m.group(1).replace("\\", "/").strip()
        low = path.lower()
        rel = path[low.rindex(marker) + len(marker):] if marker in low else path.rsplit("/", 1)[-1]
        key = (m.group(4).upper(), rel, m.group(2), m.group(3), line.split(" [")[0][-60:])
        if key in seen:
            continue
        seen.add(key)
        (nuget if key[0].startswith("NU19") else code)[(key[0], rel)] += 1
    return code, nuget


def warnings_report(log: Path, root: Path, base: Path | None) -> tuple[list[str], int]:
    code, nuget = build_warnings(log, root)
    out = [f"# Avisos de build — {root.name}", "",
           f"**Código:** {sum(code.values())} avisos · **NuGet (NU19xx):** {sum(nuget.values())} (dependen de la "
           "base de vulnerabilidades, no del código)", "", "## Por código y archivo", "",
           "| Código | Archivo | Avisos |", "| --- | --- | --- |"]
    out += [f"| {c} | `{f}` | {n} |" for (c, f), n in sorted(code.items())]
    out += ["", "## NuGet", "", "| Código | Proyecto | Avisos |", "| --- | --- | --- |"]
    out += [f"| {c} | `{f}` | {n} |" for (c, f), n in sorted(nuget.items())]
    if not base:
        return out, 0
    old = Counter({(c, f): int(n) for c, f, n in re.findall(r"^\| (\w+) \| `([^`]+)` \| (\d+) \|$",
                                                             read(base).split("## NuGet")[0], re.M)})
    new = {k: n - old.get(k, 0) for k, n in code.items() if n > old.get(k, 0)}
    gone = sum(max(0, n - code.get(k, 0)) for k, n in old.items())
    out += ["", f"## Comparación con `{base.as_posix()}`", "",
            f"{sum(new.values())} avisos nuevos · {gone} menos"]
    out += [f"- ✗ {c} · `{f}` · +{n}" for (c, f), n in sorted(new.items())]
    return out, sum(new.values())


def check_plan(plan: Path, files: dict) -> tuple[list[str], int]:
    """Every code file with something to document is in exactly one area; areas and blocks within limits."""
    text = read(plan)
    out = [f"# Comprobación del plan — {plan.as_posix()}", ""]
    errors = warnings = 0
    sections = re.split(r"^### +(A-\w+)\b[^\n]*$", text.split("## Archivos por área", 1)[-1], flags=re.M)
    area_files: dict[str, list[str]] = {}
    for i in range(1, len(sections) - 1, 2):
        area_files[sections[i]] = re.findall(r"^- (?!prueba)`([^`]+)`", sections[i + 1], re.M)
    rows = re.findall(r"^\| *(A-\w+) *\|(.*)$", text, re.M)
    block_of = {}
    for aid, rest in rows:
        b = re.search(r"\b(B-\d+)\b", rest)
        block_of[aid] = b.group(1) if b else None
    seen: Counter = Counter(f for fs in area_files.values() for f in fs)
    prod = {f for f, d in files.items() if not d["test"]}
    missing = sorted(f for f in prod - set(seen) if any(not s["doc"] for s in files[f]["symbols"]))
    dup = sorted(f for f, n in seen.items() if n > 1)
    unknown = sorted(f for f in seen if f not in files)
    for label, items in (("Archivos con algo que documentar que no están en ningún área", missing),
                         ("Archivos en más de un área", dup), ("Archivos que no existen o no son analizables", unknown)):
        if items:
            errors += len(items)
            out += [f"✗ {label}: {len(items)}"] + [f"  - `{f}`" for f in items[:30]] + (["  - …"] if len(items) > 30 else [])
    for aid, fs in area_files.items():
        und = sum(1 for f in fs if f in files for s in files[f]["symbols"] if not s["doc"])
        if len(fs) > AREA_MAX_FILES or und > AREA_MAX_UNDOC:
            warnings += 1
            out.append(f"⚠ {aid}: {len(fs)} archivos, {und} sin documentar (límite {AREA_MAX_FILES} / {AREA_MAX_UNDOC})")
        if aid not in block_of:
            errors += 1
            out.append(f"✗ {aid}: tiene archivos pero no está en la tabla de áreas")
    blocks: dict[str, int] = defaultdict(int)
    for aid, b in block_of.items():
        if b:
            blocks[b] += len(area_files.get(aid, []))
        elif area_files.get(aid):
            warnings += 1
            out.append(f"⚠ {aid}: sin bloque")
    for b, n in sorted(blocks.items()):
        if n > BLOCK_MAX_FILES:
            warnings += 1
            out.append(f"⚠ {b}: {n} archivos (límite {BLOCK_MAX_FILES})")
    out += ["", f"{len(area_files)} áreas · {len(blocks)} bloques · {sum(seen.values())} archivos · "
            f"{errors} errores · {warnings} avisos"]
    return out, errors


def write_report(root: Path, files: dict, args) -> tuple[list[str], dict]:
    out = [f"# Cobertura de comentarios de documentación — {root.name}", "",
           "Heurística por líneas (no es el compilador): sirve para planificar y medir antes y después.", ""]
    data: dict = {"root": root.name}
    cs1591_counts = cs1591(args.build_log, files)
    if args.files:
        out += ["## Detalle por archivo", ""]
        detail = {}
        for f in args.files:
            f = f.replace("\\", "/")
            if f not in files:
                out.append(f"- `{f}`: no es código analizable (excluido o no existe)")
                continue
            syms = files[f]["symbols"]
            missing = [s for s in syms if not s["doc"]]
            out.append(f"### `{f}` — {len(syms) - len(missing)}/{len(syms)} documentados"
                       + (" · prueba" if files[f]["test"] else "")
                       + (f" · CS1591: {cs1591_counts[f]}" if args.build_log else ""))
            out += [f"- {s['line']} · {s['kind']} · {s['name']}" for s in missing] or ["- (nada pendiente)"]
            out.append("")
            detail[f] = {"total": len(syms), "documented": len(syms) - len(missing),
                         "missing": [{k: s[k] for k in ("line", "kind", "name")} for s in missing]}
        data["files"] = detail
        return out, data
    prod = [f for f in files if not files[f]["test"]]
    tests = [f for f in files if files[f]["test"]]
    t, d = stats(prod, files)
    tt, td = stats(tests, files)
    out += [f"**Código:** {len(prod)} archivos · {d}/{t} símbolos documentados ({pct(d, t)})",
            f"**Pruebas:** {len(tests)} archivos · {td}/{tt} clases con resumen ({pct(td, tt)})"]
    if args.build_log:
        out.append(f"**CS1591** (build): {sum(cs1591_counts.values())} avisos en {len(cs1591_counts)} archivos")
    out += ["", "## Por carpeta", "", "| Carpeta | Archivos | Símbolos | Documentados | % |", "| --- | --- | --- | --- | --- |"]
    groups: dict[str, list[str]] = defaultdict(list)
    for f in prod:
        groups[folder_of(f, 3)].append(f)
    for g, fs in sorted(groups.items()):
        a, b = stats(fs, files)
        out.append(f"| `{g}` | {len(fs)} | {a} | {b} | {pct(b, a)} |")
    data.update({"code": {"files": len(prod), "symbols": t, "documented": d},
                 "tests": {"files": len(tests), "classes": tt, "documented": td},
                 "cs1591": sum(cs1591_counts.values())})
    if args.areas:
        recent = changes(root)
        order = {"transversal": 0, "backend": 1, "frontend-transversal": 2, "frontend": 3}
        areas = propose_areas(files)
        for a in areas:
            a["changes"] = sum(recent.get(f, 0) for f in a["files"])
        areas.sort(key=lambda a: (order[a["type"]], transversal_rank(a),
                                  -a["changes"] if a["type"] in {"backend", "frontend"} else 0, a["name"]))
        areas = attach_tests([p for a in areas for p in split_area(a, files)], files)
        for n, a in enumerate(areas, 1):
            a["id"] = f"A-{n:02d}"
            a["symbols"], a["documented"] = stats(a["files"], files)
            a["changes"] = sum(recent.get(f, 0) for f in a["files"])
            a["complete"] = a["type"] != "pruebas" and a["symbols"] == a["documented"] and not a.get("tests")
        blocks = make_blocks(areas)
        out += ["", "## Áreas propuestas", "",
                f"Orden: transversal del backend → controladores (más cambios en 6 meses primero) → transversal "
                f"del frontend → secciones del frontend. Las áreas de más de {AREA_MAX_FILES} archivos o "
                f"{AREA_MAX_UNDOC} símbolos sin documentar ya vienen partidas, sin separar una entidad de su "
                f"configuración, una interfaz de su clase ni las partes de una clase parcial. «completa»: nada que "
                f"documentar y sin pruebas, queda fuera de los bloques.", "",
                "| ID | Área | Tipo | Archivos | Pruebas | Sin documentar | Cambios 6 m | Bloque | Nota |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
        for a in areas:
            note = "completa" if a["complete"] else ""
            out.append(f"| {a['id']} | {a['name']} | {a['type']} | {len(a['files'])} | {len(a.get('tests', []))} | "
                       f"{a['symbols'] - a['documented']}/{a['symbols']} | {a['changes']} | {a.get('block', '–')} | {note} |")
        out += ["", "## Bloques propuestos", "",
                f"Áreas consecutivas del mismo tipo y grupo (base, datos, modelos, servicios…), como máximo {BLOCK_MAX_AREAS} áreas y {BLOCK_MAX_FILES} archivos "
                f"de código.", "", "| Bloque | Áreas | Archivos | Sin documentar |", "| --- | --- | --- | --- |"]
        out += [f"| {b['id']} | {', '.join(b['areas'])} | {b['files']} | {b['undoc']} |" for b in blocks]
        out += ["", "## Archivos por área", ""]
        for a in areas:
            out.append(f"### {a['id']} · {a['name']}")
            out += [f"- `{f}`" for f in a["files"]] + [f"- prueba: `{f}`" for f in a.get("tests", [])]
            out.append("")
        data["areas"] = [{k: a.get(k) for k in ("id", "name", "type", "files", "symbols", "documented", "changes",
                                                "block", "complete")} | {"tests": a.get("tests", [])} for a in areas]
        data["blocks"] = [{k: b[k] for k in ("id", "areas", "files", "undoc")} for b in blocks]
    return out, data


def main() -> int:
    ap = argparse.ArgumentParser(description="Cobertura de comentarios de documentación y áreas")
    ap.add_argument("--root", default=".", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--json", type=Path)
    ap.add_argument("--areas", action="store_true")
    ap.add_argument("--build-log", type=Path)
    ap.add_argument("--files", nargs="+")
    ap.add_argument("--check-plan", type=Path, help="comprueba un plan.md contra el código")
    ap.add_argument("--warnings", type=Path, help="log de build: avisos por código y archivo")
    ap.add_argument("--compare", type=Path, help="con --warnings: informe anterior con el que comparar")
    args = ap.parse_args()
    root = args.root.resolve()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.warnings:
        out, new = warnings_report(args.warnings, root, args.compare)
        text = "\n".join(out) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            print(f"✓ Informe en {args.out}")
            print(out[2] + ("\n" + "\n".join(out[out.index(next(l for l in out if l.startswith("## Comparación"))) + 2:])
                            if args.compare else ""))
        else:
            print(text)
        return 1 if new else 0
    files = analyse(root)
    if args.check_plan:
        out, errors = check_plan(args.check_plan, files)
        print("\n".join(out))
        return 1 if errors else 0
    out, data = write_report(root, files, args)
    text = "\n".join(out) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
        print(f"✓ Informe en {args.out}")
        print("\n".join(l for l in out[:8] if l.startswith("**")))
    else:
        print(text)
    if args.json:
        args.json.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
