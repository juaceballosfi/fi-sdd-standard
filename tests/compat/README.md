# Prueba de compatibilidad

Un work item real recorre el flujo en cada herramienta, con las mismas comprobaciones. Es el criterio
de salida de la fase 2 y se repite en cada versión menor del kit (ADR-0005).

| Herramienta | Alcance en el MVP |
| --- | --- |
| Claude Code | Flujo completo (probado en los pilotos de Bonis) |
| GitHub Copilot en VS Code | Flujo completo, con `runSubagent` |
| GitHub Copilot en Visual Studio | Carga de reglas y skills, y un paso (decisión pendiente: ¿flujo completo?) |
| Codex | Fase 7 |

## 1 · Carga (cada herramienta, 10 min)

En el repositorio con el kit instalado, en una sesión nueva:

| # | Comprobación | Cómo | Esperado |
| --- | --- | --- | --- |
| C1 | Lee `AGENTS.md` | «¿Qué reglas de commit tiene este proyecto?» | Cita `.gitmessage`, `Ref: #id` y nunca `fix #id` |
| C2 | No duplica las reglas | VS Code: en *Chat → References* de una respuesta, mira qué archivos de instrucciones entraron | `AGENTS.md` una sola vez. Si también entra `.github/copilot-instructions.md`, pon `"github.copilot.chat.codeGeneration.useInstructionFiles": false` en `.vscode/settings.json` y repite |
| C3 | Ve los skills | Escribe `/` (VS Code y Claude Code) o pregunta «¿qué skills tienes?» | Los 9 del kit |
| C4 | Ve los agentes | VS Code: el selector de agentes; Claude Code: `/agents` | Los 7 estables (`.github/agents/*.agent.md` o `.claude/agents/`) |
| C5 | Argumentos | `/enrich-us 40933` | Toma el ID (Copilot no sustituye `$ARGUMENTS`: el skill lo lee del mensaje) |
| C6 | Guardarraíles | Claude Code: «lee Bonis/appsettings.Development.json» | Bloqueado por el permiso o por el hook. En Copilot no hay hook: anótalo |

## 2 · Flujo completo (VS Code, 1–2 sesiones por paso)

Un PBI real y pequeño, con una sola capa, y otro work item que tenga traducciones.

| Paso | Comando | Comprobar |
| --- | --- | --- |
| 0 | `new-sdd-item.py` y `story.md` copiado | `check-sdd-item.py` en verde |
| 1 | `/enrich-us <ID>` | `pbi.md` con sello `GitHub Copilot`; preguntas en un bloque |
| 2 | `/technical-analysis <ID>` | 00–06 con sus anclas; `code-explorer` delegado con `runSubagent` |
| 3 | `/wbs-execution <ID>` | Cada tarea la escribe `backend-dev` o `frontend-dev` (subagente), línea *Rojo*, verificación propia |
| 4 | `/qa-review <ID>` en una sesión nueva | `qa-reviewer` como subagente; `qa-report.md` con su ancla |
| 5 | `/document-code <ID>` | `doc-writer` como subagente; `comment_only.py` dice «solo comentarios» |
| 6 | Commit y `pr-check.py` | 0 errores |
| — | `/quick-fix <ID>` con un bug pequeño | La compuerta y la tarea `T-01` |

Para cada paso, anota: funcionó · funcionó con ayuda (qué) · no funcionó (qué), el modelo, el
tiempo y si los subagentes corrieron como subagentes o la sesión hizo el trabajo.

## 3 · Resultados

| Comprobación | Claude Code | VS Code | Visual Studio |
| --- | --- | --- | --- |
| C1–C6 | | | |
| Pasos 0–6 | ✓ (Bonis, v0.10) | | |
| `quick-fix` | | | |
| Subagentes reales | ✓ | | — |
| Hooks | ✓ | no tiene | no tiene |

Las diferencias que obliguen a cambiar un skill se corrigen en el kit (`core/skills/`) y se anotan
en el CHANGELOG. Nunca se corrigen en la copia instalada.
