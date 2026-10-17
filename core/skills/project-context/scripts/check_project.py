#!/usr/bin/env python3
"""Check the project context of a repository (/project-context, fi-sdd-standard). No AI.

Usage (from the repository root):
    python <skill folder>/scripts/check_project.py [--root .]

Checks AGENTS.md (kit block, fixed headings of "Project context", stamp, size, open markers and
whether its sources changed after the context date), CLAUDE.md, the six base documents in docs/
(headings and sections still empty), that a .NET solution has a test project, and the drafts in
docs/sdd/_borradores/ waiting for a work item, by priority (ADR-0028). The required
headings come from the templates next to this script, so they never drift from the skill.
Exit code 0 = no errors (warnings allowed), 1 = errors.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATES = HERE.parent / "templates"
DOCS = ["architecture.md", "backend.md", "database.md", "api-reference.md", "frontend.md", "reglas-negocio.md"]
MAX_LINES, WARN_LINES = 200, 185
TEST_PACKAGES = ("xunit", "nunit", "mstest", "microsoft.net.test.sdk")
SKIP = {"node_modules", "bin", "obj", ".git", "dist", "build", ".agents", ".claude"}  # .agents/.claude: kit templates
PRIORITIES = ("Urgente", "Alta", "Media", "Baja")


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, mark: str, what: str, detail: str = "") -> None:
        self.rows.append((mark, what, detail))

    def count(self, mark: str) -> int:
        return sum(1 for m, _, _ in self.rows if m == mark)


def headings(path: Path) -> list[str]:
    return re.findall(r"^## +(.+?)\s*$", path.read_text(encoding="utf-8"), re.M)


def read(path: Path) -> str:
    return path.read_bytes().decode("utf-8-sig", errors="replace")


def empty_sections(text: str) -> list[str]:
    """Headings whose body is empty or only HTML comments / template placeholders."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    empty = []
    for i in range(1, len(parts) - 1, 2):
        body = re.sub(r"<!--.*?-->", "", parts[i + 1], flags=re.S).strip()
        if not body or body.startswith("[") and body.endswith("]"):
            empty.append(parts[i])
    return empty


def last_change(root: Path, path: str) -> str | None:
    try:
        out = subprocess.run(["git", "-C", str(root), "log", "-1", "--format=%cs", "--", path],
                             capture_output=True, text=True, timeout=15)
        return out.stdout.strip() or None
    except (OSError, subprocess.SubprocessError):
        return None


def check_agents(root: Path, r: Report) -> None:
    path = root / "AGENTS.md"
    if not path.exists():
        r.add("✗", "AGENTS.md", "no existe: ejecuta install.py y después /project-context")
        return
    text = read(path)
    lines = text.count("\n") + 1
    if "<!-- sdd-kit:base:start -->" not in text or "<!-- sdd-kit:base:end -->" not in text:
        r.add("✗", "AGENTS.md", "sin el bloque del kit (marcas sdd-kit:base)")
        context = text
    else:
        r.add("✓", "AGENTS.md", "bloque del kit")
        context = text.split("<!-- sdd-kit:base:end -->", 1)[1]
    found = re.findall(r"^## +(.+?)\s*$", context, re.M)
    missing = [h for h in headings(TEMPLATES / "project-context.md") if h not in found]
    if missing:
        r.add("✗", "Project context", "faltan los encabezados fijos: " + ", ".join(missing))
    else:
        r.add("✓", "Project context", f"{len(found)} secciones, con los encabezados fijos")
    budgets = dict(re.findall(r"^## +(.+?)\s*\n<!-- max (\d+) lines", read(TEMPLATES / "project-context.md"), re.M))
    parts = re.split(r"^## +(.+?)\s*$", context, flags=re.M)
    over = []
    for i in range(1, len(parts) - 1, 2):
        size = len([l for l in re.sub(r"<!--.*?-->", "", parts[i + 1], flags=re.S).strip().splitlines()])
        if parts[i] in budgets and size > int(budgets[parts[i]]):
            over.append(f"{parts[i]} ({size}/{budgets[parts[i]]})")
    if over:
        r.add("⚠", "Project context", "secciones por encima de su presupuesto: " + ", ".join(over) + " → el detalle a docs/")
    empty = [h for h in empty_sections(context) if h in headings(TEMPLATES / "project-context.md")]
    if empty:
        r.add("⚠", "Project context", "secciones sin rellenar: " + ", ".join(empty))
    if not re.search(r"\*\*Generado con:\*\* project-context v[\d.]+", context):
        r.add("⚠", "Project context", "sin el sello «Generado con: project-context» (¿escrito a mano?)")
    if lines > MAX_LINES:
        r.add("✗", "AGENTS.md", f"{lines} líneas (máximo {MAX_LINES}, ADR-0014): pasa el detalle a docs/")
    elif lines > WARN_LINES:
        r.add("⚠", "AGENTS.md", f"{lines} líneas (cerca del máximo de {MAX_LINES}): mira qué puede ir a docs/")
    else:
        r.add("✓", "AGENTS.md", f"{lines} líneas")
    open_rv = re.findall(r"\[REQUIRES-VALIDATION:\s*([^\]]+)\]", re.sub(r"<!--.*?-->", "", context, flags=re.S))
    for reason in open_rv:
        r.add("⚠", "Project context", f"[REQUIRES-VALIDATION] {reason.strip()[:110]} → /project-context check")
    m = re.search(r"<!-- sdd:context · (\d{4}-\d{2}-\d{2}) · fuentes: (.*?) -->", context)
    if not m:
        r.add("⚠", "Project context", "sin la marca sdd:context (fecha y fuentes): no se pueden detectar cambios")
        return
    date, sources = m.group(1), [s.strip().strip("`") for s in m.group(2).split(",") if s.strip()]
    changed = []
    for s in sources:
        if any(ch in s for ch in "*?[<") or not (root / s).exists():
            continue
        when = last_change(root, s)
        if when and when > date:
            changed.append(f"{s} ({when})")
    if changed:
        r.add("⚠", "Project context", f"fuentes cambiadas después del {date}: {', '.join(changed)} → /project-context")
    else:
        r.add("✓", "Project context", f"fuentes sin cambios desde el {date}")


def check_claude(root: Path, r: Report) -> None:
    path = root / "CLAUDE.md"
    if path.exists() and "@AGENTS.md" not in read(path):
        r.add("⚠", "CLAUDE.md", "no importa @AGENTS.md: pasa su contenido a AGENTS.md y deja solo «@AGENTS.md»")
    elif path.exists():
        r.add("✓", "CLAUDE.md", "importa @AGENTS.md")


def check_docs(root: Path, r: Report) -> None:
    for name in DOCS:
        path = root / "docs" / name
        if not path.exists():
            r.add("✗", f"docs/{name}", "no existe")
            continue
        text = read(path)
        if "Completar con el contexto real" in text:
            r.add("⚠", f"docs/{name}", "sigue siendo la plantilla vacía")
            continue
        missing = [h for h in headings(TEMPLATES / "docs" / name) if h not in re.findall(r"^## +(.+?)\s*$", text, re.M)]
        empty = empty_sections(text)
        if missing:
            r.add("⚠", f"docs/{name}", "faltan encabezados: " + ", ".join(missing))
        if empty:
            r.add("⚠", f"docs/{name}", "secciones sin rellenar: " + ", ".join(empty))
        if not missing and not empty:
            r.add("✓", f"docs/{name}")


def check_tests(root: Path, r: Report) -> None:
    def files(pattern: str):
        for p in root.rglob(pattern):
            if not SKIP.intersection(p.relative_to(root).parts):
                yield p
    if not any(True for _ in files("*.sln")) and not any(True for _ in files("*.slnx")):
        return
    tests = []
    for p in files("*.csproj"):
        t = read(p).lower()
        if "<istestproject>true" in t or any(f'include="{pkg}' in t for pkg in TEST_PACKAGES):
            tests.append(p.relative_to(root).as_posix())
    if tests:
        r.add("✓", "pruebas .NET", ", ".join(tests))
    else:
        r.add("✗", "pruebas .NET", "no hay proyecto de pruebas: /project-context lo crea (ADR-0021)")


def check_guardrails(root: Path, r: Report) -> None:
    """sdd-guardrails.json and architecture tests (ADR-0023)."""
    import json
    path = root / "sdd-guardrails.json"
    if not path.exists():
        r.add("⚠", "sdd-guardrails.json", "no existe: ejecuta install.py")
    else:
        try:
            cfg = json.loads(read(path))
            agents = read(root / "AGENTS.md") if (root / "AGENTS.md").exists() else ""
            section = re.search(r"^## +Protected paths\s*\n(.*?)(?=^## |\Z)", agents, re.S | re.M)
            declared = section and re.search(r"^- ", section.group(1), re.M)
            if declared and not cfg.get("protected"):
                r.add("⚠", "sdd-guardrails.json", "AGENTS.md declara rutas protegidas y «protected» está vacío")
            else:
                r.add("✓", "sdd-guardrails.json", f"{len(cfg.get('protected', []))} rutas protegidas · "
                      f"{len(cfg.get('patterns', []))} patrones")
        except ValueError:
            r.add("✗", "sdd-guardrails.json", "no es JSON válido")
    if any(True for _ in root.rglob("*.sln")) or any(True for _ in root.rglob("*.slnx")):
        arch = [p for p in root.rglob("*Architecture*Tests*.cs") if not SKIP.intersection(p.relative_to(root).parts)]
        r.add("✓" if arch else "⚠", "pruebas de arquitectura",
              ", ".join(p.relative_to(root).as_posix() for p in arch[:3]) if arch
              else "no hay: /project-context las crea desde la plantilla (ADR-0023)")


def check_drafts(root: Path, r: Report) -> None:
    """Drafts waiting for a work item, most urgent first (ADR-0027, ADR-0028)."""
    folder = root / "docs" / "sdd" / "_borradores"
    drafts = sorted(p for p in folder.glob("*.md")) if folder.is_dir() else []
    if not drafts:
        return
    by_priority: dict[str, list[str]] = {p: [] for p in PRIORITIES}
    unknown = []
    for d in drafts:
        m = re.search(r"^\*\*Prioridad:\*\*\s*\[?(\w+)", read(d), re.M)
        level = next((p for p in PRIORITIES if m and m.group(1).lower() == p.lower()), None)
        (by_priority[level] if level else unknown).append(d.name)
    summary = " · ".join(f"{len(v)} {k.lower()}" for k, v in by_priority.items() if v)
    if by_priority["Urgente"]:
        r.add("⚠", "borradores", f"{summary}. Crea ya en Azure DevOps los urgentes: "
              + ", ".join(by_priority["Urgente"]))
    else:
        r.add("⚠", "borradores", f"{summary or str(len(drafts))} pendientes de work item; no llegan a dev (ADR-0027)")
    if unknown:
        r.add("⚠", "borradores sin prioridad", ", ".join(unknown)
              + " → añade «**Prioridad:** Urgente | Alta | Media | Baja» (plantilla borrador.md)")


def main() -> int:
    ap = argparse.ArgumentParser(description="Comprueba el contexto del proyecto")
    ap.add_argument("--root", default=".", type=Path)
    root = ap.parse_args().root.resolve()
    r = Report()
    check_agents(root, r)
    check_claude(root, r)
    check_docs(root, r)
    check_tests(root, r)
    check_guardrails(root, r)
    check_drafts(root, r)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"\nContexto del proyecto: {root.name}\n")
    for mark, what, detail in r.rows:
        print(f"  {mark} {what}" + (f" — {detail}" if detail else ""))
    print(f"\n  {r.count('✗')} errores · {r.count('⚠')} avisos\n")
    return 1 if r.count("✗") else 0


if __name__ == "__main__":
    sys.exit(main())
