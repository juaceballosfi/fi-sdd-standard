#!/usr/bin/env python3
"""Check that the text files changed in a branch are UTF-8, and optionally repair them.

Usage (from the project root):
    python <kit>/scripts/check-encoding.py --base origin/dev          # check only
    python <kit>/scripts/check-encoding.py --base origin/dev --fix    # repair to UTF-8

Why: on Windows, an AI agent that edits a file with a script that does not pass
encoding="utf-8" saves it as Windows-1252. Accents and «—» then break, and Azure Repos shows
"utf-8 -> Windows-1252" in the PR. Detected in the Bonis pilot (PBI 40944).

It also reports a file whose UTF-8 BOM was added or removed compared with the base branch: the
text is the same, but Azure Repos then shows an encoding change ("utf-8 -> Windows-1252") for the
whole file. --fix restores the BOM state of the base.

--fix keeps every valid UTF-8 sequence and reads each invalid byte as Windows-1252, so it also
repairs files that mix both encodings. It keeps an existing UTF-8 BOM and the line endings.
Exit code 0 = all UTF-8 (or repaired), 1 = files still not UTF-8, 2 = usage or git error.
"""
from __future__ import annotations

import argparse
import codecs
import subprocess
import sys
from pathlib import Path

TEXT_EXT = {".ts", ".tsx", ".js", ".jsx", ".json", ".cs", ".csproj", ".props", ".md", ".css", ".scss",
            ".html", ".yml", ".yaml", ".xml", ".resx", ".sql", ".py", ".ps1", ".txt", ".config"}
BOM = b"\xef\xbb\xbf"


def _cp1252_fallback(err: UnicodeDecodeError):
    return err.object[err.start:err.end].decode("cp1252", errors="replace"), err.end


codecs.register_error("cp1252-fallback", _cp1252_fallback)


def changed_files(base: str) -> list[str]:
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AMR", f"{base}...HEAD"],
                         capture_output=True, text=True, encoding="utf-8")
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or "git diff failed")
    return [f for f in out.stdout.splitlines() if Path(f).suffix.lower() in TEXT_EXT]


def base_bytes(base: str, name: str) -> bytes | None:
    out = subprocess.run(["git", "show", f"{base}:{name}"], capture_output=True)
    return out.stdout if out.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba (y repara) que los archivos cambiados están en UTF-8")
    parser.add_argument("--base", default="origin/dev", help="Rama base de la comparación (por defecto origin/dev)")
    parser.add_argument("--fix", action="store_true", help="Convierte a UTF-8 los archivos que no lo están")
    args = parser.parse_args()
    try:
        files = changed_files(args.base)
    except (RuntimeError, OSError) as exc:
        print(f"No se pudo obtener la lista de archivos: {exc}")
        return 2

    bad = []
    bom_changed = []
    for name in files:
        path = Path(name)
        if not path.is_file():
            continue
        data = path.read_bytes()
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            line = data[:exc.start].count(b"\n") + 1
            bad.append((path, line))
            continue
        before = base_bytes(args.base, name)
        if before is not None and before.startswith(BOM) != data.startswith(BOM):
            bom_changed.append((path, before.startswith(BOM)))

    print(f"\n{len(files)} archivo(s) de texto cambiados frente a {args.base}\n")
    for path, had_bom in bom_changed:
        what = "ha perdido el BOM que tenía" if had_bom else "ha ganado un BOM que no tenía"
        if args.fix:
            data = path.read_bytes()
            path.write_bytes(BOM + data if had_bom else data[len(BOM):])
            print(f"  ✓ BOM restaurado  {path.as_posix()} ({what})")
        else:
            print(f"  ⚠ BOM  {path.as_posix()} {what} en {args.base}: el texto es el mismo, pero Azure Repos "
                  "lo muestra como cambio de codificación. Restáuralo con --fix")
    if not bad:
        print("  ✓ Todos están en UTF-8\n")
        return 1 if bom_changed and not args.fix else 0
    for path, line in bad:
        if args.fix:
            data = path.read_bytes()
            bom = data.startswith(BOM)
            text = data[len(BOM) if bom else 0:].decode("utf-8", errors="cp1252-fallback")
            path.write_bytes((BOM if bom else b"") + text.encode("utf-8"))
            print(f"  ✓ reparado  {path.as_posix()} (el primer carácter erróneo estaba en la línea {line})")
        else:
            print(f"  ✗ no UTF-8  {path.as_posix()} (primer carácter erróneo en la línea {line})")
    if args.fix:
        print("\n  Revisa el cambio con `git diff` y vuelve a ejecutar sin --fix.\n")
        return 0
    print("\n  Repáralos con --fix.\n")
    return 1


if __name__ == "__main__":
    sys.exit(main())
