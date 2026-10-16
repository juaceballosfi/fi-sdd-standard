# Referencia rápida

:::lead
Todo lo esencial en un par de páginas. Imprímelas o tenlas a mano las primeras semanas.
:::

## Comandos de las skills

| Comando | Paso | Sesión | Sale |
| --- | --- | --- | --- |
| `/project-context` · `fresh` · `check` | 0 | Nueva · Opus | *Project context*, `docs/`, pruebas, guardarraíles |
| `/document-project` · `plan` · `status` · `block:B-NN` · `area:A-NN` | 0 (opcional) | Nueva por bloque | Comentarios, `docs/`, `_documentacion/` |
| `/enrich-us <id>` · `<id> qa` | 1 · G1 | Nueva · Opus | `pbi.md` / `bug.md` |
| `/technical-analysis <id>` | 2 · G2 | Nueva · Opus | `00`–`06` |
| `/wbs-execution <id>` · `from:T-XX` · `qa` | 3 | Nueva · Sonnet | Código, `CHANGELOG.md`, `commit-message.md` |
| `/wbs-execution-sonnet` (Copilot) | 3 | Nueva | Igual, con Sonnet fijado |
| `/quick-fix <id>` | 1–3 (bug) | Nueva · Sonnet | `bug.md`, `fix-plan.md`, código |
| `/qa-review <id>` · `base:` · `head:` | 4 · G3 | **Nueva siempre** | `qa-report.md` |
| `/document-code <id>` · `base:` | 5 | Nueva | Comentarios, `docs/` |
| `/test-cases <id>` | QA | Nueva · Sonnet | `test-cases.md`, `.csv` |

## Comandos de terminal

```powershell
# Instalar o actualizar el kit
python <kit>\scripts\install.py --target . --tools copilot,claude [--dry-run]
git config commit.template .gitmessage

# Empezar un work item
git switch -c feature/<id>-<título> origin/dev
python <kit>\scripts\new-sdd-item.py <id> "<título>" [--tipo bug]
python .agents\scripts\check-sdd-item.py docs\sdd\<carpeta>

# Antes del PR
git add <rutas exactas> docs\sdd\<carpeta>\
git commit -F docs\sdd\<carpeta>\commit-message.md
python .agents\scripts\pr-check.py
cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"
python .agents\scripts\check-sdd-item.py --commit-message $env:TEMP\msg.txt --id <id>

# Contexto y documentación
python .agents\skills\project-context\scripts\check_project.py
python .agents\skills\document-project\scripts\doc_coverage.py --warnings build.log --compare docs\sdd\_documentacion\avisos.md

# Probar el hook
'{"tool_name":"Read","tool_input":{"file_path":"Api/appsettings.Development.json"}}' | python .agents\hooks\sdd_guard.py pre
```

## Compuertas

| | Cuándo | Decides |
| --- | --- | --- |
| **G1** | Fin del análisis de `enrich-us` | Si el resumen del work item es correcto |
| **G2** | Tras `technical-analysis` | Aprobar `03` y `04` (contrato) |
| **G3** | Tras `qa-review` | Corregir, aceptar o separar cada hallazgo |
| **G4** | PR a `dev` | Aprobar el código; el PO valida los criterios |

## Límites de los bucles

| Bucle | Límite |
| --- | --- |
| Un subagente con la misma comprobación fallando | 3 intentos |
| Verificación de la sesión → vuelta al subagente | 2 rondas |
| Subagente parado sin informe | 1 reanudación |
| Rondas de QA | 2 |
| `doc-writer` con cambios que no son comentarios | 2 rondas |
| Tareas seguidas en una sesión de `wbs-execution` | Bloques de 6 |

## La compuerta de quick-fix

Causa con `archivo:línea` · ≤ 3 archivos de producción de una capa · sin migración ni entidad · sin
cambio de contrato · sin cambio de autorización · sin `[PENDING-BUSINESS]` · textos nuevos con
todas sus traducciones · sin paquetes nuevos ni actualizados.

## Marcadores

| Marcador | Falta |
| --- | --- |
| `[PENDING-BUSINESS: pregunta]` | Información de negocio |
| `[REQUIRES-VALIDATION: motivo]` | Evidencia técnica |
| `[ASSUMPTION-BASED: campo]` | Un campo del que depende la sección |
| `[PENDING-TRANSLATION: clave → idioma]` | Una traducción |

## Commit

```text
tipo(ámbito): descripción en imperativo, minúscula, ≤ 72 caracteres

PBI-<id> — [MÓDULO] Título del work item

**Problema** · **Causa** (solo fix) · **Cambios** · **Alcance y no regresión** · **Pruebas**

Ref: #<id>
```

Nunca `fix #id` · nunca `Co-Authored-By` · < 4000 caracteres · un commit por work item ·
`git add` con rutas exactas.

## Qué no se versiona (ADR-0027)

De cada work item: `assets/` (los adjuntos están en Azure DevOps), `commit-message.md` (queda en el
commit y en el PR) y `test-cases.csv` (se regenera). Tampoco los borradores de
`docs/sdd/_borradores/` (se crean en Azure DevOps y se borran antes del PR), ni `.claude/skills/`,
`.claude/agents/`, `.claude/settings.local.json` o `.github/copilot-instructions.md`.

## Lo que la IA nunca hace

:::grid2
:::tile
- Commit, push, merge ni cambiar de rama sin que lo pidas.
- Leer o mostrar secretos.
- Editar rutas protegidas o `story.md`.
- Inventar reglas, criterios, límites o traducciones.
:::
:::tile
- Revisar en la misma sesión lo que implementó.
- Cambiar `03`/`04` aprobados sin tu aprobación.
- Arreglar de paso algo fuera del work item.
- Decir que algo se ejecutó si no se ejecutó.
:::
:::
