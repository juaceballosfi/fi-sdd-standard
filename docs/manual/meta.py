"""Versión del kit, de las skills y fecha de generación: una sola fuente para build.py y build_md.py."""

import datetime
import re
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent.parent
VERSION = (KIT / "VERSION").read_text(encoding="utf-8").strip()
SKILLS = re.search(r"· v(\d+\.\d+)", (KIT / "core" / "skills" / "enrich-us" / "SKILL.md").read_text(encoding="utf-8")).group(1)
_MONTHS = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
           "octubre", "noviembre", "diciembre"]
_today = datetime.date.today()
DATE = f"{_today.day} de {_MONTHS[_today.month - 1]} de {_today.year}"
