# Marcadores, sellos, anclas y bitácora

:::lead
Son las convenciones que permiten que nueve skills distintas, en herramientas distintas, se
entiendan entre sí y que una persona sepa en todo momento qué está confirmado y qué no. Están en el
bloque *Shared SDD conventions*, idéntico en todas las skills.
:::

## Marcadores

Un marcador señala un hueco que la IA **no puede rellenar por su cuenta**. Mientras exista, el
documento no está cerrado.

| Marcador | Significa | Ejemplo | Lo resuelve |
| --- | --- | --- | --- |
| `[PENDING-BUSINESS: <pregunta>]` | Falta información de negocio que solo una persona puede dar | `[PENDING-BUSINESS: ¿cuántos días de antelación como máximo?]` | El PO o quien tenga la respuesta |
| `[REQUIRES-VALIDATION: <motivo>]` | Una afirmación técnica sin evidencia directa en el código | `[REQUIRES-VALIDATION: no se ve si el job se ejecuta en producción]` | Un dev, con un comando, una pantalla o una persona |
| `[ASSUMPTION-BASED: <campo>]` | Una sección construida encima de un campo sin resolver | `[ASSUMPTION-BASED: límite de días]` en 03 §3.4 | Se resuelve al resolver el campo del que depende |
| `[PENDING-TRANSLATION: <clave> → <idioma>]` | Una traducción que la IA no puede dar con seguridad | `[PENDING-TRANSLATION: Offers → fr]` | Alguien con el idioma, o el PO decide dejarlo pendiente |

Dónde frenan:

- `technical-analysis` se para si `pbi.md` tiene `[PENDING-BUSINESS]` y te pregunta si sigues (las
  secciones afectadas saldrían `[ASSUMPTION-BASED]`).
- `wbs-execution` se para si el resumen ejecutivo lista `[ASSUMPTION-BASED]` o
  `[REQUIRES-VALIDATION]`.
- `quick-fix` no admite ningún `[PENDING-BUSINESS]`.
- `test-cases` deja Bloqueados los casos con un `[PENDING-BUSINESS]`.
- `wbs-execution` hace un **barrido** al cerrar: los resueltos se sustituyen por la decisión; los
  abiertos van al informe y a `commit-message.md`.

### Resolver un marcador

Cuando tengas la respuesta, díselo a la IA con quién la dio:

:::ask
El máximo son 30 días; lo confirmó Laura Gómez (PO) hoy.
:::

La IA quita el marcador **en todos los archivos de la carpeta** que lo tengan (incluido
`pbi.md`), escribe la respuesta en su lugar, registra quién la resolvió en `bitacora.md` y, al
final, te da el *Comentario para Azure DevOps*.

## Sello de trazabilidad

Cada archivo que genera la IA empieza su bloque de metadatos con:

```markdown
**Generado con:** enrich-us v3.10 · Claude Code · claude-opus-5-5
```

- `<skill> v<versión>`: la skill y la versión de las skills del kit.
- `<herramienta>`: `Claude Code`, `GitHub Copilot` o `Codex`.
- `<modelo>`: el de la sesión que ejecutó la skill (los de los subagentes los fija la versión del
  kit). Si la sesión no lo sabe, el modelo por defecto del equipo, `claude-opus-5-5`.

Es **la evidencia verificable** de que el documento lo produjo la IA, y por eso los commits no
llevan `Co-Authored-By` (ADR-0004). Nunca se borra. `story.md`, que lo prepara una persona, lleva
`**Preparado por:**` en su lugar.

Cuando una skill posterior cambia un documento con una decisión confirmada, añade debajo:

```markdown
**Actualizado con:** technical-analysis v3.10 · Claude Code · claude-opus-5-5 (2026-10-16: CA-03 añadido, aprobado por Laura Gómez)
```

## Anclas

Las anclas son comentarios HTML que marcan secciones: la skill siguiente busca el ancla, no el
título, así que funciona aunque el título cambie o esté en otro idioma.

| Ancla | Archivo | La lee |
| --- | --- | --- |
| `sdd:description` · `sdd:acceptance-criteria` · `sdd:pending` | `pbi.md`, `bug.md` | `technical-analysis`, `test-cases` |
| `sdd:qa-classification` | `pbi.md`, `bug.md` | `test-cases` |
| `sdd:i18n` | `pbi.md`, `bug.md`, `01` §1.8 | `technical-analysis`, `wbs-execution` |
| `sdd:markers` | `00` | `wbs-execution` |
| `sdd:specs` | `04` | `wbs-execution`, `qa-review`, `test-cases` |
| `sdd:tasks` · `sdd:task-log` | `05`, `fix-plan.md` | `wbs-execution`, `check-sdd-item.py` |
| `sdd:risks` | `06` | `wbs-execution`, `qa-review` |
| `sdd:fix-gate` · `sdd:fix-cause` · `sdd:fix-tests` | `fix-plan.md` | `qa-review`, `check-sdd-item.py` |
| `sdd:qa-findings` | `qa-report.md` | `wbs-execution qa` |
| `sdd:test-cases` | `test-cases.md` | `test_cases_csv.py` |
| `sdd:log` | `bitacora.md`, `plan.md` | Todas |
| `sdd:doc-areas` · `sdd:doc-blocks` · `sdd:doc-findings` | `plan.md` | `document-project`, `doc_coverage.py` |
| `sdd:context` | *Project context* de `AGENTS.md` | `check_project.py` (fecha y fuentes) |
| `sdd-kit:base:start` / `end` | `AGENTS.md` | `install.py` |

:::danger No borres un ancla
Si editas un documento a mano, deja los comentarios `<!-- sdd:... -->` donde están.
`check-sdd-item.py` avisa si falta una.
:::

## La bitácora

`bitacora.md` es la memoria del work item. Cualquier persona que retome el trabajo (o una sesión
nueva) sabe qué se preguntó, qué se respondió y quién lo confirmó.

:::file bitacora.md
# Bitácora — 40399 Sección de ofertas en el menú lateral

**Generado con:** enrich-us v3.10 · Claude Code · claude-opus-5-5
**Work item:** #40399 · **Carpeta:** docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/

## Decisiones

| Fecha | Decisión | Confirmada por | En pbi.md |
| ----- | -------- | -------------- | --------- |
| 2026-10-15 | Ven la sección Comercial y Jefe de ventas | Laura Gómez | Sí |

## Preguntas abiertas

- [ ] 2026-10-15 · ¿Orden de las ofertas: por fecha ascendente o descendente? · para: PO

## Registro

<!-- sdd:log -->
- 2026-10-15 · Ana Pérez · carpeta creada; story.md preparado a partir del work item
- 2026-10-15 · enrich-us · story.md leído · adjuntos revisados: 1 de 1 · huecos: 0
- 2026-10-15 · enrich-us · pbi.md generado · pendientes: 0
- 2026-10-15 · technical-analysis · diseño 00–06 generado · 4 SP · 2 tareas

## Hallazgos

- 2026-10-15 · technical-analysis · SideMenu.tsx:30 — «Inicio» sin i18n (deuda previa, fuera de alcance)
:::

Reglas:

- **Solo crece.** Nunca se edita, fusiona ni reordena una línea anterior. Un hallazgo que resulta
  falso no se borra: se añade otro que lo corrige («corrige el hallazgo del 2026-10-15»).
- Una línea por entrada: `<fecha> · <skill o persona> · <qué>`.
- **Toda decisión confirmada pasa también a `pbi.md`/`bug.md`**, que es el contrato que leen los
  pasos siguientes, y se marca «Sí» en la tabla. `enrich-us` no termina con decisiones sin pasar.
- Los nombres de las personas se escriben siempre igual.

## Comentario para Azure DevOps

Cuando un paso confirma decisiones que cambian el work item (alcance, criterios, reglas), el
informe final termina con un bloque listo para pegar en Azure DevOps:

:::out
Comentario para Azure DevOps:
2026-10-15 · Decisiones del análisis (enrich-us):
- Ven la sección «Ofertas» los roles Comercial y Jefe de ventas (confirmado por Laura Gómez).
- El texto del menú será «Ofertas» en es, «Offers» en en y «Offres» en fr (propuesto, validado por Laura Gómez).
:::

La IA no lo publica: lo pegas tú. Solo lo haría con el MCP de Azure DevOps habilitado con
escritura y si se lo pides.

## Borradores de work items

Un problema real que no es de este work item (un bug, una deuda) no se arregla de paso: se escribe
como propuesta en `docs/sdd/_borradores/<slug>.md` para que una persona lo cree en Azure DevOps. Se
registra en la bitácora y se menciona en el informe final. Nunca es un `story.md`.

El borrador es temporal y **no llega a `dev`** (ADR-0027). Antes del PR:

1. Crea el work item en Azure DevOps con el contenido del borrador.
2. Anota su ID donde se citaba: una línea en `bitacora.md`
   (`2026-10-16 · Ana Pérez · borrador build-sin-tipos creado como #41100`), el estado del hallazgo
   en `qa-report.md` (`Work item #41100`) o la fila de *Hallazgos* de `plan.md`.
3. Borra el borrador.

`pr-check.py` da error si la rama añade o cambia un borrador, así que nadie se olvida: el hallazgo
acaba en el backlog, que es donde se prioriza, y no escondido en una carpeta del repositorio.
