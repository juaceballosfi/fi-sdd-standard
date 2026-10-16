"""Genera el manual en un solo Markdown, pensado para leerlo una persona o darlo de contexto a una IA.

Usa las mismas fuentes que el PDF (src/*.md) y convierte su sintaxis propia a Markdown estándar:
contenedores → etiquetas y bloques de código, avisos → alertas de GitHub, fichas → tablas,
diagramas → texto. Añade al principio una guía para usarlo con una IA y al final unas preguntas
frecuentes (src/md-intro.md y src/md-faq.md).

    python build_md.py      # manual-fi-sdd-standard.md
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
OUT = ROOT / "manual-fi-sdd-standard.md"

ALERTS = {"note": "NOTE", "tip": "TIP", "warn": "WARNING", "danger": "CAUTION", "ok": "IMPORTANT", "neutral": "NOTE"}
EXAMPLES = {"ask": "Lo que pides", "out": "Lo que responde", "cmd": "Comando", "file": "Archivo"}

# Los diagramas del PDF, en texto: una IA no ve el SVG.
FIGURES = {
    "flujo.svg": """```text
UNA VEZ POR REPOSITORIO
  install.py → 0 /project-context → /document-project (opcional, por bloques, un PR por bloque)

CADA WORK ITEM
  story.md (lo copia una persona)
    → 1 /enrich-us ──G1──▶ 2 /technical-analysis ──G2──▶ 3 /wbs-execution
       (bug pequeño: /quick-fix sustituye a 1, 2 y 3 si pasa la compuerta de 8 criterios)
    → 4 /qa-review (sesión nueva) ──G3──▶ 5 /document-code → 6 pr-check y PR a dev ──G4──▶ 7 despliegue (Staging → prod)

  Bucle de QA: hallazgos «A corregir» → /wbs-execution <id> qa → /qa-review en sesión nueva (máx. 2 rondas)

QA
  /enrich-us <id> qa → /test-cases <id> → test-cases.md y CSV para Azure Test Plans
```""",
    "carpeta.svg": """```text
docs/sdd/<id>-<título>/
├── story.md              persona       el work item tal cual
├── assets/               persona       imágenes y archivos del work item (local, no se versiona)
├── bitacora.md           todas         preguntas, decisiones, hallazgos
├── pbi.md | bug.md       paso 1        requisito técnico completo (contrato funcional)
├── 00 … 06               paso 2        diseño, plan, WBS, riesgos
├── fix-plan.md           vía rápida    sustituye a 00–06
├── CHANGELOG.md          paso 3        qué se hizo y cómo se verificó
├── commit-message.md     paso 3        mensaje del commit y del PR (local, no se versiona)
├── qa-report.md          paso 4        hallazgos y decisiones
└── test-cases.md · .csv  QA            casos; el CSV de Azure Test Plans es local
```""",
    "herramientas.svg": """```text
fi-sdd-standard (core/, fuente única)
  └─ install.py --tools copilot,claude,visualstudio
       ├─ .agents/skills/    versionado · Copilot, Codex
       ├─ .claude/skills/    local (gitignore) · Claude Code
       ├─ .github/agents/    versionado · Copilot
       └─ .claude/agents/    local (gitignore) · Claude Code
Lo versionado viaja con el repositorio; lo local lo regenera install.py en cada equipo.
```""",
    "delegacion.svg": """```text
Sesión principal (la skill: decide, pregunta, verifica)
  ── paquete cerrado ──▶ code-explorer                 busca y mapea código
  ── paquete cerrado ──▶ backend-dev / frontend-dev    implementa una tarea
  ── paquete cerrado ──▶ qa-reviewer                   revisa e intenta romper
  ── paquete cerrado ──▶ doc-writer                    escribe comentarios y docs/
  ◀── informe (la sesión lo verifica: no es evidencia)
```""",
    "guardarrailes.svg": """```text
Antes de actuar        permisos deny (.claude/settings.json)   bloquea leer secretos y git commit/push
Al usar una herramienta sdd_guard.py pre (hook PreToolUse)     bloquea secretos y rutas protegidas
Tras editar            sdd_guard.py post (hook PostToolUse)    formatea, revisa UTF-8, avisa de patrones
Al compilar y probar   ArchitectureTests (xUnit)               capas y autorización de endpoints
Antes del PR           pr-check.py (.agents/scripts/)          commits, rutas, secretos, kit, UTF-8
```""",
}


CAPTIONS = {
    "flujo.svg": "el flujo SDD; los números son los pasos y G1–G4 las aprobaciones humanas.",
    "carpeta.svg": "los archivos de la carpeta del work item, quién o qué paso crea cada uno y para qué sirve.",
    "herramientas.svg": "el instalador copia la fuente única del kit al formato de cada herramienta.",
    "delegacion.svg": "la sesión principal decide y verifica; los subagentes hacen trabajo acotado con un paquete cerrado.",
    "guardarrailes.svg": "las cinco capas de guardarraíles, de la más temprana a la última.",
}


def inline(s: str) -> str:
    """HTML de una ficha → Markdown en línea."""
    s = re.sub(r"<code>(.*?)</code>", r"`\1`", s)
    s = re.sub(r"</?em>", "*", s)
    s = re.sub(r"</?strong>", "**", s)
    s = re.sub(r"<[^>]+>", "", s)
    return html.unescape(s).replace("|", "\\|")


def card_table(block: str) -> list[str]:
    pairs = re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", block, re.S)
    rows = ["| Ficha | |", "| --- | --- |"]
    rows += [f"| **{inline(k)}** | {inline(v)} |" for k, v in pairs]
    return ["", *rows, ""]


def convert(text: str) -> str:
    out: list[str] = []
    stack: list[str] = []          # cómo cerrar cada contenedor abierto
    raw: list[str] | None = None   # contenido de un ejemplo
    card: list[str] | None = None  # contenido de una ficha
    fence = None
    lines = text.splitlines()
    for line in lines:
        s = line.strip()
        if raw is not None:
            if s == ":::":
                if not any(l.strip().startswith(("```", "~~~")) for l in raw):
                    raw = ["```text", *raw, "```"]
                out.extend([*raw, ""])
                raw = None
                stack.pop()
            else:
                raw.append(line)
            continue
        if card is not None:
            if s == ":::":
                out.extend(card_table("\n".join(card)))
                card = None
                stack.pop()
            else:
                card.append(line)
            continue
        m = re.match(r"^(```+|~~~+)", s)
        if m:
            fence = m.group(1) if fence is None else (None if s.startswith(fence) else fence)
            out.append(_prefix(stack) + line)
            continue
        if fence is None and s.startswith("@@figure "):
            name, _, caption = s[9:].partition("|")
            out.append(_prefix(stack) + f"*Esquema: {CAPTIONS[name.strip()]}*")
            out.append(_prefix(stack))
            out.extend(_prefix(stack) + l for l in FIGURES[name.strip()].splitlines())
            continue
        if fence is None and s.startswith(":::"):
            spec = s[3:].strip()
            if not spec:
                stack.pop()
                out.append("")
                continue
            kind, _, label = spec.partition(" ")
            label = label.strip()
            if kind in ALERTS:
                out.extend(["", f"> [!{ALERTS[kind]}]"])
                if label:
                    out.append(f"> **{label}**")
                    out.append(">")
                stack.append("ALERT")
            elif kind in EXAMPLES or kind == "view":
                title = label or EXAMPLES.get(kind, "")
                out.extend(["", f"**{title}:**", ""])
                if kind == "view":
                    stack.append("")
                else:
                    stack.append("")
                    raw = []
            elif kind == "card":
                stack.append("")
                card = []
            elif kind in ("tile", "tile-accent"):
                out.extend(["", f"**{label}**" if label else "", ""])
                stack.append("")
            elif kind in ("grid2", "grid3", "avoid", "lead"):
                out.append("")
                stack.append("")
            else:
                raise SystemExit(f"contenedor desconocido: {kind}")
            continue
        out.append(_prefix(stack) + line)
    return "\n".join(out)


def _prefix(stack: list[str]) -> str:
    return "> " if "ALERT" in stack else ""


def renumber(text: str, n: int, annex: bool) -> str:
    """# → ## N. Título · ## → ### N.M Título · ### → #### · #### → #####. No toca los bloques de código."""
    out, fence, m2 = [], None, 0
    for line in text.splitlines():
        s = line.lstrip("> ").strip() if line.startswith(">") else line
        f = re.match(r"^\s*(```+|~~~+)", s)
        if f:
            fence = f.group(1) if fence is None else (None if s.strip().startswith(fence) else fence)
        h = None if fence or (f and fence is None and s.strip().startswith(("```", "~~~"))) else re.match(r"^(#{1,5}) (.*)$", line)
        if h and not line.startswith(">"):
            level, title = len(h.group(1)), h.group(2)
            if level == 1:
                line = f"## Anexo · {title}" if annex else f"## {n}. {title}"
            elif level == 2:
                m2 += 1
                line = f"### {'A' if annex else n}.{m2} {title}"
            else:
                line = "#" * (level + 1) + " " + title
        out.append(line)
    return "\n".join(out)


def tidy(text: str) -> str:
    text = re.sub(r"(?m)^> *$\n(?=> *$)", "", text)          # líneas vacías repetidas en alertas
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?m)^(> \[![A-Z]+\])\n>\n", r"\1\n", text)
    return text.strip() + "\n"


def main() -> None:
    from meta import DATE, SKILLS, VERSION  # una sola fuente para la versión y la fecha
    intro = (SRC / "md-intro.md").read_text(encoding="utf-8").strip()
    intro = intro.replace("{{VERSION}}", VERSION).replace("{{SKILLS}}", SKILLS).replace("{{DATE}}", DATE)
    parts = [intro]
    files = sorted(SRC.glob("[0-9][0-9]-*.md"))
    for n, f in enumerate(files, start=1):
        annex = f.name.startswith("9")
        body = renumber(convert(f.read_text(encoding="utf-8")), n, annex)
        parts.append(body.strip())
    parts.append((SRC / "md-faq.md").read_text(encoding="utf-8").strip())
    text = tidy("\n\n---\n\n".join(parts))
    for bad in (":::", "@@figure", "<dl", "markdown=\"1\""):
        if bad in text:
            raise SystemExit(f"queda sintaxis sin convertir: {bad}")
    OUT.write_text(text, encoding="utf-8")
    words = len(text.split())
    print(f"✓ {OUT.name} · {len(text.splitlines())} líneas · {words} palabras · ~{len(text) // 4} tokens")


if __name__ == "__main__":
    main()
