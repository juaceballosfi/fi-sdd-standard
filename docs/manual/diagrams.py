"""Diagramas SVG del manual, con la paleta del FI Design System. Escribe src/fig/*.svg."""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / "src" / "fig"
NAVY9, NAVY7, NAVY4, NAVY2, NAVY1 = "#232f41", "#374a66", "#7b8fb2", "#ccd5e6", "#e6ebf3"
Y5, Y7, Y50, Y2 = "#efac14", "#a8710f", "#fff8e6", "#fbdd8c"
N0, N2, N3, N6 = "#ffffff", "#e5e5ee", "#d2d2e0", "#74758f"
G6, G50 = "#0f7a56", "#e8f7f0"
FONT = "Jost, sans-serif"
MONO = "JetBrains Mono, monospace"


class Svg:
    def __init__(self, w, h):
        self.w, self.h, self.items = w, h, []

    def add(self, s):
        self.items.append(s)

    def box(self, x, y, w, h, title, sub="", *, kind="step", num=None):
        fill, stroke, fg, subfg = {
            "step": (NAVY9, NAVY9, N0, NAVY2),
            "light": (N0, NAVY4, NAVY9, N6),
            "opt": (N0, NAVY4, NAVY9, N6),
            "brand": (Y5, Y5, NAVY9, NAVY9),
            "fast": (Y50, Y5, NAVY9, Y7),
            "qa": (G50, G6, NAVY9, G6),
        }[kind]
        dash = ' stroke-dasharray="4 4"' if kind == "opt" else ""
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="1.4"{dash}/>')
        tx = x + 12
        if num is not None:
            self.add(f'<circle cx="{x + 16}" cy="{y + h / 2}" r="9" fill="{Y5}"/>'
                     f'<text x="{x + 16}" y="{y + h / 2 + 3.6}" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="{NAVY9}">{num}</text>')
            tx = x + 32
        ty = y + h / 2 + (4 if not sub else -2)
        self.add(f'<text x="{tx}" y="{ty}" font-family="{MONO}" font-size="11" font-weight="600" fill="{fg}">{escape(title)}</text>')
        if sub:
            self.add(f'<text x="{tx}" y="{ty + 13}" font-family="{FONT}" font-size="9.5" fill="{subfg}">{escape(sub)}</text>')

    def arrow(self, d, color=NAVY4, dash=False):
        da = ' stroke-dasharray="4 4"' if dash else ""
        self.add(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="1.4"{da} marker-end="url(#ah)"/>')

    def gate(self, x, y, label):
        self.add(f'<g transform="translate({x} {y})"><rect x="-13" y="-10" width="26" height="20" rx="10" fill="{N0}" stroke="{Y5}" stroke-width="1.6"/>'
                 f'<text y="3.8" text-anchor="middle" font-family="{MONO}" font-size="9.5" font-weight="700" fill="{Y7}">{label}</text></g>')

    def text(self, x, y, s, *, size=9.5, color=N6, weight=400, anchor="start", mono=False):
        f = MONO if mono else FONT
        self.add(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{f}" font-size="{size}" font-weight="{weight}" fill="{color}">{escape(s)}</text>')

    def write(self, name):
        defs = (f'<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M0,0 L10,5 L0,10 z" fill="{NAVY4}"/></marker></defs>')
        svg = (f'<svg viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" role="img">{defs}'
               + "".join(self.items) + "</svg>")
        (OUT / name).write_text(svg, encoding="utf-8")


def flujo():
    s = Svg(760, 400)
    # fila 0: una vez por repositorio
    s.text(20, 18, "UNA VEZ POR REPOSITORIO", size=8.5, weight=700, color=N6)
    s.box(20, 26, 190, 44, "/project-context", "contexto, docs/ base y pruebas", num=0)
    s.arrow("M 210 48 L 240 48")
    s.box(242, 26, 210, 44, "/document-project", "opcional · por bloques, un PR cada uno", kind="opt")
    s.text(470, 44, "install.py antes de todo: copia skills,", size=9)
    s.text(470, 57, "subagentes, hooks y reglas al proyecto", size=9)
    # fila 1
    s.text(20, 104, "CADA WORK ITEM", size=8.5, weight=700, color=N6)
    s.box(20, 112, 96, 44, "story.md", "copiado a mano", kind="brand")
    s.arrow("M 116 134 L 136 134")
    s.box(138, 112, 160, 44, "/enrich-us", "pbi.md o bug.md", num=1)
    s.arrow("M 298 134 L 344 134")
    s.gate(321, 134, "G1")
    s.box(346, 112, 190, 44, "/technical-analysis", "diseño 00–06 · WBS", num=2)
    s.arrow("M 536 134 L 582 134")
    s.gate(559, 134, "G2")
    s.box(584, 112, 156, 44, "/wbs-execution", "código, pruebas, commit", num=3)
    # vía rápida
    s.box(138, 176, 602, 34, "/quick-fix", "bug pequeño que pasa la compuerta de 8 criterios: sustituye a los pasos 1, 2 y 3", kind="fast")
    s.arrow("M 68 156 L 68 193 L 136 193", color=Y5)
    # bajada
    s.arrow("M 740 134 L 752 134 L 752 240 L 120 240 L 120 258")
    s.add(f'<path d="M 740 193 L 752 193" stroke="{Y5}" stroke-width="1.4"/>')
    # fila 2
    s.box(20, 260, 168, 44, "/qa-review", "sesión nueva · qa-report.md", num=4)
    s.arrow("M 188 282 L 234 282")
    s.gate(211, 282, "G3")
    s.box(236, 260, 164, 44, "/document-code", "comentarios y docs/", num=5)
    s.arrow("M 400 282 L 420 282")
    s.box(422, 260, 150, 44, "pr-check · PR", "commit y PR a dev", num=6)
    s.arrow("M 572 282 L 618 282")
    s.gate(595, 282, "G4")
    s.box(620, 260, 120, 44, "despliegue", "Staging → prod", num=7)
    # bucle de QA
    s.arrow("M 150 304 L 150 318 L 8 318 L 8 282 L 18 282", dash=True)
    s.text(160, 334, "Bucle de QA: hallazgos «A corregir» → /wbs-execution <id> qa → /qa-review en sesión nueva (máx. 2 rondas)", size=9, color=Y7)
    # QA
    s.text(20, 374, "QA", size=8.5, weight=700, color=N6)
    s.box(46, 360, 170, 30, "/enrich-us <id> qa", kind="qa")
    s.arrow("M 216 375 L 236 375")
    s.box(238, 360, 160, 30, "/test-cases <id>", kind="qa")
    s.text(410, 379, "test-cases.md y CSV para Azure Test Plans", size=9.5)
    s.write("flujo.svg")


def carpeta():
    s = Svg(760, 210)
    rows = [
        ("story.md", "persona", "El work item tal cual", "brand"),
        ("bitacora.md", "todas", "Preguntas, decisiones, hallazgos", "light"),
        ("pbi.md · bug.md", "1", "Requisito técnico completo", "step"),
        ("00 … 06", "2", "Diseño, plan, WBS, riesgos", "step"),
        ("CHANGELOG.md", "3", "Qué se hizo y cómo se verificó", "step"),
        ("commit-message.md", "3", "Mensaje del commit (local)", "opt"),
        ("qa-report.md", "4", "Hallazgos y decisiones", "step"),
        ("fix-plan.md", "vía rápida", "Sustituye a 00–06", "fast"),
        ("test-cases.md · .csv", "QA", "Casos; el CSV es local", "qa"),
        ("assets/", "persona", "Imágenes del work item (local)", "opt"),
    ]
    for i, (name, step, what, kind) in enumerate(rows):
        col, row = divmod(i, 5)
        x, y = 20 + col * 370, 12 + row * 39
        s.box(x, y, 190, 32, name, kind=kind)
        s.text(x + 200, y + 14, what, size=10, color=NAVY9, weight=500)
        s.text(x + 200, y + 27, f"paso: {step}", size=8.5, color=N6)
    s.write("carpeta.svg")


def herramientas():
    s = Svg(760, 230)
    s.box(280, 12, 200, 44, "fi-sdd-standard", "core/ · fuente única", kind="brand")
    s.arrow("M 380 56 L 380 80")
    s.box(290, 82, 180, 36, "install.py", "--tools copilot,claude,visualstudio", kind="light")
    targets = [
        (20, ".agents/skills/", "versionado · Copilot, Codex"),
        (210, ".claude/skills/", "local · Claude Code"),
        (400, ".github/agents/", "versionado · Copilot"),
        (590, ".claude/agents/", "local · Claude Code"),
    ]
    for x, t, sub in targets:
        s.arrow(f"M 380 118 L {x + 75} 160")
        s.box(x, 162, 150, 44, t, sub, kind="step" if "versionado" in sub else "opt")
    s.text(380, 222, "Lo versionado viaja con el repositorio; lo local lo regenera install.py en cada equipo.", size=9.5, anchor="middle")
    s.write("herramientas.svg")


def guardarrailes():
    s = Svg(760, 190)
    cols = [
        ("Antes de actuar", "permisos deny", ".claude/settings.json", "Bloquea leer secretos y git commit/push", "step"),
        ("Al usar una herramienta", "sdd_guard.py pre", "hook PreToolUse", "Bloquea secretos y rutas protegidas", "step"),
        ("Tras editar", "sdd_guard.py post", "hook PostToolUse", "Formatea, revisa UTF-8 y avisa de patrones", "light"),
        ("Al compilar y probar", "ArchitectureTests", "pruebas xUnit", "Capas y autorización de endpoints", "light"),
        ("Antes del PR", "pr-check.py", ".agents/scripts/", "Commits, rutas, secretos, kit, UTF-8", "brand"),
    ]
    for i, (when, name, where, what, kind) in enumerate(cols):
        x = 14 + i * 150
        s.text(x, 18, when.upper(), size=8, weight=700)
        s.box(x, 26, 138, 46, name, where, kind=kind)
        words, line, ly = what.split(), "", 92
        for w in words:
            if len(line) + len(w) > 24:
                s.text(x + 2, ly, line.strip(), size=9.5, color=NAVY9)
                line, ly = "", ly + 13
            line += w + " "
        s.text(x + 2, ly, line.strip(), size=9.5, color=NAVY9)
        if i < 4:
            s.arrow(f"M {x + 138} 49 L {x + 150} 49")
    s.text(380, 176, "Cada regla obligatoria tiene al menos una comprobación que no depende de que la IA obedezca (ADR-0012, ADR-0023).", size=9.5, anchor="middle")
    s.write("guardarrailes.svg")


def delegacion():
    s = Svg(760, 200)
    s.box(20, 70, 200, 56, "Sesión principal", "la skill: decide, pregunta, verifica", kind="brand")
    agents = [("code-explorer", "busca y mapea código"), ("backend-dev / frontend-dev", "implementa una tarea"),
              ("qa-reviewer", "revisa e intenta romper"), ("doc-writer", "escribe comentarios y docs/")]
    for i, (n, sub) in enumerate(agents):
        y = 10 + i * 46
        s.arrow(f"M 220 98 L 400 {y + 18}")
        s.box(402, y, 220, 36, n, sub)
    s.text(300, 186, "paquete cerrado →", size=9.5, color=Y7, anchor="middle")
    s.text(640, 70, "← informe", size=9.5, color=Y7)
    s.text(640, 84, "(la sesión lo verifica:", size=9)
    s.text(640, 97, "no es evidencia)", size=9)
    s.write("delegacion.svg")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in (flujo, carpeta, herramientas, guardarrailes, delegacion):
        f()
    print("✓", ", ".join(p.name for p in sorted(OUT.glob("*.svg"))))
