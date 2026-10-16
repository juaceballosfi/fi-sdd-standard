# Plan de documentación — <repositorio>

**Generado con:** document-project v3.8 · [Claude Code | GitHub Copilot | Codex] · [modelo]
**Creado:** AAAA-MM-DD · **Work item:** #<ID> | ninguno · **Kit:** v<versión>
**Línea base (AAAA-MM-DD):** código N/M símbolos documentados (P %) · pruebas N/M clases con resumen ·
CS1591: N | sin `GenerateDocumentationFile` · build: N avisos · lint: N avisos · tipos: N errores ·
DocFX: N avisos | no instalado | no hay sitio

## Cómo se trabaja

- Un bloque por sesión, en una sesión nueva: `/document-project` toma el siguiente bloque pendiente;
  `/document-project block:B-03` o `area:A-07` eligen uno; `/document-project status` solo informa.
- Un bloque es un commit y un PR. El registro de cada bloque está en `B-NN.md`, junto a este plan.
- Solo cambian comentarios y `docs/`: `comment_only.py` lo comprueba en cada bloque.
- Lo que el código o un documento no dicen no se escribe: queda en *Sin documentar* del bloque.

## Áreas
<!-- sdd:doc-areas -->

[Estado: Pendiente · En curso · Hecha (AAAA-MM-DD) · Revisar (motivo). «Sin documentar» se mide con
`doc_coverage.py` sobre los archivos del área: antes del bloque → después.]

| ID | Área | Tipo | Archivos | Pruebas | docs/ | Sin documentar | Bloque | Estado |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | <nombre> | transversal · backend · frontend | N | N | <archivos de docs/ que toca> | N/M → – | B-01 | Pendiente |

## Bloques
<!-- sdd:doc-blocks -->

| Bloque | Áreas | Archivos | Registro | PR | Estado |
| --- | --- | --- | --- | --- | --- |
| B-01 | A-01, A-02 | N | B-01.md | – | Pendiente |

## Hallazgos
<!-- sdd:doc-findings -->

[Lo que se ve al documentar y no se corrige aquí: comportamiento dudoso, código muerto, documentación
que contradice el código. Una línea por hallazgo; los que merecen un work item van a
`docs/sdd/_borradores/`. Solo crece.]

- AAAA-MM-DD · B-NN · `<archivo:línea>` · <qué se vio> · <_borradores/<slug>.md | solo anotado>

## Registro
<!-- sdd:log -->

- AAAA-MM-DD · document-project · plan creado: N áreas en M bloques

## Archivos por área

[Una subsección por área con sus archivos de código y de pruebas. Se lee solo la del área en curso.]

### A-01 · <nombre>

- `<ruta>`
- prueba: `<ruta>`
