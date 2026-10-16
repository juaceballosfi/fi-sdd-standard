#!/usr/bin/env python3
"""Create the folder of a new work item so a person can prepare story.md (ADR-0015).

Usage (from the project root):
    python <kit>/scripts/new-sdd-item.py <id> "<work item title>" [--tipo pbi|bug] [--por "<name>"]

Creates docs/sdd/<id>-<slug>/ with:
    story.md     header pre-filled (ID, title, type, who prepares it, date); the person copies the
                 work item from Azure DevOps into it
    bitacora.md  working log with the first entry
    assets/      images and files of the work item

The slug follows the same rule as enrich-us: title in lowercase, without accents, every other
character replaced by '-', cut at a '-' so it is at most 40 characters.
It never overwrites anything: if a folder for that ID already exists, it only creates what is
missing (assets/, bitacora.md, story.md) and leaves every existing file untouched.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import unicodedata
from datetime import date
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent
VERSION = (KIT / "VERSION").read_text(encoding="utf-8").strip()
TEMPLATES = KIT / "core" / "skills" / "enrich-us" / "templates"
SLUG_MAX = 40
BUG_BLOCK = re.compile(r"<!-- solo-bug -->\n(.*?)<!-- /solo-bug -->\n\n?", re.S)


def slugify(title: str) -> str:
    text = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(slug) > SLUG_MAX:
        cut = slug[:SLUG_MAX + 1]
        slug = cut[:cut.rfind("-")] if "-" in cut else slug[:SLUG_MAX]
    return slug.strip("-")


def git_user(target: Path) -> str:
    try:
        out = subprocess.run(["git", "-C", str(target), "config", "--get", "user.name"],
                             capture_output=True, text=True, timeout=10)
        return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def shown(path: Path) -> str:
    """Path relative to the current folder when possible (shorter commands to copy)."""
    try:
        return os.path.relpath(path)
    except ValueError:  # another drive on Windows
        return str(path)


def build_story(item_id: str, title: str, kind: str, person: str, today: str) -> str:
    text = (TEMPLATES / "story.md").read_text(encoding="utf-8")
    text = text.replace("# Work item <ID> — <Título>", f"# Work item {item_id} — {title}", 1)
    text = text.replace("**Preparado por:** <persona> · **Leído:** <AAAA-MM-DD>",
                        f"**Preparado por:** {person} · **Leído:** {today}", 1)
    text = text.replace("<PBI | Bug>", "Bug" if kind == "bug" else "PBI", 1)
    if kind == "bug":  # Azure DevOps bugs use Repro Steps and System Info instead of Description
        text = text.replace("## Descripción\n\n<texto literal>\n\n", "", 1)
        return BUG_BLOCK.sub(lambda m: m.group(1) + "\n", text)
    return BUG_BLOCK.sub("", text)


def build_log(item_id: str, title: str, folder: str, person: str, today: str) -> str:
    text = (TEMPLATES / "bitacora.md").read_text(encoding="utf-8")
    text = text.replace("# Bitácora — <ID> <Título>", f"# Bitácora — {item_id} {title}", 1)
    text = re.sub(r"^\*\*Generado con:\*\*.*$", f"**Creado con:** new-sdd-item.py · fi-sdd-standard v{VERSION}",
                  text, count=1, flags=re.M)
    text = text.replace("#[ID]", f"#{item_id}", 1).replace("docs/sdd/[ID]-[slug]/", folder, 1)
    text = re.sub(r"^- AAAA-MM-DD · <persona> · .*$",
                  f"- {today} · {person} · carpeta creada con new-sdd-item.py; story.md pendiente de rellenar",
                  text, count=1, flags=re.M)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description="Crea la carpeta de un work item para preparar story.md")
    parser.add_argument("id", help="ID del work item en Azure DevOps")
    parser.add_argument("titulo", help="Título del work item, tal cual (entre comillas)")
    parser.add_argument("--tipo", choices=("pbi", "bug"), default="pbi", help="pbi (por defecto) o bug")
    parser.add_argument("--por", help="Quién prepara story.md (por defecto, git config user.name)")
    parser.add_argument("--target", type=Path, default=Path("."), help="Raíz del proyecto (por defecto, la carpeta actual)")
    args = parser.parse_args()

    item_id = args.id.strip().lstrip("#")
    if not item_id.isdigit():
        print(f"El ID debe ser un número: «{args.id}»")
        return 2
    title = " ".join(args.titulo.split())
    slug = slugify(title)
    if not slug:
        print("El título no deja ningún carácter válido para el nombre de la carpeta")
        return 2

    target = args.target.resolve()
    if target == KIT or KIT in target.parents:
        print("Ejecútalo desde la raíz del proyecto, no desde el kit")
        return 2
    sdd = target / "docs" / "sdd"
    if not sdd.is_dir():
        print(f"No existe {shown(sdd)}: ejecútalo desde la raíz del proyecto o instala antes el kit (install.py)")
        return 2
    existing = sorted(p for p in sdd.glob(f"{item_id}-*") if p.is_dir())
    if len(existing) > 1:
        print(f"Hay varias carpetas para el work item {item_id}; deja solo una:")
        for p in existing:
            print(f"  {shown(p)}")
        return 1

    person = (args.por or git_user(target) or "<persona>").strip()
    today = date.today().isoformat()
    folder = existing[0] if existing else sdd / f"{item_id}-{slug}"
    rel = f"docs/sdd/{folder.name}/"
    created: list[str] = []
    folder.mkdir(parents=True, exist_ok=True)
    if not (folder / "story.md").exists():
        (folder / "story.md").write_text(build_story(item_id, title, args.tipo, person, today), encoding="utf-8", newline="\n")
        created.append("story.md     ← cópialo desde Azure DevOps (instrucciones en el comentario del archivo)")
    if not (folder / "bitacora.md").exists():
        (folder / "bitacora.md").write_text(build_log(item_id, title, rel, person, today), encoding="utf-8", newline="\n")
        created.append("bitacora.md  ← notas de trabajo; ya tiene la primera entrada")
    if not (folder / "assets").is_dir():
        (folder / "assets").mkdir(parents=True)
        created.append("assets/      ← imágenes y archivos del work item, con nombre descriptivo")

    checker = shown(KIT / "scripts" / "check-sdd-item.py")
    if existing:
        print(f"\nLa carpeta del work item {item_id} ya existía: {rel}")
        if created:
            print("Solo se ha creado lo que faltaba; story.md y lo demás no se han tocado:")
            for line in created:
                print(f"  {line}")
        else:
            print("No falta nada: no se ha tocado ningún archivo.")
        if folder.name != f"{item_id}-{slug}" and not re.fullmatch(r"\d+-[a-z0-9]+(?:-[a-z0-9]+)*", folder.name):
            print(f"\n  Aviso: el nombre no sigue el formato (minúsculas, sin tildes). Sugerido: {item_id}-{slug}")
    else:
        print(f"\nCreado {rel}")
        for line in created:
            print(f"  {line}")
    if person == "<persona>":
        print("\n  Aviso: no se encontró git user.name; pon tu nombre en «Preparado por» o usa --por")
    print("\nSiguiente:")
    print(f"  1. Rellena story.md y guarda las imágenes en assets/")
    print(f"  2. python {checker} {shown(folder)}")
    print(f"  3. En una sesión nueva: /enrich-us {item_id}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
