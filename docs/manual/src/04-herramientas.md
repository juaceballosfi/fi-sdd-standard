# Herramientas y dónde vive cada cosa

:::lead
El kit tiene una sola fuente (`core/` del repositorio del kit) y el instalador la copia al formato
que lee cada herramienta. Así, una misma skill funciona igual en Claude Code y en Copilot, y una
corrección se hace una sola vez.
:::

## Herramientas soportadas

| Herramienta | Estado en el MVP | Subagentes | Hooks | Cómo se invoca una skill |
| --- | --- | --- | --- | --- |
| **Claude Code** (terminal, VS Code, escritorio) | Flujo completo, probado en Bonis | Sí (herramienta *Agent*) | Sí | `/enrich-us 40399` |
| **GitHub Copilot en VS Code** (modo agente) | Flujo completo, en pruebas (ola 3) | Sí (`runSubagent`) | No: el pipeline y `pr-check.py` cubren las reglas | `/enrich-us 40399` |
| **GitHub Copilot en Visual Studio** | Carga de reglas y skills, y pasos sueltos | No: la sesión hace todo el trabajo | No | `/enrich-us 40399` (desde 17.14/18.5) o pidiéndolo en el chat |
| **Codex** | Fase 7 | — | — | — |

:::note Si la herramienta no tiene subagentes
Todas las skills funcionan sin subagentes: la sesión principal hace el trabajo con las mismas
reglas y lo dice en su confirmación («*Writer: this session (the tool has no subagents)*»). Solo
se pierde la separación de contexto y, en `qa-review`, conviene elegir a mano un modelo de
razonamiento.
:::

## Qué se instala y dónde

@@figure herramientas.svg | El instalador copia la fuente única del kit al formato de cada herramienta.

| Pieza | Copilot · VS Code | Copilot · Visual Studio | Claude Code | ¿Se versiona? |
| --- | --- | --- | --- | --- |
| Reglas | `AGENTS.md` | `.github/copilot-instructions.md` (generado desde `AGENTS.md`) | `CLAUDE.md`, que solo contiene `@AGENTS.md` | `AGENTS.md` y `CLAUDE.md` sí · `copilot-instructions.md` no (copia local, ADR-0027) |
| Skills | `.agents/skills/<skill>/` | `.agents/skills/<skill>/` | `.claude/skills/<skill>/` (copia generada) | `.agents/` sí · `.claude/skills/` no |
| Subagentes | `.github/agents/<nombre>.agent.md` | `.github/agents/` (se eligen a mano) | `.claude/agents/<nombre>.md` (copia generada) | `.github/agents/` sí · `.claude/agents/` no |
| Prompts | `.github/prompts/*.prompt.md` | `.github/prompts/` | — | Sí |
| Hook y permisos | — | — | `.claude/settings.json` + `.agents/hooks/sdd_guard.py` | Sí |
| Configuración de guardarraíles | `sdd-guardrails.json` | `sdd-guardrails.json` | `sdd-guardrails.json` | Sí |
| Scripts del proyecto | `.agents/scripts/` | `.agents/scripts/` | `.agents/scripts/` | Sí |
| Plantilla de commit | `.gitmessage` | `.gitmessage` | `.gitmessage` | Sí |
| Registro de la instalación | `.sdd-kit.json` | `.sdd-kit.json` | `.sdd-kit.json` | Sí |

:::warn No edites las copias generadas
Los archivos de `.claude/skills/` y `.claude/agents/` empiezan con
`# GENERATED from fi-sdd-standard by scripts/install.py - do not edit this copy`. Si cambias algo
ahí, el próximo `install.py` lo sobrescribe. Las mejoras se hacen en el kit (`core/`) y se
reinstalan. Lo mismo vale para `.agents/skills/`: `pr-check.py` da error si una rama cambia un
archivo del kit sin un commit `chore(sdd)`.
:::

## El archivo AGENTS.md

`AGENTS.md`, en la raíz del proyecto, es lo primero que lee cualquier herramienta. Tiene dos
partes:

```text
<!-- sdd-kit:base:start -->
  # Team rules (fi-sdd-standard)        ← reglas comunes; las escribe install.py, no se editan
  ...
<!-- sdd-kit:base:end -->

# Project context — <proyecto>          ← lo escribe /project-context; lo mantiene el equipo
## What this is
## Commands
## Local run
## Architecture
## Authorization and errors
## Data
## Tests
## Internationalization
## Protected paths
## Branches, CI and commits
## Documentation
```

- El **bloque del kit** son las reglas del equipo (unas 55 líneas). Se actualiza solo al
  reinstalar el kit.
- El ***Project context*** son los hechos del proyecto: comandos verificados, línea base de avisos y
  pruebas, arquitectura, autorización, datos, traducciones, rutas protegidas. Lo escribe
  `/project-context` con encabezados fijos en inglés y se revisa con `/project-context check`.
- Límite: **200 líneas** en total (objetivo: menos de 185). Lo que no cabe va a `docs/` con un
  enlace. `pr-check.py` y `check_project.py` lo comprueban.

:::tip Por qué los encabezados están en inglés
Las instrucciones internas del kit están en inglés (ADR-0003) y las skills buscan las secciones de
*Project context* por su nombre exacto. El contenido puede estar en español.
:::

## Modelos

Cada paso pide un tipo de trabajo distinto. El kit fija el modelo donde la herramienta lo permite
(ADR-0014; la tabla se revisa cada mes):

| Skill o subagente | Tipo de trabajo | Claude Code | Copilot |
| --- | --- | --- | --- |
| `enrich-us`, `technical-analysis` | Análisis y diseño | El de la sesión: elige uno de razonamiento (Opus) | Elige uno de razonamiento en el chat |
| `project-context` | Síntesis de todo el repositorio | Fijado: `opus` | Elige uno de razonamiento |
| `wbs-execution`, `quick-fix`, `test-cases` | Ciclos rápidos de implementación o trabajo estructurado | Fijado: `sonnet` | Prompt `/wbs-execution-sonnet`, o elige Sonnet |
| `qa-review`, `document-code`, `document-project` | Coordinación | El de la sesión | El de la sesión (en `qa-review`, uno de razonamiento) |
| `code-explorer`, `doc-writer` | Búsqueda y escritura acotada | `haiku` (tier *fast*) | El modelo del chat |
| `backend-dev`, `frontend-dev`, `runtime-tester`, `migration-reviewer` | Implementación y comprobación | `sonnet` (tier *standard*) | El modelo del chat |
| `qa-reviewer` | Revisión adversarial | `opus` (tier *reasoning*) | El modelo del chat |

El modelo con el que se generó cada documento queda en su sello (`**Generado con:** … · <modelo>`).
Si la sesión no sabe qué modelo es, escribe el modelo por defecto del equipo, `claude-opus-5-5`.

## MCP de Azure DevOps

El kit trae plantillas para conectar el MCP de Azure DevOps en **solo lectura** (ADR-0008,
propuesta): `core/templates/mcp/vscode-mcp.json` (VS Code), `claude-mcp.json` y
`claude-settings-mcp.json` (Claude Code). Con el MCP activo y declarado en `AGENTS.md`,
`enrich-us` puede leer el work item y escribir `story.md` por ti, que luego **revisas**. Mientras
TI no confirme el acceso con Entra ID, `story.md` se copia a mano. La guía está en
`docs/guias/mcp-azure-devops.md` del kit.
