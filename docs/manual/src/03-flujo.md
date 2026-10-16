# El flujo de un work item

:::lead
Todo work item recorre el mismo camino: de `story.md` a un PR revisado, documentado y enlazado en
Azure DevOps. Este capítulo da el mapa completo: los pasos, quién hace qué, dónde aprueba una
persona y qué archivo deja cada paso.
:::

## El mapa

@@figure flujo.svg | El flujo SDD. Los círculos amarillos son los pasos; G1–G4, las aprobaciones humanas. La franja amarilla es la vía rápida para bugs pequeños; la verde, el camino de QA.

| Paso | Skill o acción | Quién lo lanza | Entrada | Salida | Compuerta |
| --- | --- | --- | --- | --- | --- |
| 0 | `/project-context` | Tech lead, una vez por repositorio | El código y lo que ya hay escrito | *Project context* de `AGENTS.md`, `docs/*.md`, proyecto de pruebas, `sdd-guardrails.json` | Aprobación del borrador |
| 0 | `/document-project` (opcional) | Tech lead o un dev | El repositorio, por bloques | Comentarios de documentación y `docs/` completos | Un PR por bloque |
| — | `new-sdd-item.py` + copiar el work item | La persona que toma el work item | Azure DevOps | `story.md`, `bitacora.md`, `assets/` | — |
| 1 | `/enrich-us <id>` | Dev (o QA con `qa`) | `story.md` | `pbi.md` o `bug.md` | **G1** el PO o el dev confirman el análisis |
| 2 | `/technical-analysis <id>` | Dev | `pbi.md`/`bug.md` + código | `00`–`06` | **G2** aprobar `03` y `04` |
| 3 | `/wbs-execution <id>` | Dev | `00`–`06` | Código y pruebas, `CHANGELOG.md`, `commit-message.md` | Confirmar el inicio y cada tarea sensible |
| 4 | `/qa-review <id>` en **sesión nueva** | Dev o QA | El cambio y el diseño | `qa-report.md` | **G3** decidir cada hallazgo |
| 5 | `/document-code <id>` | Dev | El cambio | Comentarios y `docs/` | Confirmación de lo que se documenta |
| 6 | `git commit` + `pr-check.py` + PR | Dev | `commit-message.md` | PR a `dev` enlazado al work item | **G4** revisión del PR y validación del PO |
| 7 | Despliegue | Pipeline | `dev` | `dev` → `main`/Staging → producción | Según ADR-0006 |

:::note Una skill, una sesión
Cada paso grande se lanza en una **sesión nueva**: el contexto de la conversación anterior no hace
falta (todo está en los documentos) y una sesión limpia trabaja mejor y gasta menos. Para
`qa-review` es obligatorio: la sesión que implementó el cambio no puede revisarlo.
:::

## Las cuatro compuertas

Una compuerta es un punto en el que la IA se detiene y **una persona decide**. Sin esa respuesta no
se escribe nada.

| Compuerta | Cuándo | Qué decides | Si no estás de acuerdo |
| --- | --- | --- | --- |
| **G1** | Al final del análisis de `enrich-us`, antes de escribir `pbi.md`/`bug.md` | Si el resumen del work item es correcto: tipo, módulos, criterios, preguntas abiertas | Lo corriges en el chat; la IA rehace el resumen. Si falta información de negocio, se la pides al PO |
| **G2** | Tras `technical-analysis`: revisas `03-solution-proposal.md` y `04-implementation-plan.md` | Si el diseño y el plan son los adecuados. Una vez aprobados, son **contrato** | Pides el ajuste antes de aprobar. Después, cambiarlos exige tu aprobación explícita y una nueva versión |
| **G3** | Tras `qa-review` | Para cada hallazgo Alta o Media: corregir, aceptar el riesgo o llevarlo a otro work item | Puedes descartar un hallazgo con su motivo; la fila no se borra |
| **G4** | El PR a `dev` | El revisor aprueba el código; el PO valida los criterios de aceptación | Cambios en la misma rama, y otra ronda |

Además de las cuatro compuertas, cada skill pide **confirmación antes de empezar** y antes de
cualquier acción sensible: un cambio de contrato público, una migración, borrar archivos o tocar la
infraestructura.

## La carpeta del work item

Todo lo que el flujo produce para un work item vive en una sola carpeta junto al código (ADR-0002):
`docs/sdd/<id>-<título>/`. El título va en minúsculas, sin acentos y con guiones, como máximo 40
caracteres: `docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/`. Casi todo se versiona; lo que
duplica algo ya guardado o se regenera igual se queda en tu equipo (ADR-0027, columna *¿Se versiona?*).

@@figure carpeta.svg | Los archivos de la carpeta y el paso que crea cada uno.

| Archivo | Lo escribe | Para qué sirve | Quién lo lee después | ¿Se versiona? |
| --- | --- | --- | --- | --- |
| `story.md` | **Una persona** (nunca la IA) | El work item de Azure DevOps copiado tal cual: descripción, criterios, comentarios, adjuntos | `enrich-us`, `quick-fix` | Sí |
| `assets/` | Una persona | Las imágenes y archivos del work item, con nombre descriptivo | `enrich-us`, `quick-fix` | **No**: están en Azure DevOps; en otro equipo se bajan del work item |
| `bitacora.md` | Todas las skills | Notas con fecha: preguntas, respuestas y quién las dio, decisiones, hallazgos | Cualquier persona que retome el trabajo | Sí |
| `pbi.md` / `bug.md` | `enrich-us` (o `quick-fix`) | El requisito técnico completo y autosuficiente: el **contrato funcional** | Todos los pasos siguientes | Sí |
| `00-executive-summary.md` | `technical-analysis` | Resumen y marcadores pendientes | `wbs-execution` | Sí |
| `01-current-state-report.md` | `technical-analysis` | Cómo está hoy el código (solo hechos del código) | `wbs-execution`, revisores | Sí |
| `02-analysis-diagnosis.md` | `technical-analysis` | La brecha entre lo que hay y los criterios | `wbs-execution` | Sí |
| `03-solution-proposal.md` | `technical-analysis` | La solución: **contrato**, congelado tras G2 | `wbs-execution`, `qa-review`, `document-code` | Sí |
| `04-implementation-plan.md` | `technical-analysis` | Orden, SPECs, contratos, DoD: **contrato** | `wbs-execution`, `qa-review`, `test-cases` | Sí |
| `05-wbs-estimation.md` | `technical-analysis`; `wbs-execution` actualiza el estado | Tareas con SP, rol e i18n. **Fuente de verdad del avance** | `wbs-execution`, `qa-review` | Sí |
| `06-risks-mitigations.md` | `technical-analysis` | Riesgos ligados a tareas y su mitigación | `wbs-execution`, `qa-review` | Sí |
| `fix-plan.md` | `quick-fix` | Diseño de una página de la vía rápida: compuerta, causa, cambio, pruebas, `T-01` | `qa-review`, `document-code` | Sí |
| `CHANGELOG.md` | `wbs-execution`, `quick-fix`, `document-code` | Una entrada por tarea: archivos, SPECs verificadas, comandos ejecutados | `qa-review`, `document-code`, el mensaje de commit | Sí |
| `commit-message.md` | `wbs-execution`, `quick-fix` | El mensaje del commit del work item, que también es la descripción del PR | Tú, al hacer el commit | **No**: queda en el commit y en el PR |
| `qa-report.md` | `qa-review` | Hallazgos con severidad, estado y decisión | `wbs-execution <id> qa` | Sí |
| `test-cases.md` | `test-cases` | Casos de prueba | QA, `qa-review` | Sí |
| `test-cases.csv` | `test-cases` | El CSV para Azure Test Plans | QA | **No**: se regenera con `test_cases_csv.py` |

Lo que no se versiona ya está en el `.gitignore` del proyecto (lo añade `install.py`), así que
`git add <carpeta>` lo salta solo.

Hay además dos carpetas compartidas en `docs/sdd/`:

- `_borradores/`: propuestas de work items nuevos (un bug o una deuda encontrados fuera del
  alcance). Nunca son un `story.md` y **no llegan a `dev`**: antes del PR, una persona crea el work
  item en Azure DevOps, anota su ID donde se citaba el borrador y lo borra. `pr-check.py` da error
  si un borrador llega al PR.
- `_documentacion/`: el plan de `/document-project` (`plan.md`), un `B-NN.md` por bloque y
  `avisos.md` con la línea base de avisos del build. Se versiona mientras dure el plan.

## Reglas que no cambian nunca

:::danger Las reglas fijas del flujo
- `story.md` lo prepara una persona y la IA nunca lo edita. Si algo falta, se corrige en Azure
  DevOps y se vuelve a copiar.
- La IA nunca hace commit, push, merge ni cambia de rama salvo que se lo pidas. Los permisos de
  Claude Code lo bloquean además.
- Un commit por work item. Siempre `Ref: #<id>`, nunca `fix #<id>` (Azure Repos cerraría el work
  item). Sin líneas `Co-Authored-By`: el sello SDD es la evidencia.
- `git add` con rutas exactas, nunca `git add -A` ni `git add .`.
- `qa-review` siempre en una sesión distinta de la que implementó.
- Nada de secretos: ni leerlos ni copiarlos en comentarios, documentos o commits.
- Al repositorio no van `assets/`, `commit-message.md`, `test-cases.csv` ni los borradores (ADR-0027).
- Toda decisión confirmada pasa de `bitacora.md` a `pbi.md`/`bug.md`, que es el contrato.
:::

## Ramas y despliegue

El modelo de ramas es el de ADR-0006:

| Rama | Para qué | Quién la crea |
| --- | --- | --- |
| `feature/<id>-<título>` | Un PBI | El dev, desde `dev` |
| `fix/<id>-<título>` | Un bug (vía rápida o flujo completo) | El dev, desde `dev` |
| `chore/…` · `docs/…` | Cambios del kit, del contexto o de documentación | El dev o el tech lead |
| `dev` | Integración; destino de los PR | — |
| `main` | Staging, y de ahí producción | El pipeline, tras aprobar |

:::tip Las skills comprueban la rama
`quick-fix`, `project-context` y `document-project` se paran si estás en `dev` o `main`, y te piden
crear la rama. `wbs-execution` te recuerda al final cuál es la rama esperada antes del commit.
:::
