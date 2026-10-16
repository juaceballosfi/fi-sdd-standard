# Manual de uso de fi-sdd-standard

| Archivo | Para qué |
| --- | --- |
| `manual-fi-sdd-standard.pdf` | El manual para leer o imprimir, con el FI Design System |
| `manual-fi-sdd-standard.md` | El mismo contenido en un solo Markdown, con instrucciones para una IA al principio y preguntas frecuentes al final: se puede dar de contexto a un asistente que ayude al equipo |

El manual vive solo en el repositorio del kit: `install.py` no lo copia a los proyectos (ADR-0027).

## Regenerarlo

Las fuentes son los capítulos de `src/` (Markdown con bloques propios: `:::` para ejemplos, avisos y
fichas, y `@@figure` para los diagramas). La versión del kit, la de las skills y la fecha salen de
`meta.py` (lee `VERSION` y el sello de `enrich-us`).

```bash
pip install markdown beautifulsoup4 pypdf playwright   # y un Chromium para Playwright
python diagrams.py      # src/fig/*.svg, si cambian los diagramas
python build.py         # manual-fi-sdd-standard.pdf (dos pasadas: índice con páginas y marcadores)
python build_md.py      # manual-fi-sdd-standard.md
```

`build/` es temporal y no se versiona. Cuando cambia un comportamiento del kit, el capítulo que lo
explica se actualiza en el mismo PR y se regeneran los dos archivos.

| Fuente | Contenido |
| --- | --- |
| `src/01-…md` a `src/18-…md`, `src/90-adr.md` | Los capítulos y el anexo de ADR |
| `src/md-intro.md`, `src/md-faq.md` | Solo para el Markdown: instrucciones para la IA y preguntas frecuentes |
| `src/cover-art.svg`, `src/fig/` | Portada y diagramas (`fig/` lo genera `diagrams.py`) |
| `assets/` | `fi-design-system.css`, `manual.css` (capa de impresión) y las fuentes Jost y JetBrains Mono |
