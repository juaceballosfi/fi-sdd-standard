"""Genera el manual de fi-sdd-standard en PDF.

src/*.md (capítulos) → HTML con el FI Design System → PDF con Chromium (Playwright).
Dos pasadas: la primera mide en qué página empieza cada sección (marcadores del PDF) y la
segunda escribe esos números en el índice. La portada se renderiza aparte, sin pie de página.

    python build.py            # manual-fi-sdd-standard.pdf
    python build.py --html     # deja también build/manual.html para revisarlo
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

import markdown
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
ASSETS = ROOT / "assets"
BUILD = ROOT / "build"
OUT = ROOT / "manual-fi-sdd-standard.pdf"

from meta import DATE, SKILLS, VERSION  # noqa: E402  (versión del kit y fecha)
TITLE = "fi-sdd-standard · Manual de uso"

# ---------------------------------------------------------------- contenedores
# :::tipo título opcional        → bloque con estilo (se pueden anidar)
# :::                            → cierra
ALERTS = {"note": "", "tip": "fi-alert--primary", "warn": "fi-alert--warning",
          "danger": "fi-alert--danger", "ok": "fi-alert--success", "neutral": "fi-alert--neutral"}
EXAMPLES = {"ask": "Lo que pides", "out": "Lo que responde", "cmd": "Comando", "file": "Archivo"}


def containers(text: str) -> str:
    out, stack, fence = [], [], None
    raw: list[str] | None = None  # contenido de un ejemplo: si no trae bloque de código, se envuelve
    for line in text.splitlines():
        s = line.strip()
        if raw is not None:
            if s == ":::":
                if not any(l.strip().startswith(("```", "~~~")) for l in raw):
                    raw = ["```text", *raw, "```"]
                out.extend(raw)
                out.extend(["", stack.pop(), ""])
                raw = None
            else:
                raw.append(line)
            continue
        m = re.match(r"^(```+|~~~+)", s)
        if m:
            if fence is None:
                fence = m.group(1)
            elif s.startswith(fence):
                fence = None
            out.append(line)
            continue
        if fence is None and s.startswith("@@figure "):
            name, _, caption = s[9:].partition("|")
            svg = " ".join((SRC / "fig" / name.strip()).read_text(encoding="utf-8").split())
            cap = f"<figcaption>{html.escape(caption.strip())}</figcaption>" if caption.strip() else ""
            out.extend(["", f"<figure>{svg}{cap}</figure>", ""])
            continue
        if fence is None and s.startswith(":::"):
            spec = s[3:].strip()
            if not spec:
                out.extend(["", stack.pop(), ""])
                continue
            kind, _, label = spec.partition(" ")
            label = label.strip()
            if kind in ALERTS:
                title = f'<span class="fi-alert__title">{html.escape(label)}</span>' if label else ""
                out.extend(["", f'<div class="fi-alert {ALERTS[kind]}" markdown="1">', '<div class="fi-alert__content" markdown="1">', "", title, ""])
                stack.append("</div>\n</div>")
            elif kind in EXAMPLES:
                out.extend(["", f'<div class="ex {kind}" markdown="1">',
                            f'<div class="ex-label">{html.escape(label or EXAMPLES[kind])}</div>', ""])
                stack.append("</div>")
                raw = []
            elif kind == "view":
                out.extend(["", '<div class="ex view" markdown="1">',
                            f'<div class="ex-label">{html.escape(label)}</div>', ""])
                stack.append("</div>")
            elif kind == "card":
                out.extend(["", '<div class="card-skill" markdown="1">', ""])
                stack.append("</div>")
            elif kind in ("grid2", "grid3"):
                out.extend(["", f'<div class="{kind}" markdown="1">', ""])
                stack.append("</div>")
            elif kind in ("tile", "tile-accent"):
                cls = "tile accent" if kind == "tile-accent" else "tile"
                head = f"<h4>{html.escape(label)}</h4>" if label else ""
                out.extend(["", f'<div class="{cls}" markdown="1">', head, ""])
                stack.append("</div>")
            elif kind == "lead":
                out.extend(["", '<div class="fi-lead" markdown="1">', ""])
                stack.append("</div>")
            elif kind == "avoid":
                out.extend(["", '<div class="avoid" markdown="1">', ""])
                stack.append("</div>")
            else:
                raise SystemExit(f"contenedor desconocido: {kind}")
            continue
        out.append(line)
    if stack:
        raise SystemExit(f"contenedor sin cerrar ({len(stack)})")
    return "\n".join(out)


# ---------------------------------------------------------------- capítulos
def render_chapters() -> tuple[str, list[dict]]:
    files = sorted(SRC.glob("[0-9][0-9]-*.md"))
    if not files:
        raise SystemExit("no hay capítulos en src/")
    md = markdown.Markdown(extensions=["tables", "fenced_code", "md_in_html", "attr_list", "sane_lists"])
    sections, toc = [], []
    for n, f in enumerate(files, start=1):
        md.reset()
        body = md.convert(containers(f.read_text(encoding="utf-8")))
        soup = BeautifulSoup(body, "html.parser")
        h1 = soup.find("h1")
        if h1 is None:
            raise SystemExit(f"{f.name}: falta el título (# …)")
        annex = f.name.startswith("9")
        label = f"Anexo" if annex else f"Capítulo {n}"
        title = h1.get_text(strip=True)
        cid = f"c{n}"
        h1["id"] = cid
        h1["class"] = "ch"
        head = soup.new_tag("div", attrs={"class": "ch-head"})
        over = soup.new_tag("div", attrs={"class": "fi-overline"})
        over.string = label
        h1.insert_before(head)
        head.append(over)
        head.append(h1.extract())
        lead = soup.find("div", class_="fi-lead")
        if lead is not None:
            head.append(lead.extract())
        toc.append({"level": 1, "id": cid, "num": "" if annex else str(n), "title": title})
        for m, h2 in enumerate(soup.find_all("h2"), start=1):
            text = h2.get_text(strip=True)
            h2["id"] = f"{cid}-{m}"
            num = soup.new_tag("span", attrs={"class": "num"})
            num.string = f"{n}.{m}" if not annex else f"A.{m}"
            h2.insert(0, num)
            num.insert_after(" ")
            toc.append({"level": 2, "id": h2["id"], "num": num.string, "title": text})
        for table in soup.find_all("table"):
            classes = table.get("class", [])
            table["class"] = ["fi-table"] + [c for c in classes if c != "fi-table"]
            if table.parent.name != "div" or "fi-table-wrap" not in table.parent.get("class", []):
                table.wrap(soup.new_tag("div", attrs={"class": "fi-table-wrap"}))
        sections.append(f'<section class="chapter" id="s{n}">{soup}</section>')
    return "\n".join(sections), toc


# Página vacía que ocupa el lugar de la portada: así el pie numera igual que el visor de PDF.
PLACEHOLDER = '<div style="break-after: page; height: 10mm"></div>'


def toc_html(toc: list[dict], pages: dict[str, int]) -> str:
    rows = []
    for e in toc:
        p = pages.get(e["id"], 0)
        num = f'<span class="tnum">{e["num"]}</span> ' if e["num"] else ""
        rows.append(
            f'<li class="l{e["level"]}"><a href="#{e["id"]}" class="t">{num}{html.escape(e["title"])}</a>'
            f'<span class="dots"></span><span class="p">{p or "00"}</span></li>')
    return ('<section class="toc"><div class="ch-head"><div class="fi-overline">Contenido</div>'
            '<h1 class="ch toc-title">Índice</h1></div><ol>' + "\n".join(rows) + "</ol></section>")


def page_html(body: str, *, cover: bool = False) -> str:
    css = (ASSETS / "fi-design-system.css").read_text(encoding="utf-8")
    manual = (ASSETS / "manual.css").read_text(encoding="utf-8")
    return f"""<!doctype html>
<html lang="es" data-fi-theme="light"><head><meta charset="utf-8">
<title>{TITLE}</title>
<base href="{ASSETS.as_uri()}/">
<style>{css}</style><style>{manual}</style>
</head><body class="{'is-cover' if cover else 'is-body'}">{body}</body></html>"""


def cover_html() -> str:
    art = (SRC / "cover-art.svg").read_text(encoding="utf-8") if (SRC / "cover-art.svg").exists() else ""
    return page_html(f"""
<div class="cover">
  <div class="fi-overline">FI GROUP · fi-sdd-standard</div>
  <h1>Manual de <strong>uso</strong></h1>
  <p class="lead">Cómo trabajar un work item con IA, de <code>story.md</code> al PR: el flujo SDD,
  sus skills, subagentes, plantillas, scripts y guardarraíles, para desarrollo y QA.</p>
  <div class="badges">
    <span class="fi-badge fi-badge--primary fi-badge--pill">Desarrollo</span>
    <span class="fi-badge fi-badge--info fi-badge--pill">QA</span>
    <span class="fi-badge fi-badge--success fi-badge--pill">Tech lead</span>
  </div>
  <div class="cover-art">{art}</div>
  <div class="meta"><dl>
    <dt>Versión del kit</dt><dd>{VERSION} (candidata a MVP)</dd>
    <dt>Skills</dt><dd>v{SKILLS} · 9 skills · 7 subagentes</dd>
    <dt>Herramientas</dt><dd>Claude Code · GitHub Copilot (VS Code y Visual Studio) · Codex</dd>
    <dt>Fecha</dt><dd>{DATE}</dd>
    <dt>Responsables</dt><dd>Juan Clavijo · Juan Ceballos</dd>
  </dl></div>
</div>""", cover=True)


def footer_template() -> str:
    # El pie se dibuja en un contexto aparte: sin las fuentes web de la página ni sus variables.
    return f"""<div style="font-family:'Jost','DejaVu Sans',sans-serif;font-size:7pt;color:#5c5d74;width:100%;
padding:0 17mm;display:flex;justify-content:space-between;align-items:center;letter-spacing:0.04em;
-webkit-print-color-adjust:exact;">
<span><span style="display:inline-block;width:5mm;height:0.7mm;background:#efac14;border-radius:1mm;
vertical-align:middle;margin-right:2mm"></span>{TITLE} · v{VERSION}</span>
<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>"""


def render_pdf(page, html_text: str, out: Path, *, footer: bool) -> None:
    tmp = BUILD / (out.stem + ".html")
    tmp.write_text(html_text, encoding="utf-8")
    page.goto(tmp.as_uri())
    page.wait_for_load_state("networkidle")
    page.evaluate("document.fonts.ready")
    opts = dict(path=str(out), format="A4", print_background=True, outline=True, tagged=True)
    if footer:
        opts.update(display_header_footer=True, header_template="<span></span>",
                    footer_template=footer_template(),
                    margin={"top": "18mm", "bottom": "17mm", "left": "17mm", "right": "17mm"})
    else:
        opts.update(margin={"top": "0", "bottom": "0", "left": "0", "right": "0"}, prefer_css_page_size=True)
    page.pdf(**opts)


def outline_pages(pdf: Path) -> list[tuple[str, int]]:
    reader = PdfReader(str(pdf))
    found: list[tuple[str, int]] = []

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                found.append((it.title or "", reader.get_destination_page_number(it) + 1))
    walk(reader.outline)
    return found


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def match_pages(toc: list[dict], outline: list[tuple[str, int]]) -> dict[str, int]:
    pages, i = {}, 0
    for e in toc:
        want = norm(e["title"])
        for j in range(i, len(outline)):
            if norm(outline[j][0]).endswith(want):
                pages[e["id"]] = outline[j][1]
                i = j + 1
                break
    return pages


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", action="store_true")
    args = ap.parse_args()
    BUILD.mkdir(exist_ok=True)
    chapters, toc = render_chapters()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        render_pdf(page, cover_html(), BUILD / "cover.pdf", footer=False)
        pages: dict[str, int] = {}
        for pass_ in (1, 2):
            body = PLACEHOLDER + toc_html(toc, pages) + chapters
            render_pdf(page, page_html(body), BUILD / "body.pdf", footer=True)
            new = match_pages(toc, outline_pages(BUILD / "body.pdf"))
            missing = [e["title"] for e in toc if e["id"] not in new]
            if missing:
                print("aviso: sin página en el índice:", missing[:5], file=sys.stderr)
            if new == pages:
                break
            pages = new
        else:
            body = PLACEHOLDER + toc_html(toc, pages) + chapters
            render_pdf(page, page_html(body), BUILD / "body.pdf", footer=True)
        browser.close()

    writer = PdfWriter()
    writer.append(str(BUILD / "cover.pdf"), import_outline=False)
    body_pages = len(PdfReader(str(BUILD / "body.pdf")).pages)
    writer.append(str(BUILD / "body.pdf"), pages=list(range(1, body_pages)))  # la 1 es el hueco de la portada
    writer.add_metadata({"/Title": TITLE, "/Author": "Juan Clavijo, Juan Ceballos · FI GROUP",
                         "/Subject": f"Manual de uso del kit fi-sdd-standard v{VERSION}",
                         "/Keywords": "SDD, IA, Claude Code, GitHub Copilot, Azure DevOps"})
    writer.page_mode = "/UseOutlines"
    with open(OUT, "wb") as fh:
        writer.write(fh)
    n = len(PdfReader(str(OUT)).pages)
    print(f"✓ {OUT.name} · {n} páginas · {len(toc)} entradas en el índice")
    if not args.html:
        for f in BUILD.glob("*.html"):
            f.unlink()


if __name__ == "__main__":
    main()
