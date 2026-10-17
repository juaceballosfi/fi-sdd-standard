#!/usr/bin/env python3
"""Mandatory rules of fi-sdd-standard for a branch, before the PR (ADR-0023). No AI.

Usage (from the repository root):
    python .agents/scripts/pr-check.py [--base origin/dev]

The same checks the PR validation will run in phase 4, so that they also cover the tools without
hooks (GitHub Copilot, Codex). For every commit in base..HEAD and every file changed:

- commit messages: format of `.gitmessage`, `Ref: #<id>`, never `fix #id`, no AI trailers, size;
- encoding: changed text files in UTF-8 with the BOM of the base (check-encoding.py);
- work items: every `docs/sdd/<id>-<title>/` changed passes check-sdd-item.py;
- protected paths of `sdd-guardrails.json` not changed, and no secret file (`secrets`) added;
- files installed by the kit (`.sdd-kit.json`) changed only by install.py (a `chore(sdd)` commit);
- no draft of `docs/sdd/_borradores/` added or changed: create the work item and delete it (ADR-0027);
- AGENTS.md under 200 lines;
- added lines without high-confidence secrets (private keys, storage keys, SAS, tokens).

Exit code 0 = no errors (warnings allowed), 1 = errors, 2 = usage or git error.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENTS_MAX = 200
SECRET_PATTERNS = [
    (re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"), "clave privada"),
    (re.compile(r"AccountKey=[A-Za-z0-9+/]{30,}={0,2}"), "clave de cuenta de Azure Storage"),
    # Every pattern needs a value after the key: a bare "SharedAccessSignature=" also matched this
    # very line when the kit was installed in the same branch (Calls4Grants, v0.12.0).
    (re.compile(r"SharedAccessSignature=[^;\s\"']{20,}|[?&]sig=[A-Za-z0-9%+/]{30,}"), "firma SAS"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"), "token de GitHub"),
    (re.compile(r"\bxox[abpr]-[A-Za-z0-9-]{20,}\b"), "token de Slack"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "clave de AWS"),
    (re.compile(r"(?i)\b(?:password|pwd)\s*=\s*[^;\"'\s]{8,}\s*;"), "contraseña en una cadena de conexión"),
]


def git(*args: str) -> str:
    out = subprocess.run(["git", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"git {' '.join(args)} failed")
    return out.stdout


def load_checker():
    sys.dont_write_bytecode = True  # no __pycache__ inside .agents/scripts/ of the project
    spec = importlib.util.spec_from_file_location("check_sdd_item", HERE / "check-sdd-item.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def glob_regex(pattern: str) -> re.Pattern:
    p = pattern.replace("\\", "/").strip("/")
    if "/" not in p:
        p = "**/" + p
    out, i = "", 0
    while i < len(p):
        if p.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif p.startswith("**", i):
            out, i = out + ".*", i + 2
        elif p[i] == "*":
            out, i = out + "[^/]*", i + 1
        elif p[i] == "?":
            out, i = out + "[^/]", i + 1
        else:
            out, i = out + re.escape(p[i]), i + 1
    return re.compile(f"^{out}$", re.I)


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def add(self, mark: str, what: str, detail: str = "") -> None:
        self.rows.append((mark, what, detail))

    def count(self, mark: str) -> int:
        return sum(1 for m, _, _ in self.rows if m == mark)


def check_commits(base: str, checker, r: Report) -> bool:
    shas = git("rev-list", "--reverse", f"{base}..HEAD").split()
    if not shas:
        r.add("⚠", "commits", f"no hay commits nuevos respecto a {base}")
        return False
    kit_commit = False
    for sha in shas:
        msg = git("log", "-1", "--format=%B", sha)
        first = msg.splitlines()[0] if msg else ""
        kit_commit |= first.startswith("chore(sdd)")
        rep = checker.Report()
        checker.check_commit_message(msg, None, rep)
        bad = [(w, d) for s, w, d in rep.rows if s == "✗"]
        warn = [(w, d) for s, w, d in rep.rows if s == "⚠"]
        if bad:
            r.add("✗", f"commit {sha[:8]}", f"«{first[:60]}»: " + "; ".join(f"{w} ({d})" for w, d in bad))
        elif warn:
            r.add("⚠", f"commit {sha[:8]}", f"«{first[:60]}»: " + "; ".join(w for w, _ in warn))
        else:
            r.add("✓", f"commit {sha[:8]}", first[:60])
    return kit_commit


def check_files(base: str, root: Path, kit_commit: bool, checker, r: Report) -> None:
    changed = [l for l in git("diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD").splitlines() if l]
    deleted = [l for l in git("diff", "--name-only", "--diff-filter=D", f"{base}...HEAD").splitlines() if l]
    r.add("·", "archivos", f"{len(changed)} cambiados o nuevos, {len(deleted)} borrados")
    cfg = {}
    try:
        cfg = json.loads((root / "sdd-guardrails.json").read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        r.add("⚠", "sdd-guardrails.json", "no existe o no es JSON: sin rutas protegidas ni patrones de secretos")
    protected = [glob_regex(p) for p in cfg.get("protected", [])]
    secrets = [glob_regex(p) for p in cfg.get("secrets", [])]
    hits = [f for f in changed + deleted if any(p.match(f) for p in protected)]
    r.add("✗" if hits else "✓", "rutas protegidas", ", ".join(hits[:10]) if hits else "sin cambios")
    added = [l for l in git("diff", "--name-only", "--diff-filter=A", f"{base}...HEAD").splitlines() if l]
    leaked = [f for f in added if any(p.match(f) for p in secrets) and f not in cfg.get("secretsAllowed", [])]
    r.add("✗" if leaked else "✓", "archivos de secretos", ", ".join(leaked) if leaked else "ninguno añadido")
    drafts = [f for f in changed if f.startswith("docs/sdd/_borradores/") and not f.endswith(".gitkeep")]
    if drafts:
        r.add("✗", "borradores", ", ".join(drafts[:5]) + ": crea el work item en Azure DevOps, anota su ID donde "
              "se citaba el borrador (bitacora.md, qa-report.md, plan.md) y borra el archivo antes del PR (ADR-0027)")
    else:
        r.add("✓", "borradores", "ninguno en la rama")
    local = [f for f in added if re.match(r"docs/sdd/[^/]+/(assets/|commit-message\.md$|test-cases\.csv$)", f)]
    if local:
        r.add("⚠", "archivos locales", ", ".join(local[:5]) + ": no se versionan (ADR-0027); un adjunto solo si es "
              "la especificación, añadido a propósito con git add -f")
    try:
        managed = set(json.loads((root / ".sdd-kit.json").read_text(encoding="utf-8")).get("managed", []))
    except (OSError, ValueError):
        managed = set()
    touched = [f for f in changed if f in managed]
    if touched and not kit_commit:
        r.add("✗", "archivos del kit", f"{len(touched)} cambiados sin un commit chore(sdd) de install.py: "
              + ", ".join(touched[:5]))
    else:
        r.add("✓", "archivos del kit", "sin cambios a mano" if not touched else "actualizados por install.py")
    agents = root / "AGENTS.md"
    if agents.exists():
        n = agents.read_text(encoding="utf-8-sig").count("\n") + 1
        r.add("✗" if n > AGENTS_MAX else "✓", "AGENTS.md", f"{n} líneas (máximo {AGENTS_MAX})")
    diff = git("diff", "-U0", "--no-color", f"{base}...HEAD")
    found = []
    current = ""
    for line in diff.splitlines():
        if line.startswith("+++ "):
            current = line[6:] if line.startswith("+++ b/") else ""
        elif line.startswith("+") and current:
            for pattern, label in SECRET_PATTERNS:
                if pattern.search(line):
                    found.append(f"{current} ({label})")
    r.add("✗" if found else "✓", "secretos en el diff", "; ".join(sorted(set(found))[:10]) if found else "ninguno")
    items = sorted({"/".join(f.split("/")[:3]) for f in changed
                    if f.startswith("docs/sdd/") and len(f.split("/")) > 3 and re.match(r"\d+-", f.split("/")[2])})
    for item in items:
        rep = checker.Report()
        checker.check_folder((root / item).resolve(), rep)
        errs = [f"{w} ({d})" for s, w, d in rep.rows if s == "✗"]
        r.add("✗" if errs else "✓", item, "; ".join(errs[:5]) if errs else "artefactos correctos")
    enc = subprocess.run([sys.executable, str(HERE / "check-encoding.py"), "--base", base],
                         capture_output=True, text=True, encoding="utf-8", errors="replace")
    r.add("✓" if enc.returncode == 0 else "✗", "codificación UTF-8",
          "correcta" if enc.returncode == 0 else (enc.stdout.strip().splitlines() or ["ver check-encoding.py"])[-1])


def main() -> int:
    ap = argparse.ArgumentParser(description="Reglas obligatorias de fi-sdd-standard antes del PR")
    ap.add_argument("--base", default="origin/dev")
    ap.add_argument("--root", default=".", type=Path)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    root = args.root.resolve()
    checker = load_checker()
    r = Report()
    try:
        git("rev-parse", "--verify", args.base)
        kit_commit = check_commits(args.base, checker, r)
        check_files(args.base, root, kit_commit, checker, r)
    except RuntimeError as exc:
        print(f"✗ git: {exc}")
        return 2
    print(f"\npr-check · {root.name} · {args.base}..HEAD\n")
    for mark, what, detail in r.rows:
        print(f"  {mark} {what}" + (f" — {detail}" if detail else ""))
    print(f"\n  {r.count('✗')} errores · {r.count('⚠')} avisos\n")
    return 1 if r.count("✗") else 0


if __name__ == "__main__":
    sys.exit(main())
