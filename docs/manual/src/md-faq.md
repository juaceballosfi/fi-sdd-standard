## Preguntas frecuentes

Respuestas cortas a las dudas que más atascan. Cada una remite a la sección con el detalle.

### Instalación y herramientas

**No veo las skills al escribir `/`.**
Cierra y vuelve a abrir la herramienta: las skills, agentes y hooks se cargan al arrancar. En Claude
Code deben existir `.claude/skills/<skill>/SKILL.md` (si no, instalaste solo `--tools copilot`:
vuelve a ejecutar `install.py --tools copilot,claude`). En VS Code, `.agents/skills/`. (5, 17.1)

**¿Tengo que hacer commit de `.claude/skills/` y `.claude/agents/`?**
No. Son copias locales que `install.py` genera en cada equipo y añade al `.gitignore`. Sí se
versionan `.agents/`, `.github/agents/`, `.github/prompts/` y `.claude/settings.json`. (5.6)

**¿Qué de la carpeta del work item va al repositorio?**
Casi todo: `story.md`, `bitacora.md`, `pbi.md`/`bug.md`, `00`–`06` o `fix-plan.md`, `CHANGELOG.md`,
`qa-report.md` y `test-cases.md`. No van `assets/` (los adjuntos están en Azure DevOps),
`commit-message.md` (queda en el commit) ni `test-cases.csv` (se regenera). Ya están en `.gitignore`,
así que `git add <carpeta>` los salta solo. (3.3, ADR-0027)

**`/project-context` encontró un problema del proyecto (un secreto, un script roto). ¿Lo arregla?**
No. Lo deja como borrador en `docs/sdd/_borradores/` con su prioridad (Urgente, Alta, Media, Baja) y
sigue: su trabajo es dejar el kit listo. Crea los urgentes en Azure DevOps en cuanto hagas el commit.
Si se pone a depurar una herramienta, dile que lo anote en un borrador y siga. (8.1, ADR-0028)

**`/project-context` se para nada más empezar.**
O falta el commit de la instalación, o el entorno no compila (`dotnet restore` con 401, un enlace
roto, un submódulo vacío). Te da los pasos; arréglalo tú y vuelve a lanzarlo. (17, *Entorno y
project-context*)

**`pr-check.py` da error por un borrador.**
Los borradores de `docs/sdd/_borradores/` no llegan a `dev`. Crea el work item en Azure DevOps, anota
su ID donde se citaba el borrador (`bitacora.md`, `qa-report.md`) y borra el archivo. (13.6, 14.2)

**Retomo un work item en otro equipo y faltan las imágenes.**
Los adjuntos no se versionan. Bájalos del work item en Azure DevOps a `assets/` con los nombres que
enlaza `story.md`; `check-sdd-item.py` lo avisa. (10.2)

**El instalador dice `PENDIENTE` o `CONFLICTO`. ¿Lo he roto?**
No. `PENDIENTE` es un paso tuyo (casi siempre `/project-context`). `CONFLICTO` significa que ya
existe un archivo con ese nombre que no es del kit y no se ha tocado: decide a mano cuál se queda.
(5.2)

**Edité una skill instalada y `pr-check.py` da error.**
Las skills instaladas no se editan: el cambio se hace en el kit (`core/`) y se reinstala con un
commit `chore(sdd): actualizar fi-sdd-standard a v<versión>`. Revierte tu cambio en la copia. (4.2,
11.4)

**¿Qué modelo uso en cada paso?**
Razonamiento (Opus) para `enrich-us`, `technical-analysis`, `project-context` y `qa-review`; Sonnet
para `wbs-execution`, `quick-fix` y `test-cases` (en Claude Code ya va fijado; en Copilot usa
`/wbs-execution-sonnet` o elígelo en el chat). (4.4, 16.6)

### Flujo y skills

**La skill me pregunta el ID aunque lo escribí.**
En Copilot la skill no recibe los argumentos: escribe el ID en la misma línea del comando,
`/enrich-us 40399`. (6.1, 17.2)

**`/enrich-us` dice que no hay `story.md`.**
Crea la carpeta con `python <kit>\scripts\new-sdd-item.py <id> "<título>"` (añade `--tipo bug` para
un bug), copia el work item de Azure DevOps literal en `story.md`, guarda las imágenes en `assets/`
y vuelve a lanzar `/enrich-us <id>`. (6.2, 10.2)

**La IA me pide un dato de negocio que no sé.**
Responde «No lo sé: déjalo pendiente, se lo pregunto al PO». Quedará `[PENDING-BUSINESS: …]`.
Cuando tengas la respuesta, díselo con quién la dio («lo confirmó Laura Gómez hoy») y la IA quita
el marcador en todos los archivos. No le pidas que «ponga lo lógico». (13.1, 16.2)

**`/technical-analysis` se para por campos pendientes.**
`pbi.md` tiene `[PENDING-BUSINESS]`. Opción A (recomendada): resuélvelos antes. Opción B: seguir;
las secciones afectadas saldrán `[ASSUMPTION-BASED]` y `wbs-execution` volverá a preguntar. (6.3)

**Se cortó la sesión a mitad de `/wbs-execution`.**
Abre una sesión nueva y lanza `/wbs-execution <id>`: lee el estado en `05-wbs-estimation.md`, ejecuta
build y pruebas y sigue por la primera tarea pendiente. Para empezar en una concreta,
`from:T-04`. (6.4, 15.7)

**El diseño aprobado no se puede implementar tal cual.**
`wbs-execution` se para con *Desviación de diseño* y propone el ajuste mínimo. Si lo apruebas, se
actualizan primero `03`/`04` (nueva versión y quién aprobó) y luego sigue. No le pidas que «lo haga
como crea mejor» sin actualizar el diseño. (15.6)

**`/qa-review` dice que debe ejecutarse en una sesión nueva.**
Es intencionado: quien implementó no revisa su propio trabajo. Abre otra conversación y vuelve a
lanzarlo. (6.5)

**¿Qué hago con los hallazgos de QA?**
Decide cada Alta y Media: A) corregir, B) aceptar el riesgo (con tu nombre), C) work item aparte.
Los «A corregir» se arreglan con `/wbs-execution <id> qa` (nunca en la sesión de QA) y se verifican
con `/qa-review <id>` en otra sesión nueva (ronda 2, la última). (6.5, 15.5)

**`/quick-fix` dice «No es una corrección rápida».**
El bug no pasa uno de los 8 criterios (migración, contrato, permisos, más de 3 archivos…). Sigue el
flujo completo con `/enrich-us <id>`: la causa ya encontrada está en `bitacora.md`. No se fuerza la
compuerta. (7.1, 15.3)

**Un caso de prueba sale «Bloqueado».**
Su criterio está *A confirmar* o le falta un dato (`[PENDING-BUSINESS]`). Cuando el PO responda,
vuelve a lanzar `/test-cases <id>`; los bloqueados no van al CSV salvo con `--include-blocked`.
(7.3)

**¿Puedo saltarme `qa-review` o `document-code`?**
El flujo los espera antes del PR; `document-code` avisa si no hay `qa-report.md` y pregunta si sigue.
Saltarlos deja el PR sin la revisión independiente o sin documentación. (3.1, 6.6)

### Git y PR

**`nothing added to commit` al hacer el commit.**
Faltó `git add`. Añade las rutas exactas que te dio la skill al cerrar (también los archivos nuevos,
`??`) y la carpeta del work item; comprueba con `git status --short`; luego
`git commit -F docs/sdd/<carpeta>/commit-message.md`. (14.2)

**`pr-check.py` da error en el commit.**
Revisa el formato: primera línea `tipo(ámbito): descripción` (≤ 72 caracteres), `Ref: #<id>` al
final, sin `fix #id` y sin `Co-Authored-By`. Corrige con `git commit --amend -F <archivo>` antes
del push. (11.3, 14.1)

**Tengo varios commits en la rama.**
Antes del push: `git reset --soft origin/dev` y un solo commit con `-F commit-message.md`. Después
del push, el *squash* del PR los junta. (14.2)

**Se cerró el work item solo al mezclar.**
El mensaje tenía `fix #id`. Reábrelo a mano en Azure DevOps y usa siempre `Ref: #id`. (14.1)

**¿Puedo borrar la rama si `git branch -d` no me deja?**
Sí, con el PR completado: `git branch -D <rama>`. Con *squash*, git no la reconoce como mezclada.
(14.2)

### Guardarraíles y secretos

**El hook bloquea un archivo que necesito leer.**
Si es un archivo de entorno (`appsettings.Development.json`, `.env`), el bloqueo es correcto: pide
el dato a una persona sin pegar credenciales. Si de verdad no tiene secretos (una plantilla
`.env.example`), añádelo a `secretsAllowed` de `sdd-guardrails.json` y justifícalo en el PR.
(12.3, 12.4)

**«bloqueado: … es una ruta protegida».**
La ruta está en `protected` de `sdd-guardrails.json` (librería compartida, submódulo, código
generado). El cambio se hace en su origen, no en este repositorio. (12.3)

**El hook no hace nada.**
Reinicia Claude Code, comprueba que `python` está en el PATH y pruébalo a mano: debe salir con 2
al leer un archivo de entorno (12.3, *Probarlo a mano*). En Copilot no hay hooks: ahí cuentan las
pruebas de arquitectura y `pr-check.py`. (12.1)

**Falla una prueba de arquitectura.**
El cambio rompe una regla (un controller con `DbContext`, un endpoint sin autorización, Datos que
usa Servicios). Se corrige el código; añadir una excepción lo decide el tech lead y lleva su
motivo. (12.5)

### Windows y codificación

**Veo `Ã©` o `├®` en lugar de tildes.**
Es la consola de PowerShell 5.1, no el archivo. Para leer: `Get-Content -Encoding UTF8 <archivo>`.
Para guardar un mensaje de commit: `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"`. Si un
archivo dejó de ser UTF-8: `python .agents\scripts\check-encoding.py --fix`. (17.4)

**`warning: LF will be replaced by CRLF`.**
Es inofensivo. No cambies `core.autocrlf` por esto. (17.3)

**Los avisos del build no cuadran con la línea base.**
Compila siempre igual (`dotnet build <solución> --no-incremental`) y compara con
`doc_coverage.py --warnings <log> --compare docs/sdd/_documentacion/avisos.md`, que quita duplicados
y aparta los `NU19xx` de NuGet. (11.10, 17.7)
