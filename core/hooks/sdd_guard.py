#!/usr/bin/env python3
"""Claude Code hook of fi-sdd-standard (ADR-0023). No AI, standard library only.

    python sdd_guard.py pre    # PreToolUse: Read, Edit, Write, MultiEdit, NotebookEdit, Bash, PowerShell
    python sdd_guard.py post   # PostToolUse: Edit, Write, MultiEdit

pre  blocks editing a protected path and reading or editing a secret file, also through a shell
     command that names it.
post runs the formatter configured for the file's extension, checks that the file is still UTF-8
     and warns about the configured patterns.

The rules come from `sdd-guardrails.json` at the repository root (written by install.py and
completed by /project-context). The hook is an early warning: every mandatory rule is also checked
by a test or by pr-check.py (ADR-0012, ADR-0023).
Exit code 0 = no decision (the normal permission flow applies) · 2 = blocked (pre) or a warning the
agent must read (post). Any internal error exits 0: a broken hook must never stop the work.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

CONFIG = "sdd-guardrails.json"
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "PowerShell"}
# Words of a shell command that look like a file name, to compare with the secret patterns.
PATH_TOKEN = re.compile(r"[\w./\\:*-]*(?:\.env(?:\.[\w-]+)?|appsettings\.[\w.-]+\.json|secrets\.json|\.pfx|\.key|\.pem)\b",
                        re.I)


def glob_regex(pattern: str) -> re.Pattern:
    """Gitignore-like glob: ** any folders, * within a folder, ? one character. No slash = any folder."""
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


def matches(rel: str, patterns: list[str]) -> str | None:
    return next((p for p in patterns if glob_regex(p).match(rel)), None)


def project_root(event: dict) -> Path:
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or event.get("cwd") or ".").resolve()


def relative(path: str, root: Path) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = root / p
    try:
        return p.resolve().relative_to(root).as_posix()
    except ValueError:
        return p.as_posix()


def load_config(root: Path) -> dict:
    try:
        return json.loads((root / CONFIG).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def block(message: str) -> int:
    print(f"fi-sdd-standard · bloqueado: {message} ({CONFIG}, ADR-0023)", file=sys.stderr)
    return 2


def pre(event: dict, root: Path, cfg: dict) -> int:
    tool, data = event.get("tool_name", ""), event.get("tool_input") or {}
    secrets, protected = cfg.get("secrets", []), cfg.get("protected", [])
    if tool in EDIT_TOOLS or tool == "Read":
        path = data.get("file_path") or data.get("notebook_path")
        if not path:
            return 0
        rel = relative(path, root)
        if (hit := matches(rel, secrets)) and rel not in cfg.get("secretsAllowed", []):
            return block(f"«{rel}» puede contener secretos (patrón «{hit}»); pide a una persona el dato que necesitas")
        if tool in EDIT_TOOLS and (hit := matches(rel, protected)):
            return block(f"«{rel}» es una ruta protegida (patrón «{hit}»); el cambio va en su origen")
        return 0
    if tool in SHELL_TOOLS:
        command = str(data.get("command", ""))
        for token in PATH_TOKEN.findall(command):
            name = token.replace("\\", "/").strip("'\"").rsplit("/", 1)[-1]
            if "*" not in name and (hit := matches(name, secrets)) and name not in cfg.get("secretsAllowed", []):
                return block(f"el comando usa «{name}», que puede contener secretos (patrón «{hit}»)")
    return 0


def post(event: dict, root: Path, cfg: dict) -> int:
    data = event.get("tool_input") or {}
    path = data.get("file_path")
    if not path:
        return 0
    file = Path(path) if Path(path).is_absolute() else root / path
    rel = relative(path, root)
    if not file.is_file():
        return 0
    warnings: list[str] = []
    command = (cfg.get("format") or {}).get(file.suffix.lower())
    if command:
        args = [a.replace("{file}", str(file)) for a in command]
        try:
            res = subprocess.run(args, cwd=root, capture_output=True, text=True, timeout=90)
            if res.returncode != 0:
                warnings.append(f"el formateador ({args[0]}) terminó con código {res.returncode}: revisa el archivo")
        except (OSError, subprocess.SubprocessError) as exc:
            warnings.append(f"no se pudo ejecutar el formateador ({args[0]}): {exc.__class__.__name__}")
    raw = file.read_bytes()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        warnings.append("ya no es UTF-8 (¿se guardó como Windows-1252?): vuelve a escribirlo en UTF-8 y conserva el BOM si lo tenía")
        text = raw.decode("utf-8", errors="replace")
    for rule in cfg.get("patterns", []):
        if not glob_regex(rule.get("glob", "**")).match(rel):
            continue
        if rule.get("forbid") and re.search(rule["forbid"], text, re.M):
            warnings.append(rule.get("message", f"contiene el patrón prohibido «{rule['forbid']}»"))
        if rule.get("require") and not re.search(rule["require"], text, re.M):
            warnings.append(rule.get("message", f"le falta el patrón obligatorio «{rule['require']}»"))
    if not warnings:
        return 0
    print(f"fi-sdd-standard · {rel}:\n" + "\n".join(f"  - {w}" for w in warnings), file=sys.stderr)
    return 2


def main() -> int:
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        event = json.loads(sys.stdin.read() or "{}")
        root = project_root(event)
        cfg = load_config(root)
        if mode == "pre":
            return pre(event, root, cfg)
        if mode == "post":
            return post(event, root, cfg)
    except Exception:  # noqa: BLE001 - a hook failure must never block the session
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
