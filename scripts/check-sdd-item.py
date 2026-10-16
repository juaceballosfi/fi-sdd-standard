#!/usr/bin/env python3
"""Check the SDD artifacts of one work item folder, without AI (deterministic).

Usage:
    python scripts/check-sdd-item.py <project>/docs/sdd/<id>-<title>
    python scripts/check-sdd-item.py --commit-message <file> --id <id>

It reports which step the work item has reached and whether each artifact follows the standard:
story.md prepared by a person with its assets (ADR-0015),
stamps, anchors, unresolved markers, the working log and the commit message format (ADR-0004).
Attachments and commit-message.md are not committed (ADR-0027): a missing attachment that git
ignores is a warning, and a folder already committed with `Ref: #<id>` counts as step 5.
Exit code 0 = no errors (warnings allowed), 1 = errors. Reused later by the PR validation pipeline.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote

COMMIT_TYPES = "feat|fix|refactor|perf|docs|test|chore|ci|style|revert"
FOLDER_RE = re.compile(r"^(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*$")
# Only the marker form with ":" counts; "Secciones [ASSUMPTION-BASED]: Ninguna" in 00 is a summary line.
BLOCKING_MARKERS = ("[ASSUMPTION-BASED:", "[PENDING-TRANSLATION:")
PLACEHOLDER = re.compile(r"<([^<>\n!]{1,40})>")
HTML_TAGS = {"a", "b", "br", "code", "div", "em", "hr", "i", "img", "li", "ol", "p", "pre", "span", "strong",
             "sub", "sup", "table", "tbody", "td", "th", "thead", "tr", "u", "ul"}
MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\((<[^>]+>|[^)\s]+)(?:\s+\"[^\"]*\")?\)")
HTML_IMG = re.compile(r"<img[^>]*\ssrc=\"([^\"]+)\"", re.I)
GENERIC_ALT = {"", "alt text", "alt", "image", "imagen", "img", "captura", "screenshot", "picture"}
GENERIC_FILE = re.compile(r"^(image|imagen|img|screenshot|captura|pasted[-_ ]?image|clipboard)[-_ ]?\(?\d*\)?\.\w+$", re.I)
ASSET_MAX_MB = 5
DESIGN_FILES = [
    ("00-executive-summary.md", "00-resumen-ejecutivo.md"),
    ("01-current-state-report.md", "01-reporte-estado-actual.md", "01-informe-estado-actual.md"),
    ("02-analysis-diagnosis.md", "02-analisis-diagnostico.md"),
    ("03-solution-proposal.md", "03-propuesta-solucion.md"),
    ("04-implementation-plan.md", "04-plan-implementacion.md"),
    ("05-wbs-estimation.md", "05-wbs-estimacion.md"),
    ("06-risks-mitigations.md", "06-riesgos-y-mitigaciones.md"),
]


def git(folder: Path, *args: str) -> subprocess.CompletedProcess | None:
    try:
        return subprocess.run(["git", "-C", str(folder), *args], capture_output=True, text=True,
                              encoding="utf-8", errors="replace")
    except OSError:
        return None


def git_ignored(folder: Path, path: Path) -> bool:
    """True when git ignores the path (ADR-0027: attachments stay out of the repository)."""
    out = git(folder, "check-ignore", "-q", "--no-index", str(path))
    return out is not None and out.returncode == 0


def last_commit_message(folder: Path, item_id: str | None) -> tuple[str, str] | None:
    """The latest commit that touched the folder and links the work item with Ref: #<id>."""
    if not item_id:
        return None
    out = git(folder, "log", "-1", "--format=%h%x00%B", f"--grep=^Ref: #{item_id}$", "--", ".")
    if out is None or out.returncode != 0 or "\x00" not in out.stdout:
        return None
    sha, body = out.stdout.split("\x00", 1)
    return sha.strip(), body.strip() + "\n"


class Report:
    def __init__(self) -> None:
        self.rows: list[tuple[str, str, str]] = []

    def ok(self, what: str, detail: str = "") -> None:
        self.rows.append(("✓", what, detail))

    def warn(self, what: str, detail: str) -> None:
        self.rows.append(("⚠", what, detail))

    def err(self, what: str, detail: str) -> None:
        self.rows.append(("✗", what, detail))

    def info(self, what: str, detail: str) -> None:
        """Not a problem: a step that has not been done yet."""
        self.rows.append(("○", what, detail))

    @property
    def errors(self) -> int:
        return sum(1 for s, _, _ in self.rows if s == "✗")

    def print(self) -> None:
        for status, what, detail in self.rows:
            print(f"  {status} {what}" + (f" — {detail}" if detail else ""))


def check_commit_message(text: str, item_id: str | None, r: Report) -> None:
    if re.search(r"â€|Ã[\xa0-\xbf]|ÔÇ|├[\xa0-\xbf]", text):
        r.warn("commit: codificación", "el texto parece mal decodificado (tildes o «—» estropeadas). Si lo sacaste "
               "con `git log … > archivo` en PowerShell, usa: cmd /c \"git log -1 --format=%B > %TEMP%\\msg.txt\"")
    lines = text.replace("\r\n", "\n").rstrip("\n").split("\n")
    first = lines[0] if lines else ""
    m = re.fullmatch(rf"({COMMIT_TYPES})(\([a-z0-9._/-]+\))?: (\S.*)", first)
    if m:
        r.ok("commit: primera línea tipo(ámbito): descripción")
        if m.group(3)[0].isupper():
            r.warn("commit: primera línea", "la descripción va en minúscula")
    else:
        r.err("commit: primera línea", f"no sigue tipo(ámbito): descripción → «{first[:80]}»")
    if len(first) > 72:
        r.err("commit: primera línea", f"{len(first)} caracteres (máximo 72)")
    if first.endswith("."):
        r.err("commit: primera línea", "termina en punto")
    if len(lines) > 1 and lines[1].strip():
        r.err("commit: segunda línea", "debe quedar en blanco")
    if any(l.startswith("#") for l in lines):
        r.err("commit: encabezados", "hay líneas que empiezan por # (git las borra): usa rótulos en negrita")
    if not re.search(r"^(PBI|BUG)-\d+ — ", text, re.M):
        r.warn("commit: título del ticket", "falta la línea «PBI-XXXXX — [MÓDULO] Título»")
    refs = re.findall(r"^Ref: #(\d+)\s*$", text, re.M)
    if not refs and m and m.group(1) in ("docs", "chore", "ci", "style"):
        r.warn("commit: Ref", "sin «Ref: #<id>»: vale para docs/chore/ci/style sin work item; la política del PR puede pedir enlazarlo")
    elif not refs:
        r.err("commit: Ref", "falta la línea «Ref: #<id>»")
    elif item_id and item_id not in refs:
        r.err("commit: Ref", f"enlaza #{', #'.join(refs)} y la carpeta es del #{item_id}")
    else:
        r.ok("commit: Ref: #" + refs[0])
    if re.search(r"^(Co-Authored-By|Generated with|🤖)", text, re.M | re.I):
        r.err("commit: firma de IA", "quita las líneas Co-Authored-By / Generated with: el sello SDD es la evidencia (ADR-0004)")
    if re.search(r"\b(fix|fixes|fixed|close|closes|closed|resolve|resolves|resolved)\s+#\d+", text, re.I):
        r.err("commit: cierre automático", "no uses fix/fixes/fixed #id: Azure Repos cerraría el work item")
    size = len(text)
    if size >= 4000:
        r.err("commit: tamaño", f"{size} caracteres (máximo 3999, se reutiliza como descripción del PR)")
    else:
        r.ok("commit: tamaño", f"{size} caracteres")


def suggested_name(name: str) -> str | None:
    """Same slug rule as new-sdd-item.py and enrich-us."""
    m = re.match(r"^(\d+)-(.+)$", name)
    if not m:
        return None
    text = unicodedata.normalize("NFKD", m.group(2)).encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    if len(slug) > 40:
        cut = slug[:41]
        slug = cut[:cut.rfind("-")] if "-" in cut else slug[:40]
    return f"{m.group(1)}-{slug.strip('-')}" if slug else None


def find(folder: Path, names: tuple[str, ...]) -> Path | None:
    for n in names:
        if (folder / n).exists():
            return folder / n
    return None


def has_stamp(text: str, skill: str) -> bool:
    return re.search(rf"\*\*Generado con:\*\* {skill} v[\d.]+", text) is not None


def sections(text: str) -> dict[str, str]:
    """'## Heading' -> body text (stripped)."""
    parts = re.split(r"^## +(.+?)\s*$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1].strip() for i in range(1, len(parts) - 1, 2)}


def check_story(folder: Path, s: str, item_id: str | None, r: Report) -> None:
    """story.md is prepared by a person (ADR-0015): complete header, literal sections, valid assets."""
    body = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    plain = re.sub(r"`[^`\n]*`", "", re.sub(r"^```.*?^```", "", body, flags=re.S | re.M))

    by = re.search(r"\*\*Preparado por:\*\*\s*([^·\n]+)", body)
    if by and "<" not in by.group(1):
        r.ok("story.md", f"preparado por {by.group(1).strip()}")
    elif has_stamp(s, "enrich-us"):
        r.warn("story.md", "lo escribió enrich-us (forma anterior a v3.1): revisa que sea copia literal")
    else:
        r.err("story.md", "falta «**Preparado por:** <persona>» (ADR-0015)")
    for label in ("**Fuente:** Azure DevOps", "**Leído:**", "## Criterios de aceptación"):
        if label not in body:
            r.err("story.md", f"falta «{label}»")
    if "## Descripción" not in body and "## Pasos para reproducir" not in body:
        r.err("story.md", "falta «## Descripción» (o «## Pasos para reproducir» en un bug)")
    if item_id and f"Work item {item_id}" not in body:
        r.warn("story.md", f"el título no menciona «Work item {item_id}»")

    placeholders = []
    for m in PLACEHOLDER.finditer(plain):
        first = m.group(1).strip().lstrip("/").split(" ")[0].lower()
        if first not in HTML_TAGS and not first.startswith(("http", "mailto")) and m.group(0) not in placeholders:
            placeholders.append(m.group(0))
    if placeholders:
        shown = ", ".join(placeholders[:6]) + (" …" if len(placeholders) > 6 else "")
        r.warn("story.md", f"{len(placeholders)} campo(s) sin rellenar: {shown}")
    not_copied = body.count("No incluido en el texto pegado")
    if not_copied:
        r.warn("story.md", f"«No incluido en el texto pegado» en {not_copied} sitio(s): si Azure DevOps no tiene ese "
                           "campo, escribe «Sin <campo> en el work item»; si no se copió, cópialo")

    secs = sections(body)
    desc = secs.get("Descripción", secs.get("Pasos para reproducir", ""))
    if not desc or PLACEHOLDER.fullmatch(desc):
        r.err("story.md", "la descripción está vacía o sin rellenar")
    if not secs.get("Criterios de aceptación"):
        r.warn("story.md", "criterios de aceptación vacíos: si no hay, escribe «Sin criterios de aceptación en el work item»")
    origin = re.search(r"[Cc]opied .*?from #(\d+)|[Cc]opiado .*?de #(\d+)", body)
    if origin:
        src = origin.group(1) or origin.group(2)
        if f"#{src}" in secs.get("Enlaces", ""):
            r.ok("story.md", f"viene del #{src}, que está en «Enlaces»; lo que haga falta de él debe estar copiado aquí")
        else:
            r.warn("story.md", f"viene copiado del #{src}: añádelo a «Enlaces» y copia aquí lo que haga falta de él "
                               "(la IA solo lee este archivo)")

    linked: set[Path] = set()
    links = [(m.group(1) == "!", m.group(2), m.group(3)) for m in MD_LINK.finditer(body)]
    links += [(True, "", m.group(1)) for m in HTML_IMG.finditer(body)]
    for is_image, alt, target in links:
        target = unquote(target.strip("<>"))
        if target.startswith(("http://", "https://", "mailto:", "#")) or "<" in target:
            continue  # external link, or a template placeholder already reported above
        path = (folder / target.split("#")[0]).resolve()
        if not path.exists():
            if git_ignored(folder, path):
                r.warn("story.md", f"{target} no está en este equipo (los adjuntos no se versionan, ADR-0027): "
                       "bájalo del work item en Azure DevOps con ese nombre")
            else:
                r.err("story.md", f"enlace roto: {target}")
            continue
        linked.add(path)
        if folder.resolve() not in path.parents:
            r.warn("story.md", f"{target} está fuera de la carpeta del work item: muévelo a assets/")
        if is_image and alt.strip().lower() in GENERIC_ALT:
            r.warn("story.md", f"la imagen {path.name} no tiene texto alternativo útil: di qué muestra")
        if GENERIC_FILE.match(path.name):
            r.warn("story.md", f"{path.name}: usa un nombre descriptivo (p. ej. {item_id or '<id>'}-menu-lateral.png)")
    assets = folder / "assets"
    files = [f for f in assets.rglob("*") if f.is_file() and f.name != ".gitkeep"] if assets.is_dir() else []
    for f in files:
        if f.resolve() not in linked:
            r.warn("story.md", f"assets/{f.relative_to(assets).as_posix()} no está enlazado en story.md")
        size_mb = f.stat().st_size / 1_048_576
        if size_mb > ASSET_MAX_MB:
            r.warn("assets", f"{f.name} pesa {size_mb:.1f} MB: ¿hace falta entero en el repositorio?")
    if linked and not secs.get("Adjuntos"):
        r.warn("story.md", "describe en «Adjuntos» qué muestra cada imagen o archivo (no todas las herramientas ven imágenes)")
    if linked or files:
        r.ok("adjuntos", f"{len(linked)} enlazado(s) · {len(files)} en assets/")


QA_ROW = re.compile(r"^\|\s*(QA-\d+)\s*\|\s*([^|]*)\|(?:[^|]*\|){3}\s*([^|]*)\|\s*$", re.M)
QA_DECIDED = ("corregido", "aceptado", "descartado", "borrador")


def check_qa_report(t: str, r: Report) -> int:
    """qa-report.md (qa-review): stamp and findings still open. Returns open high/medium findings."""
    r.ok("qa-report.md") if has_stamp(t, "qa-review") else r.warn("qa-report.md", "sin sello «Generado con: qa-review»")
    rows = [(i, sev.strip(), state.strip()) for i, sev, state in QA_ROW.findall(t) if not sev.strip().startswith("Alta /")]
    blocking = [i for i, sev, state in rows
                if sev.lower().startswith(("alta", "media")) and not state.lower().startswith(QA_DECIDED)]
    low_open = [i for i, sev, state in rows if i not in blocking and not state.lower().startswith(QA_DECIDED)]
    if blocking:
        r.err("qa-report.md", f"{len(blocking)} hallazgo(s) alto(s)/medio(s) sin decidir ({', '.join(blocking)}): "
                              "corrígelos (/wbs-execution <id> qa), acéptalos con nombre o descártalos con motivo")
    elif rows:
        r.ok("qa-report.md", f"{len(rows)} hallazgo(s), ninguno alto o medio abierto"
             + (f"; bajos abiertos: {', '.join(low_open)}" if low_open else ""))
    else:
        r.ok("qa-report.md", "sin hallazgos")
    return len(blocking)


def check_folder(folder: Path, r: Report) -> tuple[int, str]:
    m = FOLDER_RE.match(folder.name)
    item_id = m.group(1) if m else None
    if m and folder.parent.name == "sdd":
        r.ok("carpeta", f"docs/sdd/{folder.name}")
    else:
        expected = suggested_name(folder.name)
        hint = f": renómbrala a {expected}" if expected and expected != folder.name else " (¿ítem antiguo?)"
        r.warn("carpeta", f"no sigue docs/sdd/<id>-<título>, sin tildes ni mayúsculas{hint}")
        item_id = item_id or (re.match(r"(\d+)", folder.name).group(1) if re.match(r"\d+", folder.name) else None)
    step = -1
    open_markers = 0

    story = folder / "story.md"
    if story.exists():
        step = 0
        check_story(folder, story.read_text(encoding="utf-8"), item_id, r)
    else:
        r.err("story.md", "no existe: créalo con new-sdd-item.py y cópialo desde Azure DevOps (ADR-0015)")

    log = folder / "bitacora.md"
    if log.exists():
        b = log.read_text(encoding="utf-8")
        r.ok("bitacora.md")
        if "<!-- sdd:log -->" not in b:
            r.warn("bitacora.md", "falta el ancla <!-- sdd:log -->")
        pending = [l for l in b.splitlines() if re.match(r"^\|\s*\d{4}-\d{2}-\d{2}\s*\|", l) and re.search(r"\|\s*No\s*\|\s*$", l)]
        if pending:
            r.err("bitacora.md", f"{len(pending)} decisión(es) sin pasar a pbi.md/bug.md")
    else:
        r.err("bitacora.md", "no existe")

    req = find(folder, ("pbi.md", "bug.md"))
    if req:
        t = req.read_text(encoding="utf-8")
        step = 1
        r.ok(req.name) if has_stamp(t, "enrich-us") or has_stamp(t, "quick-fix") else \
            r.warn(req.name, "sin sello «Generado con: enrich-us»")
        for anchor in ("sdd:acceptance-criteria", "sdd:pending", "sdd:i18n"):
            if f"<!-- {anchor} -->" not in t:
                r.err(req.name, f"falta el ancla <!-- {anchor} -->")
        pending = len(re.findall(r"\[PENDING-BUSINESS", t))
        if pending:
            r.warn(req.name, f"{pending} [PENDING-BUSINESS] sin resolver")
        open_rv = len(re.findall(r"\[REQUIRES-VALIDATION:", t))
        if open_rv:
            r.warn(req.name, f"{open_rv} [REQUIRES-VALIDATION] abierto(s): si ya se resolvió, quítalo también aquí")
        open_markers += pending + open_rv
    elif step >= 0:
        r.warn("pbi.md / bug.md", "todavía no existe (paso 1)")

    design = [find(folder, names) for names in DESIGN_FILES]
    present = [d for d in design if d]
    if present:
        step = 2
        missing = [names[0] for names, d in zip(DESIGN_FILES, design) if not d]
        if missing:
            r.err("diseño", "faltan " + ", ".join(missing))
        else:
            r.ok("diseño 00–06")
        for d in present:
            t = d.read_text(encoding="utf-8")
            if not has_stamp(t, "technical-analysis"):
                r.warn(d.name, "sin sello «Generado con: technical-analysis»")
            for marker in BLOCKING_MARKERS:
                n = t.count(marker)
                if n:
                    r.err(d.name, f"{n} {marker.rstrip(':')}] sin resolver")
            rv = len(re.findall(r"\[REQUIRES-VALIDATION:(?! motivo\])", t))
            if rv:
                r.warn(d.name, f"{rv} [REQUIRES-VALIDATION] abierto(s)")
                open_markers += rv
        for d in present:
            if d.name.startswith(("03-", "04-")):
                t = d.read_text(encoding="utf-8")
                if re.search(r"\*\*Estado:\*\*\s*Aprobado", t):
                    r.ok(f"{d.name} aprobado")
                else:
                    r.warn(d.name, "sin «Estado: Aprobado» (contrato pendiente de aprobar)")
        wbs = design[5]
        if wbs:
            t = wbs.read_text(encoding="utf-8")
            rows = re.findall(r"^\|\s*T-\d+.*$", t, re.M)  # task rows only, not the status legend
            done = sum(1 for row in rows if "✅ Hecha" in row)
            total = len(rows)
            if total:
                r.ok("WBS", f"{done}/{total} tareas hechas")
                if done == total:
                    step = 3

    fix = folder / "fix-plan.md"
    if fix.exists() and not present:
        step = 2
        t = fix.read_text(encoding="utf-8")
        r.ok("fix-plan.md (vía rápida)") if has_stamp(t, "quick-fix") else r.warn("fix-plan.md", "sin sello «Generado con: quick-fix»")
        for anchor in ("sdd:fix-gate", "sdd:fix-cause", "sdd:fix-tests", "sdd:tasks"):
            if f"<!-- {anchor} -->" not in t:
                r.err("fix-plan.md", f"falta el ancla <!-- {anchor} -->")
        gate = t.split("<!-- sdd:fix-gate -->", 1)[-1].split("##", 1)[0]
        if re.search(r"^\|[^|\n]+\|\s*✗", gate, re.M):
            r.err("fix-plan.md", "un criterio de la vía rápida no se cumple: el ítem va al flujo completo")
        if not re.search(r"\*\*Estado:\*\*\s*Aprobado", t):
            r.warn("fix-plan.md", "sin «Estado: Aprobado»")
        rows = re.findall(r"^\|\s*T-\d+.*$", t, re.M)
        if rows and all("✅ Hecha" in row for row in rows):
            step = 3
            r.ok("tarea de la vía rápida hecha")

    changelog = folder / "CHANGELOG.md"
    documented = False
    if changelog.exists():
        t = changelog.read_text(encoding="utf-8")
        r.ok("CHANGELOG.md") if has_stamp(t, "wbs-execution") or has_stamp(t, "quick-fix") else \
            r.warn("CHANGELOG.md", "sin sello «Generado con: wbs-execution»")
        documented = re.search(r"^##.*Documentaci[oó]n", t, re.M) is not None

    qa = folder / "qa-report.md"
    qa_open = 0
    if qa.exists():
        step = max(step, 4)
        qa_open = check_qa_report(qa.read_text(encoding="utf-8"), r)
    elif step >= 3:
        r.info("qa-report.md", "sin revisión de QA: /qa-review <id> en una sesión nueva (paso 4)")

    if (changelog.exists() or (folder / "commit-message.md").exists()) and not present and not fix.exists():
        r.warn("diseño", "hay CHANGELOG o commit pero no los documentos 00–06 (¿vía rápida o se saltó el paso 2?)")

    if documented:
        r.ok("documentación", "entrada «Documentación» en CHANGELOG.md (document-code)")
    elif step >= 3:
        r.info("documentación", "sin documentar: /document-code <id> (paso 5)")

    commit = folder / "commit-message.md"
    # Once the folder is committed, the commit is what counts; before that, commit-message.md.
    committed = last_commit_message(folder, item_id) if step >= 1 else None
    if committed:
        step = max(step, 5)
        r.ok("commit", f"{committed[0]} enlaza #{item_id} (commit-message.md no se versiona, ADR-0027)")
        check_commit_message(committed[1], item_id, r)
    elif commit.exists():
        step = max(step, 5)
        check_commit_message(commit.read_text(encoding="utf-8"), item_id, r)

    names = {-1: "sin empezar", 0: "0 · story.md", 1: "1 · enriquecido", 2: "2 · diseñado",
             3: "3 · implementado", 4: "4 · revisado por QA", 5: "5 · listo para commit"}
    label = names[step]
    if step == 5:
        blockers = []
        if r.errors:
            blockers.append(f"{r.errors} error(es)")
        if open_markers:
            blockers.append(f"{open_markers} marcador(es) abierto(s)")
        if qa_open:
            blockers.append(f"{qa_open} hallazgo(s) de QA sin decidir")
        if blockers:
            where = f"en el commit {committed[0]}" if committed else "commit-message.md escrito"
            label = f"5 · {where}, pero no listo: " + ", ".join(blockers)
        elif committed:
            label = f"5 · en el commit {committed[0]}" + ("" if qa.exists() else " (sin revisión de QA)")
        elif not qa.exists():
            label = "5 · listo para commit (sin revisión de QA)"
    return step, label


def read_any_text(path: Path) -> str:
    """UTF-8 (with or without BOM) or UTF-16: PowerShell 5.1 writes UTF-16 with `>`."""
    data = path.read_bytes()
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        return data.decode("utf-16")
    return data.decode("utf-8-sig")


def main() -> int:
    parser = argparse.ArgumentParser(description="Comprueba los artefactos SDD de un work item")
    parser.add_argument("folder", nargs="?", type=Path, help="docs/sdd/<id>-<título>")
    parser.add_argument("--commit-message", type=Path, help="Comprueba solo un mensaje de commit")
    parser.add_argument("--id", help="ID del work item (con --commit-message)")
    args = parser.parse_args()
    r = Report()
    if args.commit_message:
        check_commit_message(read_any_text(args.commit_message), args.id, r)
        print(f"\nMensaje de commit: {args.commit_message}\n")
    elif args.folder and args.folder.is_dir():
        _, label = check_folder(args.folder.resolve(), r)
        print(f"\nWork item: {args.folder.name} · paso alcanzado: {label}\n")
    else:
        parser.print_help()
        return 2
    r.print()
    warnings = sum(1 for s, _, _ in r.rows if s == "⚠")
    print(f"\n  {r.errors} errores · {warnings} avisos\n")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main())
