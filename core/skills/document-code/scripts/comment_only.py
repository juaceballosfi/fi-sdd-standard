#!/usr/bin/env python3
"""Check that documentation changed only comments (document-code, fi-sdd-standard).

Usage:
    python comment_only.py save  <snapshot-dir> <file> [<file> ...]
    python comment_only.py check <snapshot-dir> <file> [<file> ...]
    python comment_only.py restore <snapshot-dir> <file> [<file> ...]

`save` copies the files before the documentation step (works for untracked files too).
`check` compares each file with its copy: every added, removed or changed line must be blank or a
comment, and the encoding (BOM) and line endings must be the same. Exit code 0 = only comments,
1 = something else changed, 2 = usage error. Files under docs/ are not checked (they are docs).
`restore` puts the saved copy back, byte for byte, to discard the documentation of a file.
"""
from __future__ import annotations

import difflib
import shutil
import sys
from pathlib import Path

COMMENT_PREFIXES = {
    ".cs": ("//", "/*", "*", "*/", "#region", "#endregion"),
    ".ts": ("//", "/*", "*", "*/"),
    ".tsx": ("//", "/*", "*", "*/", "{/*"),
    ".js": ("//", "/*", "*", "*/"),
    ".jsx": ("//", "/*", "*", "*/", "{/*"),
    ".py": ("#",),
    ".sql": ("--", "/*", "*", "*/"),
}


def key(path: str) -> str:
    """Snapshot name for a path: keeps it unique and readable."""
    return path.replace("\\", "/").strip("/").replace("/", "__")


def is_comment(line: str, suffix: str) -> bool:
    text = line.strip()
    if not text:
        return True
    return text.startswith(COMMENT_PREFIXES.get(suffix, ("//", "/*", "*", "*/", "#")))


def endings(data: bytes) -> str:
    crlf = data.count(b"\r\n")
    lf = data.count(b"\n") - crlf
    return "CRLF" if crlf and not lf else "LF" if lf and not crlf else "mixed" if crlf and lf else "none"


def save(snapshot: Path, files: list[str]) -> int:
    snapshot.mkdir(parents=True, exist_ok=True)
    for f in files:
        src = Path(f)
        if not src.is_file():
            print(f"✗ {f}: no existe")
            return 2
        shutil.copyfile(src, snapshot / key(f))
    print(f"✓ {len(files)} archivo(s) guardados en {snapshot}")
    return 0


def check(snapshot: Path, files: list[str]) -> int:
    problems = 0
    for f in files:
        path, saved = Path(f), snapshot / key(f)
        if path.parts and path.parts[0] == "docs":
            continue
        if not saved.is_file():
            print(f"✗ {f}: no hay copia guardada (ejecuta antes «save» con este archivo)")
            problems += 1
            continue
        before, after = saved.read_bytes(), path.read_bytes()
        if before == after:
            print(f"· {f}: sin cambios")
            continue
        issues = []
        if before.startswith(b"\xef\xbb\xbf") != after.startswith(b"\xef\xbb\xbf"):
            issues.append("cambió el BOM (se debe conservar)")
        if endings(before) != endings(after) and endings(before) != "none":
            issues.append(f"cambiaron los finales de línea ({endings(before)} → {endings(after)})")
        old = before.decode("utf-8-sig", errors="replace").splitlines()
        new = after.decode("utf-8-sig", errors="replace").splitlines()
        added = 0
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, old, new, autojunk=False).get_opcodes():
            if tag == "equal":
                continue
            for n, line in enumerate(old[i1:i2], i1 + 1):
                if not is_comment(line, path.suffix):
                    issues.append(f"línea {n} (antes) cambió o se borró: {line.strip()[:90]}")
            for n, line in enumerate(new[j1:j2], j1 + 1):
                if not is_comment(line, path.suffix):
                    issues.append(f"línea {n} (ahora) no es comentario: {line.strip()[:90]}")
                elif line.strip():
                    added += 1
        if issues:
            problems += 1
            print(f"✗ {f}")
            for issue in issues[:15]:
                print(f"    {issue}")
            if len(issues) > 15:
                print(f"    … y {len(issues) - 15} más")
        else:
            print(f"✓ {f}: solo comentarios ({added} línea(s) de comentario)")
    print(f"\n{'Solo cambiaron comentarios' if not problems else f'{problems} archivo(s) con cambios que no son comentarios'}")
    return 1 if problems else 0


def restore(snapshot: Path, files: list[str]) -> int:
    for f in files:
        saved = snapshot / key(f)
        if not saved.is_file():
            print(f"✗ {f}: no hay copia guardada")
            return 2
        shutil.copyfile(saved, f)
        print(f"✓ {f}: restaurado")
    return 0


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles (cp1252) cannot print ✓ ✗
    commands = {"save": save, "check": check, "restore": restore}
    if len(argv) < 4 or argv[1] not in commands:
        print(__doc__)
        return 2
    return commands[argv[1]](Path(argv[2]), argv[3:])


if __name__ == "__main__":
    sys.exit(main(sys.argv))
