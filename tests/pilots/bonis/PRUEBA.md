# Prueba del flujo SDD en Bonis · kit v0.4.1

**Objetivo:** comprobar con un work item real de Bonis que los tres skills v3.2 funcionan en un
proyecto existente: instalación, preparación de `story.md` por la persona (ADR-0015),
enriquecimiento, diseño, implementación y mensaje de commit. Los pasos 4 (revisión de QA) y 5
(documentación) todavía no están en el kit.

**Dónde:** en una rama de prueba de Bonis. Nada se mezcla con `dev` hasta revisar los resultados.

Los comandos están en PowerShell, desde la raíz de Bonis, con el kit en `..\fi-sdd-standard`.

## 1 · Preparación

### Si ya instalaste una versión anterior

1. Sustituye el contenido de tu `fi-sdd-standard` por el de la v0.4.1 (conserva tu carpeta `.git`)
   y valida:
   ```powershell
   cd ..\fi-sdd-standard
   python scripts\validate.py      # 0 errores; los 5 avisos de skills de Roger son esperados
   cd ..\bonis_v2
   ```
2. Actualiza Bonis:
   ```powershell
   python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
   ```
   Esperado: `actualizado` en los skills de `.agents\skills` y `.claude\skills` y en el bloque del
   kit de `AGENTS.md`, ningún `CONFLICTO` y «Todo en orden» al final.

### Si es la primera vez

1. Valida el kit (`python scripts\validate.py`, como arriba).
2. Rama de prueba en Bonis:
   ```powershell
   git checkout dev; git pull
   git checkout -b chore/sdd-kit-piloto
   ```
3. Reglas del proyecto. Compara primero, luego copia:
   ```powershell
   git diff --no-index CLAUDE.md ..\fi-sdd-standard\tests\pilots\bonis\AGENTS.md
   copy ..\fi-sdd-standard\tests\pilots\bonis\AGENTS.md .
   copy ..\fi-sdd-standard\tests\pilots\bonis\CLAUDE.md .     # queda en una línea: @AGENTS.md
   ```
   Completa el `TODO` de la sección *Frontend architecture*: archivos de traducción de i18next,
   idiomas, convención de claves y qué pasa si falta una clave.
4. Instalación, primero en simulación:
   ```powershell
   python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude --dry-run
   python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
   ```
   Haz solo lo que diga la línea «Siguiente» del final. Si dice «Todo en orden», no hay nada más.

### Opcional: pegar imágenes en VS Code directamente en `assets/`

Al pegar una imagen en un `.md`, VS Code crea el archivo junto al documento. Con esto en
`.vscode/settings.json` (o en tu configuración de usuario) la deja en `assets/`:

```json
"markdown.copyFiles.destination": { "**/docs/sdd/*/story.md": "assets/" }
```

Después, renómbrala con un nombre descriptivo desde el explorador de VS Code; si pregunta si
actualiza los enlaces, di que sí.

## 2 · Comprobar que las herramientas ven el kit

| Comprobación | Claude Code | Copilot (VS Code) |
| --- | --- | --- |
| Al escribir `/` aparecen `enrich-us`, `technical-analysis` y `wbs-execution` | | |
| Cuántas veces aparece cada skill (VS Code lee también `.claude/skills/`: se esperan dos) | — | |
| Preguntar «¿Qué rutas no puedes editar en este proyecto?» responde `core-ui` y `docs/modernizacion/` | | |
| Contexto al empezar la sesión (`/context` en Claude Code) | | — |

## 3 · Preparar `story.md` (lo haces tú, no la IA)

Work item de la prueba: **PBI 40944 — [RSP] Ubicación seguimiento del servicio**.

1. Crea la carpeta, salvo que ya la tengas:
   ```powershell
   python ..\fi-sdd-standard\scripts\new-sdd-item.py 40944 "[RSP] Ubicación seguimiento del servicio"
   ```
   Crea `docs\sdd\40944-rsp-ubicacion-seguimiento-del-servicio\` con `story.md` (encabezado ya
   rellenado con ID, título, tipo, tu nombre y la fecha), `bitacora.md` y `assets\`. Para un bug,
   añade `--tipo bug`. Si ya creaste la carpeta a mano, no hace falta: el comprobador del punto 3
   te dice si el nombre sigue el formato.
2. Copia el work item de Azure DevOps en `story.md`. Las reglas están en el comentario del
   archivo; las importantes:
   - Texto tal cual, sin resumir ni corregir.
   - Rellena todos los `<…>` del encabezado; la revisión está en la pestaña *History*.
   - Una sección vacía en Azure DevOps se escribe «Sin criterios de aceptación en el work item»
     (o el campo que sea), no «No incluido en el texto pegado».
   - Imágenes y archivos en `assets\` con nombre descriptivo, enlazados y descritos en una línea
     en *Adjuntos*.
   - Si viene de otro work item (el 40944 dice «Copied … from #40942»), ábrelo y copia aquí lo que
     aporte.
3. Comprueba hasta que no queden errores:
   ```powershell
   python ..\fi-sdd-standard\scripts\check-sdd-item.py docs\sdd\40944-rsp-ubicacion-seguimiento-del-servicio
   ```
   El aviso «pbi.md / bug.md todavía no existe» es normal en este punto.
4. Deja `story.md` preparado (sin commit) para ver después si la IA lo ha tocado:
   ```powershell
   git add docs\sdd\40944-rsp-ubicacion-seguimiento-del-servicio
   ```

## 4 · Recorrer el flujo

Empieza cada paso en una **sesión nueva** (`/clear` en Claude Code o chat nuevo en Copilot) y anota
el contexto con `/context` al terminar. Después de cada paso, pasa el comprobador del punto 3.3.

| Paso | Qué escribes | Qué comprobar |
| --- | --- | --- |
| 1 | `/enrich-us 40944` | Encuentra la carpeta · lee `story.md` y abre la imagen (o dice que no puede y usa la descripción de *Adjuntos*) · en el resumen de confirmación muestra los adjuntos revisados y los huecos de `story.md` · pide confirmación antes de escribir · propone criterios solo a partir de la descripción y la imagen, marcados «Propuesto desde la descripción — validar con PO» · pregunta qué perfiles y qué permiso son «delegados master y RRHH que tengan habilitado…» · i18n «no aplica» (solo cambia el orden) · `pbi.md` con las anclas · `git diff -- docs\sdd\40944-*\story.md` vacío (no lo ha tocado) |
| 2 | `/technical-analysis 40944` | Lee solo la carpeta del ítem · detecta la arquitectura real (Controllers → Services → Data, `ArchitectureTests.cs`) · encuentra dónde se construye el menú y cómo se filtra por perfil · genera `00` a `06` · la columna `i18n` del WBS tiene sentido · añade la entrada en la bitácora |
| — | Revisas y apruebas 03 y 04: cambia su línea a `**Estado:** Aprobado (<fecha>, Juan Ceballos)` | El comprobador marca 03 y 04 como aprobados |
| 3 | `/wbs-execution 40944` (o `/wbs-execution-sonnet` en Copilot) | Detecta `dotnet test Bonis.Tests -c Release`, `yarn lint` y `yarn test` · escribe la prueba antes del código · marca las tareas en el WBS · crea `CHANGELOG.md` · al cerrar, `commit-message.md` sigue el `.gitmessage` · no hace commit |
| Commit | `git add -A; git commit -F docs\sdd\40944-rsp-ubicacion-seguimiento-del-servicio\commit-message.md` | `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"` y `check-sdd-item.py --commit-message $env:TEMP\msg.txt --id 40944` sin errores (con `>` de PowerShell se estropean las tildes y la raya «—») |

Si la IA necesita un log largo (de CI, de un build), guárdalo en un archivo fuera del repositorio y
dale la ruta. No lo pegues en el chat: en el primer piloto, pegarlo llevó el análisis a 551k tokens.

Si un paso falla o hace algo raro, **para** y anota qué escribiste y qué respondió: eso es lo que
hay que corregir en los skills.

## 5 · Resultados

| # | Comprobación | Claude Code | Copilot | Notas |
| --- | --- | --- | --- | --- |
| 1 | Instalación o actualización sin conflictos | | | |
| 2 | Skills visibles | | | |
| 3 | `story.md` preparado con `new-sdd-item.py` y el comprobador sin errores | | | |
| 4 | `enrich-us` abrió la imagen (o usó la descripción y lo dijo) | | | |
| 5 | `story.md` sin cambios después de `enrich-us` | | | |
| 6 | Criterios propuestos solo a partir de la descripción, marcados para validar | | | |
| 7 | Bitácora con preguntas, respuestas y decisiones | | | |
| 8 | `pbi.md` correcto y sin decisiones perdidas | | | |
| 9 | Diseño 00–06 coherente con la arquitectura de Bonis | | | |
| 10 | Implementación con pruebas primero y build/test en verde | | | |
| 11 | Traducciones en todos los idiomas (si aplica) | | | |
| 12 | `commit-message.md` válido según el comprobador | | | |
| 13 | Contexto consumido por paso (`/context`) | | | |
| 14 | Tiempo total, incluida la preparación de `story.md` | | | |

Si solo pruebas con una herramienta, deja la otra columna vacía.

## 6 · Qué enviar para revisar

- La carpeta `docs\sdd\40944-rsp-ubicacion-seguimiento-del-servicio\` completa (en un zip).
- La salida del comprobador en cada paso.
- La tabla de resultados y lo que te haya sorprendido.

## Volver atrás

```powershell
git checkout dev
git branch -D chore/sdd-kit-piloto
```
