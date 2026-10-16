# Prompts y plantillas

:::lead
Los prompts son atajos de Copilot que fijan el modelo de una skill. Las plantillas son la estructura
fija de cada documento: secciones, tablas y anclas que la siguiente skill sabe encontrar. Ninguna
se rellena a mano salvo `story.md` y, a veces, `sdd-guardrails.json`.
:::

## El prompt wbs-execution-sonnet

Copilot no permite que una skill fije su modelo, pero un archivo de prompt sí. El kit trae uno:
`.github/prompts/wbs-execution-sonnet.prompt.md`.

```markdown
---
agent: agent
description: 'Paso 3 del flujo SDD con el modelo fijado en Sonnet: implementa tarea por tarea…'
model: Claude Sonnet 5 (copilot)
tools: ['search', 'read', 'edit', 'execute', 'todo']
---
# Ejecución WBS con Sonnet — work item ${input:item:ID del work item (ej: 40399)}
Ejecuta la skill `wbs-execution` para este work item, siguiendo exactamente las instrucciones de
wbs-execution/SKILL.md …
```

**Cómo se usa (VS Code):** en el chat, `/wbs-execution-sonnet`. Copilot te pide el ID
(`${input:item}`) y ejecuta la skill con Sonnet y las herramientas indicadas.

**Cuándo:** el paso 3 en Copilot, si no quieres cambiar el modelo a mano. Las reglas no están en el
prompt (solo fija el modelo): si cambia el proceso, se cambia el `SKILL.md`.

:::note En Claude Code no hace falta
La copia de `.claude/skills/wbs-execution/SKILL.md` ya lleva `model: sonnet` en su cabecera, igual
que `quick-fix` y `test-cases`; `project-context` lleva `opus`.
:::

## Plantillas de un work item

| Plantilla | Skill | Archivo que genera | Secciones clave y anclas |
| --- | --- | --- | --- |
| `enrich-us/templates/story.md` | `new-sdd-item.py`, `enrich-us` | `story.md` | Cabecera (*Preparado por*, *Fuente*, *Estado*…), Descripción, Pasos para reproducir y Sistema (solo bug), Criterios, Comentarios, Adjuntos, Enlaces |
| `enrich-us/templates/bitacora.md` | Todas | `bitacora.md` | Decisiones (con «En pbi.md: Sí/No»), Preguntas abiertas, Registro `sdd:log`, Hallazgos |
| `enrich-us/templates/pbi.md` | `enrich-us` | `pbi.md` | `sdd:description`, `sdd:acceptance-criteria`, campos, endpoints, archivos, reglas, `sdd:qa-classification`, `sdd:i18n`, pruebas, DoD, `sdd:pending` |
| `enrich-us/templates/bug.md` | `enrich-us`, `quick-fix` | `bug.md` | `sdd:description`, reproducción, esperado/actual, causa inferida, `sdd:acceptance-criteria`, `sdd:qa-classification`, `sdd:i18n`, impacto, `sdd:pending` |
| `technical-analysis/templates/00…06` | `technical-analysis` | `00`–`06` | `sdd:markers` (00), `sdd:i18n` (01 §1.8), `sdd:specs` (04), `sdd:tasks` y `sdd:task-log` (05), `sdd:risks` (06) |
| `wbs-execution/templates/changelog.md` | `wbs-execution`, `quick-fix`, `document-code` | `CHANGELOG.md` | Una entrada por tarea: verificación, archivos, cambios, SPECs, traducciones, comandos, notas fuera de alcance |
| `qa-review/templates/qa-report.md` | `qa-review` | `qa-report.md` | Resultado, `sdd:qa-findings`, qué se revisó, runtime, pendiente |
| `quick-fix/templates/fix-plan.md` | `quick-fix` | `fix-plan.md` | `sdd:fix-gate`, `sdd:fix-cause`, cambio, `sdd:fix-tests`, riesgos, `sdd:tasks` |
| `test-cases/templates/test-cases.md` | `test-cases` | `test-cases.md` | Resumen por criterio, `sdd:test-cases` con `### TC-NN · título` y tabla de pasos |

### story.md: la única que rellenas tú

`new-sdd-item.py` la crea con un comentario de instrucciones. Así queda rellena:

:::file docs/sdd/40399-…/story.md
# Work item 40399 — Sección de ofertas en el menú lateral

**Preparado por:** Ana Pérez · **Leído:** 2026-10-15
**Fuente:** Azure DevOps · MiProyecto · PBI · revisión 7
**Estado:** Approved · **Iteración:** MiProyecto\Sprint 42 · **Área:** MiProyecto\Comercial · **Asignado a:** Ana Pérez · **Prioridad:** 2

## Descripción

Como comercial quiero ver mis ofertas desde el menú lateral para no tener que entrar por Clientes.

## Criterios de aceptación

- El menú lateral muestra «Ofertas» debajo de «Clientes».
- Al pulsarla se abre el listado de ofertas del usuario.

## Comentarios

- 2026-10-10 · Laura Gómez: ver el mockup adjunto.

## Adjuntos

- [assets/40399-menu-lateral.png](./assets/40399-menu-lateral.png): mockup del menú con «Ofertas» bajo «Clientes»

## Enlaces

- Padre: #40100 Área comercial (contexto del módulo)
:::

:::warn Reglas de story.md
- Copia el texto **literal**: sin resumir, corregir ni traducir.
- Una sección vacía en Azure DevOps se escribe «Sin <sección> en el work item».
- Imágenes con nombre descriptivo (`40399-menu-lateral.png`, no `image.png`) y una línea que
  diga qué muestran: no todas las herramientas ven imágenes.
- Si depende de otro work item, copia aquí lo necesario de ese otro: la IA solo lee este archivo.
- Nada sensible: ni credenciales ni datos personales de clientes, tampoco en capturas.
- `assets/` no se versiona (ADR-0027): los adjuntos ya están en Azure DevOps. Quien retome el work
  item en otro equipo los baja del work item con los mismos nombres que enlaza `story.md`.
- Si el work item cambia, actualiza `story.md` y anota el motivo en `bitacora.md`.
:::

### 05-wbs-estimation.md: la fuente de verdad del avance

:::view Tabla de tareas de 05 (sdd:tasks)
| ID | Tarea | Descripción | Capa | Deps | SP | Rol | i18n | Origen | Estado |
| -- | ----- | ----------- | ---- | ---- | -- | --- | ---- | ------ | ------ |
| T-01 | Permiso «ver ofertas» | Nuevo permiso y pruebas | Backend | — | 2 | Backend | No | 03 §3.4 | ✅ Hecha |
| T-02 | Entrada en el menú | Entrada, visibilidad y textos | Frontend | T-01 | 2 | Frontend | Sí | 04 §4.2 | ⬜ Pendiente |
:::

Estados: `⬜ Pendiente` · `🔄 En curso` · `✅ Hecha` · `🔴 Bloqueada`. `wbs-execution` solo cambia
la celda *Estado* y añade una línea en *Registro de ejecución*.

### 04-implementation-plan.md: las SPECs

:::view Especificaciones SDD de 04 (sdd:specs)
| ID | Dado / Cuando / Entonces | Tipo | Prioridad | Cubre |
| -- | ------------------------ | ---- | --------- | ----- |
| SPEC-01 | Dado un usuario Comercial, cuando abre el menú, entonces ve «Ofertas» bajo «Clientes» | Unitaria | Alta | CA-01 |
| SPEC-02 | Dado un usuario JefeVentas, cuando abre el menú, entonces ve «Ofertas» | Unitaria | Alta | CA-02 |
| SPEC-03 | Dado un usuario Consultor, cuando abre el menú, entonces no ve «Ofertas» | Unitaria | Media | CA-02 |
:::

### Una entrada de CHANGELOG.md

:::file CHANGELOG.md
## 2026-10-15 — T-02: Entrada «Ofertas» en el menú lateral

**Estado de verificación:** ✅ Verificado

**Archivos modificados:**
- `ClientApp/src/layout/SideMenu.tsx` — entrada «Ofertas» con permiso ViewOffers
- `ClientApp/src/layout/SideMenu.test.tsx` — 3 casos por rol

**SPEC SDD verificadas:**
- SPEC-01: ✓ — prueba automatizada (SideMenu.test.tsx)
- SPEC-02: ✓ — prueba automatizada

**Traducciones:** claves añadidas en todos los idiomas
- `Offers` → es ✓ · en (clave) · fr ✓

**Verificaciones ejecutadas:**
- `yarn lint` → Exitoso
- `yarn test` → 51 en verde, 0 fallidas
- `yarn tsc --noEmit` → Exitoso

**Notas fuera de alcance:**
- SideMenu.tsx:30 — «Inicio» está escrito sin i18n (ya existía)
:::

## Plantillas del proyecto

| Plantilla | La usa | Archivo | Contenido |
| --- | --- | --- | --- |
| `project-context/templates/project-context.md` | `project-context` | *Project context* de `AGENTS.md` | Los 11 encabezados fijos con su presupuesto de líneas y la marca `sdd:context` (fecha y fuentes) |
| `project-context/templates/docs/*.md` (6) | `project-context`, `document-code`, `document-project` | `docs/architecture.md`, `backend.md`, `database.md`, `api-reference.md`, `frontend.md`, `reglas-negocio.md` | Encabezados fijos de cada documento |
| `project-context/templates/tests/ArchitectureTests.cs` | `project-context` | `<Tests>/Architecture/ArchitectureTests.cs` | Pruebas xUnit de capas y autorización con cuatro marcadores `{{...}}` (capítulo 12) |
| `document-project/templates/plan.md` | `document-project` | `docs/sdd/_documentacion/plan.md` | `sdd:doc-areas`, `sdd:doc-blocks`, `sdd:doc-findings`, `sdd:log`, archivos por área |
| `document-project/templates/bloque.md` | `document-project` | `docs/sdd/_documentacion/B-NN.md` | Resultado, validación, sin documentar, mensaje de commit |
| `core/templates/AGENTS.project.md` | `install.py` | `AGENTS.md` | Las marcas del bloque del kit y el hueco de *Project context* |
| `core/templates/.gitmessage` | `install.py` | `.gitmessage` | La plantilla de commit del equipo (capítulo 14) |
| `core/templates/sdd-guardrails.json` | `install.py` | `sdd-guardrails.json` | Configuración del hook y de `pr-check.py` (capítulo 12) |
| `core/templates/mcp/*.json` (3) | A mano | `.vscode/mcp.json`, `.mcp.json`, `.claude/settings.json` | MCP de Azure DevOps en solo lectura |
| `project-templates/docs/adr/0000-plantilla.md` | Personas, `document-code` | `docs/adr/NNNN-<título>.md` | Contexto, decisión, consecuencias, alternativas |

:::tip Mejorar una plantilla
Las plantillas se cambian en el kit (`core/skills/<skill>/templates/`), nunca en la copia
instalada. Si quitas o renombras un ancla `<!-- sdd:... -->`, `validate.py` lo detecta: la siguiente
skill dejaría de encontrar la sección.
:::
