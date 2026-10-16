# CHANGELOG — fi-sdd-standard

## v0.12.0 — 2026-10-16 · Qué se versiona y el manual en el kit

- **Qué se versiona (ADR-0027, sustituye en parte a ADR-0002).** De cada work item ya no se suben
  `assets/` (los adjuntos están en Azure DevOps), `commit-message.md` (queda en el commit y en el
  PR) ni `test-cases.csv` (se regenera). Los borradores de `docs/sdd/_borradores/` no llegan a
  `dev`: se crea el work item, se anota su ID y se borran antes del PR.
  - **`install.py`** añade al `.gitignore` del proyecto esas rutas, `.claude/settings.local.json`,
    `.github/copilot-instructions.md` (solo si lo generó el kit) y `.agents/**/__pycache__/`.
    Avisa (`REVISAR`) de los que ya estaban versionados, sin borrar nada.
  - **`check-sdd-item.py`:** un adjunto enlazado que falta y que git ignora es un aviso, no un
    error. El paso 5 se reconoce por el último commit de la carpeta con `Ref: #<id>`, y ese es el
    mensaje que se comprueba.
  - **`pr-check.py`:** error si la rama añade o cambia un borrador; aviso si sube un archivo local
    a propósito. Ya no deja `__pycache__/` en `.agents/scripts/`.
  - **Skills v3.9:** la convención compartida de borradores, `commit-message.md` como archivo
    local, el CSV de `test-cases` local, los adjuntos desde Azure DevOps en otro equipo
    (`enrich-us`) y el estado `Work item #<ID>` de un hallazgo de QA que se creó.
  - `AGENTS.base.md`: una línea con lo que no se versiona. Guías rápidas, guía git y
    `piloto-a-dev.md` actualizadas.
- **Manual en el kit:** `docs/manual/` con el PDF, el Markdown (para dar de contexto a una IA) y
  sus fuentes (`build.py`, `build_md.py`, `diagrams.py`, `src/`, `assets/`). No se instala en los
  proyectos. Capítulos 3, 5, 14 y relacionados actualizados con ADR-0027.

## v0.11.0 — 2026-10-15 · Candidata a MVP (fases 1 a 3)

Todo lo del MVP construido, para probarlo por olas con `tests/pilots/PLAN-PRUEBAS-MVP.md`.

- **Guardarraíles (ADR-0023, fase 3):**
  - **Permisos:** `install.py` añade a `.claude/settings.json`, sin pisar lo existente, 20 reglas
    `deny`. Bloquean la lectura de `.env*`, `appsettings.*.json`, `secrets.json` y certificados, y
    `git commit`, `git push`, `git reset --hard`, `git clean`, `git branch -D` y borrados
    recursivos. También registra los hooks. Avisa si `.gitignore` ignora `.claude/settings.json`.
  - **Hook `.agents/hooks/sdd_guard.py`** (Python, sin dependencias), configurado en
    `sdd-guardrails.json`:
    - bloquea rutas protegidas y archivos de secretos, también desde Bash y PowerShell;
    - después de editar, formatea, avisa si el archivo ya no es UTF-8 y avisa de los patrones.
  - **`pr-check.py`** en `.agents/scripts/`. Comprueba:
    - los commits de la rama;
    - la codificación;
    - los work items cambiados;
    - rutas protegidas y archivos de secretos;
    - archivos del kit cambiados a mano;
    - el tamaño de `AGENTS.md`;
    - secretos en el diff.
  - **Pruebas de arquitectura** (plantilla xUnit sin paquetes):
    - controllers sin `DbContext`;
    - todo endpoint con autorización;
    - la capa de datos sin dependencias de los servicios.

    `/project-context` las crea, rellena `sdd-guardrails.json` y sustituye los hooks de Clavijo
    que cubre el kit. `check_project.py` comprueba los dos.
  - **Matriz regla → comprobación** en el ADR.
- **Vía rápida `quick-fix` (ADR-0024):** una compuerta de 8 criterios, `bug.md` y `fix-plan.md`,
  una tarea con prueba primero y verificación propia. `qa-review`, `document-code` y
  `check-sdd-item.py` reconocen el ítem.
- **QA (ADR-0025):**
  - `/enrich-us <id> qa` clasifica cada criterio en Definido / Deducción directa / A confirmar;
  - skill `test-cases`: casos por criterio, sin datos inventados, y el CSV de Azure Test Plans
    (`test_cases_csv.py`);
  - `qa-review` comprueba los casos de prioridad alta.
- **`migration-reviewer` estable:** una lista de comprobación de 8 puntos.
  `wbs-execution` lo exige en las tareas con migración.
- **Bucle de pipeline en rojo → fase 4** (ADR-0026).
- **`check-sdd-item.py`:**
  - `Ref:` es opcional en commits `docs`, `chore`, `ci` y `style` (aviso, no error);
  - `Co-Authored-By` y `Generated with` son errores.
- **Compatibilidad y MCP:**
  - `tests/compat/README.md` con el protocolo por herramienta (carga C1–C6 y flujo completo);
  - plantillas del MCP en `core/templates/mcp/` y la guía `docs/guias/mcp-azure-devops.md`.
- **Guías:** `guia-rapida-dev.md`, `guia-rapida-qa.md` y `piloto-a-dev.md`.
- **El kit es un repositorio git** (fase 0), con la etiqueta `v0.11.0`.
- **`install.py`:** ignora `__pycache__` y añade `quick-fix` y `test-cases` con Sonnet en Claude Code.
- **Convención compartida:** 9 skills.

## v0.10.2 — 2026-10-15 · Ajustes tras el plan de Bonis

- **`document-project`:** si el proyecto genera el XML pero suprime CS1591 (`NoWarn`), la línea
  base lo cuenta con un build aparte (`-p:NoWarn=`) y guarda el comando exacto para cada bloque.
- **`doc_coverage.py`:** las partes de un área siguen un solo orden alfabético (antes, las entidades
  con configuración iban después de las que no la tienen).
- **`document-project`:** los comandos del plan usan `.agents/skills/` (versionado), no `.claude/`.
- **Resultados de B-01 en Bonis:**
  - `comment_only.py` falló en la consola de Windows al imprimir ✓; ahora fuerza UTF-8;
  - `doc_coverage.py` ya no da por no documentado un símbolo con un `//` entre el `///` y la
    declaración;
  - `doc-writer`: sin números de línea en comentarios ni en `docs/` (se quedan viejos), sin listas
    de quién usa un símbolo y sin copiar nunca un literal sensible;
  - `code-explorer`: los `appsettings*.json` solo se leen por sus secciones, y un literal sensible
    se informa como `ruta:línea — literal sensible`, sin copiar su valor;
  - `doc_coverage.py --warnings <log> [--compare <informe>]`: los avisos de un build por código y
    archivo, con los `NU19xx` aparte, y los nuevos frente a un informe anterior. En Bonis explica
    los «226 frente a 222»: 222 avisos de código más 2 de NuGet que MSBuild cuenta dos veces;
  - `document-project`: la línea base y cada bloque compilan con `--no-incremental` (un build
    incremental dio 15 avisos) y comparan con `docs/sdd/_documentacion/avisos.md`, sin worktrees;
    la sesión principal no parchea comentarios, ni siquiera un `//`;
  - `doc-writer`: en los comentarios XML, los nombres van en `<c>` o `<see cref>`, no entre
    comillas invertidas.
- **`AGENTS.base.md`:** las respuestas al usuario también van en español (la repetición del plan en
  Bonis respondió en inglés).

## v0.10.1 — 2026-10-15 · El plan de `/document-project` lo parte el script

Primera prueba del plan en Bonis (`tests/pilots/bonis/RESULTADOS-DOCUMENT-PROJECT.md`): la sesión
partió a mano las áreas grandes por orden alfabético, separó las entidades de sus configuraciones,
dio una cifra estimada y no comprobó el plan escrito. El script tenía dos fallos de clasificación.

- **`doc_coverage.py --areas`:**
  - parte las áreas grandes sin separar una entidad de su configuración EF, una interfaz de su
    clase ni las partes de una clase parcial;
  - propone los bloques y marca `completa` las áreas sin nada que documentar;
  - ordena lo transversal por dependencia: base, autorización, errores y middleware → datos →
    modelos → servicios → el resto;
  - un controlador es base solo si es abstracto o si otro controlador hereda de él (antes,
    `MaximumBaseController` contaba como base por el nombre);
  - los archivos de infraestructura (`Authorization`, `Middlewares`, `Startup`…) no se llevan a un
    controlador, y un atributo `XAttribute` se busca también como `X`;
  - las pruebas se asocian también por prefijo (`MaximumBaseControllerAuthorizationTests`).
- **`doc_coverage.py --check-plan`:** comprueba el `plan.md` escrito: cada archivo con algo que
  documentar en un área y solo en una, sin archivos desconocidos, áreas y bloques dentro de los
  límites.
- **`document-project`:** el plan usa las áreas, partes y bloques del script y solo corrige lo que
  el script no puede saber; toda cifra sale de un script o un comando; después de escribir el plan,
  `--check-plan` con 0 errores. El modelo estándar basta para el plan.

## v0.10.0 — 2026-10-15 · `/document-project`

- **Skill nuevo `document-project` v3.8 (ADR-0022, aceptada):** documenta todo el proyecto una vez,
  después de `/project-context`.
  - **Plan reanudable** en `docs/sdd/_documentacion/plan.md`: áreas, bloques, estados, hallazgos y
    registro; cada bloque deja `B-NN.md` con su validación y su mensaje de commit.
  - **Por bloques:** 3 a 5 áreas, unos 40 archivos; un bloque por sesión, un commit y un PR.
  - **Orden:** transversal del backend → controladores (los más cambiados primero) → transversal del
    frontend → secciones del frontend.
  - **Garantías de `document-code`:** `doc-writer` escribe, `comment_only.py` comprueba, sin avisos
    nuevos en build, lint, tipos y DocFX; la sesión revisa las afirmaciones contra el código.
  - **Pruebas existentes:** resumen por clase, con su área.
  - Modos: plan, bloque (`block:B-NN`, `area:A-NN`) y `status`.
- **`doc_coverage.py`** (dentro del skill): cobertura de comentarios de C# y TypeScript por carpeta,
  propuesta de áreas (controlador + servicios propios + tipos propios), símbolos sin documentar por
  archivo y avisos CS1591 de un log de build.
- **`doc-writer`:** acepta símbolos «desde el código» (qué hace, nunca la intención) y resúmenes de
  clases de prueba; el porqué cita su fuente (`#<ID>` o ADR).
- **Convención compartida:** la lista de skills incluye `document-project` (los siete skills).
- **`install.py`:** sugiere `/document-project` cuando ya hay contexto y no hay plan.
- **ADR-0014:** `document-project` en la tabla de modelos (plan: razonamiento; bloques: estándar).

## v0.9.3 — 2026-10-15 · Modelo por defecto del sello

- **Convención compartida:** el sello pone `<model>` (ya no «if known»). Si la sesión no puede saber
  qué modelo la ejecuta, escribe el modelo por defecto del equipo, `claude-opus-5-5`.
- **ADR-0014:** tabla de modelos por nivel y modelo por defecto del sello, con fecha de revisión.

## v0.9.2 — 2026-10-15 · `/project-context check`

- **Modo `check`:** una pasada corta para dejar limpio `check_project.py`, sin inventario ni build.
  Convierte cada aviso en una resolución:
  - presupuesto o tamaño → el detalle pasa a `docs/` con `doc-writer`;
  - secciones vacías → búsqueda dirigida;
  - `[REQUIRES-VALIDATION]` → qué verificar, cómo y quién;
  - fuentes cambiadas → se actualizan solo las secciones afectadas.
- **`check_project.py`:** lista el texto de cada `[REQUIRES-VALIDATION]` abierto.

## v0.9.1 — 2026-10-15 · Ajustes tras `/project-context` en Bonis

Resultados en `tests/pilots/bonis/RESULTADOS-PROJECT-CONTEXT.md`: mejor que el `AGENTS.md` hecho a
mano (4 correcciones, 11 añadidos, 2 datos perdidos, nada inventado).

- **Presupuesto por sección** en *Project context* (`max N lines`, unas 120 líneas en total).
  `check_project.py` avisa de lo que se pasa y del tamaño a partir de 185 líneas.
- **La plantilla pide** el servidor de desarrollo y las versiones de las herramientas en local y en
  CI. `inventory.py` lee las versiones de los pipelines.
- **`project-context`:** los documentos que escribe `doc-writer` no se parchean en la sesión
  principal.
- **Convención compartida:** el sello lleva el modelo de la sesión que ejecuta el skill.
- **`inventory.py`:** marca las acciones con el nombre repetido en un controlador.
- **Versión del instalador:** 0.9.1. Los skills siguen en v3.8.

## v0.9.0 — 2026-10-15 · `/project-context` y cierre del bloque 4

- **Skill nuevo `project-context` v3.8 (ADR-0021):** es el primer paso después de `install.py`.
  - **Inventario determinista** con `inventory.py`: manifiestos, archivos de bloqueo, pipelines,
    submódulos, documentación y DocFX, traducciones, pruebas, Entity Framework, configuración de IA
    previa y endpoints REST.
  - **Exploración en paralelo** con `code-explorer`.
  - **Ejecuta** build, pruebas, lint y comprobación de tipos, y registra la línea base.
  - **Pregunta** en un solo bloque lo que el código no dice.
  - **Crea el proyecto de pruebas** con `backend-dev` si no hay ninguno.
  - **Escribe** *Project context* con 11 encabezados fijos y los seis `docs/*.md` base.
  - **Propone** la integración con DocFX y la migración de una configuración de IA previa.
  - Modos `new`, `update` y `fresh`.
- **`check_project.py`** (dentro del skill) comprueba:
  - los encabezados fijos y el tamaño de `AGENTS.md`, y el sello;
  - si las fuentes cambiaron después de la fecha del contexto;
  - `CLAUDE.md`, los seis `docs/*.md` y que haya proyecto de pruebas.
- **Instalador:**
  - ya no crea los `docs/*.md` vacíos;
  - la plantilla de `AGENTS.md` deja *Project context* para el skill;
  - al terminar sugiere `/project-context`.
- **`doc-writer`** también escribe los `docs/` de `project-context`.
- **ADR-0022 (propuesta):** `/document-project`, la documentación inicial y completa, por áreas y
  en varias sesiones.
- **`tests/pilots/PRUEBA-PROJECT-CONTEXT.md`:** Bonis (`fresh`, comparación) y Calls4Grants
  (instalación real).

### Ajustes tras la prueba del bloque 4

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE4.md`.

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE4.md`.

- **`doc-writer`:**
  - `<param>` va en todos los parámetros o en ninguno (CS1573); un solo parámetro se explica en
    `<remarks>`.
  - En `docs/`, una sola referencia `(#ID)` por sección.
- **`document-code`:** la sesión principal no parchea comentarios con scripts. Si algo falla,
  vuelve a `doc-writer` o el archivo se restaura.
- **`comment_only.py restore`:** devuelve un archivo a su copia guardada.
- **Guía git:** las tildes que se ven mal en `Select-String` son de la consola.

## v0.8.0 — 2026-10-15 · Fase 2, bloque 4: documentación del código

- **Skill nuevo `document-code` v3.7 (paso 5, ADR-0020):**
  - Toma los archivos del item del CHANGELOG y decide qué documentar, cada cosa con su fuente
    (`BR-XX`, `SPEC-XX`, 03).
  - Documenta: comentarios `///` y TSDoc en lo nuevo o cambiado, comentarios del porqué donde una
    decisión no es obvia, el resumen de las clases de prueba nuevas y las secciones afectadas de
    `docs/`.
  - Propone una ADR si el diseño tomó una decisión de arquitectura, preguntando antes.
  - Registra la documentación en el CHANGELOG del item, la bitácora y el mensaje de commit.
- **`scripts/comment_only.py`** (dentro del skill): guarda los archivos antes y comprueba después
  que solo cambiaron comentarios o líneas en blanco, y que se conservan el BOM y los finales de
  línea.
- **`doc-writer` pasa a estable:**
  - Modelo rápido, lectura y edición.
  - Escribe con un paquete cerrado de símbolos y hechos; lo que no puede fundamentar lo deja fuera
    y lo informa.
- **`check-sdd-item.py`:** `✓ documentación` si el CHANGELOG tiene la entrada «Documentación»; si
  no, «sin documentar» como información.
- **Flujo:** `wbs-execution` y `qa-review` indican `/document-code` como siguiente paso.
  `AGENTS.base.md` lo incluye entre los pasos que confirma la persona.
- **`tests/pilots/bonis/PRUEBA-BLOQUE4.md`:** protocolo con el 40933.

## v0.7.1 — 2026-10-15 · Cierre del bloque 3

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE3.md`. Seguimiento del 40933 en el PR 14472.

- **Convención compartida (skills v3.7):**
  - *Registro* y *Hallazgos* de la bitácora solo crecen: nunca se edita una línea anterior.
  - Los nombres de las personas, siempre igual y sin formato.
- **`wbs-execution`:** el mensaje de commit se escribe entero a partir del CHANGELOG tras el último
  cambio, también en el modo `qa`; nunca se parchea.
- **`qa-review`:**
  - El *Resultado* del informe muestra el estado actual de todos los hallazgos.
  - Los archivos del item salen del CHANGELOG.
  - No propone `runtime-tester` si el usuario local no puede tener el rol que hace falta.
  - El informe recoge los procesos detenidos y los datos locales creados.
- **`backend-dev` y `frontend-dev`:** en las tareas que solo añaden pruebas, *Rojo* por mutación
  temporal, revertida, y con `git diff --stat` de producción vacío.
- **`tests/pilots/bonis/AGENTS.md`:**
  - *Runtime checks*: usuario fijo en Debug.
  - Pruebas del frontend en `src/tests/`, sin `@testing-library`.
  - Comprobación de tipos con tsconfig temporal y línea base de unos 148 errores.
- **ADR-0019:** confirmada.

## v0.7.0 — 2026-10-14 · Fase 2, bloque 3: revisión de QA

- **Skill nuevo `qa-review` v3.6 (paso 4, ADR-0019):**
  - Se ejecuta en una sesión nueva sobre un rango `base..head`; por defecto, la rama frente a
    `origin/dev`.
  - Delega en `qa-reviewer`, y en `runtime-tester` si la persona lo acepta.
  - Verifica cada hallazgo y escribe `qa-report.md`.
  - La persona decide los hallazgos altos y medios: `A corregir`, `Aceptado` o `Borrador`.
  - Como mucho 2 rondas.
- **`qa-reviewer` y `runtime-tester` pasan a estables.**
  - `qa-reviewer` (razonamiento) recibe fuentes, no conclusiones. Cada hallazgo lleva
    `archivo:línea`, la regla rota, un escenario y cómo se confirmó.
  - `runtime-tester` arranca la aplicación solo en local y devuelve «No ejecutado» cuando no
    puede arrancarla.
  - Ninguno de los dos edita.
- **`wbs-execution` · modo `qa`:** `/wbs-execution <id> qa` corrige los hallazgos `A corregir`:
  - con el agente de su capa y una prueba que reproduce el hallazgo primero;
  - marca `Corregido` en `qa-report.md`;
  - actualiza el CHANGELOG y el mensaje de commit.
- **Plantilla `qa-report.md`:**
  - Pasa de `core/templates/` a `core/skills/qa-review/templates/`.
  - Nuevas secciones: ronda, alcance, ancla `sdd:qa-findings`, estados de cada hallazgo y la tabla
    «Qué se revisó».
- **`check-sdd-item.py`:**
  - Lee `qa-report.md`: sello, y error si queda algún hallazgo alto o medio sin decidir.
  - Muestra «sin revisión de QA» como información, sin contarlo como aviso.
- **`AGENTS.base.md`:** `qa-review` se ejecuta en una sesión nueva.
- **`docs/guias/git-por-work-item.md`:**
  - Del commit al merge: el flujo normal y la variante del piloto con *cherry-pick*.
  - Los avisos de git que no son errores.
- **`tests/pilots/bonis/PRUEBA-BLOQUE3.md`:** protocolo con el PBI 40933, ya en `dev`.

## v0.6.1 — 2026-10-14 · Ajustes tras la prueba del bloque 2

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE2.md`.

- **Skills v3.6:**
  - **Convención *Large inputs*:** la salida de build, pruebas y lint va a un archivo y en la
    conversación solo queda el resumen. Los cambios se revisan con `git diff --stat`.
  - **`wbs-execution` · documentos:** una edición por archivo y tarea; no se repite la tabla del
    WBS ni se marca «En curso».
  - **`wbs-execution` · agente parado:** se revisa lo que dejó, se reanuda una vez con «Ya hecho»
    y «Falta», y a la segunda decide la persona.
  - **`wbs-execution` · *Rojo*:** si el informe no trae la línea *Rojo*, se registra como
    desviación y se comprueba la caracterización contra `HEAD`.
  - **`wbs-execution` · cierre:**
    - Barrido de marcadores ya resueltos antes del mensaje de commit.
    - Rutas exactas para el commit, nunca `git add -A`.
    - El siguiente paso es `/qa-review` en una sesión nueva.
  - **`technical-analysis`:** divide en dos las tareas de más de 2 SP que reestructuran código y
    además cambian comportamiento, y las que tocan varias zonas de un archivo enorme.
- **`backend-dev` y `frontend-dev`:**
  - Las pruebas se ejecutan antes de tocar cualquier archivo de producción.
  - El informe trae *Rojo* (o *Caracterización*) y *Verde*.
  - Si se rompió el orden, el agente lo declara como desviación.
- **`check-sdd-item.py`:** no dice «listo para commit» si hay errores o marcadores abiertos.
- **ADR-0018:** confirmada, con la reanudación de un agente parado en la tabla de bucles.

## v0.6.0 — 2026-10-14 · Fase 2, bloque 2: implementación delegada

- **`backend-dev` y `frontend-dev` pasan a estables** (ADR-0018):
  - Implementan una sola tarea con un paquete cerrado, con las pruebas primero.
  - Hacen como mucho 3 intentos por comprobación.
  - No tocan `docs/sdd/`, no hacen commit y se detienen ante cualquier decisión.
  - Devuelven un informe fijo (Estado · Cambios · Archivos · Pruebas · Validación · Hallazgos).
  - `frontend-dev` hace las traducciones en todos los idiomas y, si no hay herramientas de prueba
    de componentes, deja los pasos de verificación manual.
- **Skills v3.5:**
  - `wbs-execution` elige el agente con la columna Rol del WBS, monta el paquete y delega.
  - Verifica por su cuenta: build, pruebas, lint y alcance con `git status`.
  - Bucles con límites (3 intentos del agente, 2 rondas de verificación). El diseño cambia solo
    con 03/04 aprobados.
  - Paralelo opcional: como mucho 2 agentes, con archivos disjuntos.
  - Solo la sesión principal escribe en la carpeta del work item.
  - `technical-analysis` usa la columna Rol para dividir las tareas que tocan dos capas.
- **`tests/pilots/bonis/PRUEBA-BLOQUE2.md`:** protocolo con el PBI 40933.

## v0.5.2 — 2026-10-14 · Cierre del bloque 1

Prueba con el PBI 40933. Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE1.md`.

- **Contexto:** `technical-analysis` bajó de 551k a 202k tokens, con mejor diseño. `enrich-us` se
  quedó en 105k.
- **Skills v3.4:**
  - Convención compartida *Resolved markers*: un marcador resuelto se quita en todos los archivos
    de la carpeta, incluido `pbi.md`.
  - `technical-analysis` no vuelve a verificar cada respuesta de `code-explorer`: solo las líneas
    que serán causa raíz o contrato, con unas 20 líneas como mucho por comprobación.
- **`check-sdd-item.py`:** avisa de los `[REQUIRES-VALIDATION]` abiertos en `pbi.md`/`bug.md` y en
  00–06, sin contar la nota de la plantilla de 01.

## v0.5.1 — 2026-10-14 · Ajustes tras la prueba directa de `code-explorer`

- `code-explorer` busca siempre las pruebas que cubren los archivos que cita. En Claude Code (Haiku)
  respondió «no las busqué» aunque `nav-items.test.ts` existe.
- La cabecera de las copias generadas usa solo ASCII: `Get-Content` de PowerShell 5.1 mostraba la
  raya «—» como «â€”».
- `PRUEBA-BLOQUE1.md`: Claude Code ya no tiene el asistente `/agents`. Se comprueba el archivo y se
  pregunta en una sesión nueva.

## v0.5.0 — 2026-10-14 · Fase 2, bloque 1: `code-explorer`

- **`code-explorer` pasa a estable:**
  - Busca primero y lee por rangos.
  - Abre como mucho 15 archivos, no lee archivos generados ni secretos y no modifica nada.
  - Responde en español en menos de 60 líneas (Respuesta · Archivos · Patrones · Pruebas · No
    cubierto).
- **`install.py` instala los agentes con `status: stable`** (ADR-0017):
  - `.github/agents/<nombre>.agent.md`, versionado, para Copilot en VS Code y Visual Studio; solo
    como subagente (`user-invocable: false`).
  - `.claude/agents/<nombre>.md`, local y en `.gitignore`, con las herramientas de Claude Code y
    `model: haiku` para el nivel rápido.
- **Skills v3.3:**
  - Nueva convención compartida *Code exploration*: las búsquedas amplias se delegan en
    `code-explorer` (Agent en Claude Code, `runSubagent` en VS Code), con preguntas en paralelo, y
    se conserva solo la respuesta.
  - `technical-analysis` mapea el código con `code-explorer` antes del resumen de confirmación.
- **`validate.py`:** el estado de los agentes es `draft` o `stable`, y un agente estable debe decir
  cuándo usarlo.
- **`tests/pilots/bonis/PRUEBA-BLOQUE1.md`:** protocolo de prueba del bloque 1.

## v0.4.2 — 2026-10-14 · Codificación de los archivos

- En la PR del 40944, Azure Repos mostró `useDashboard.ts` como «utf-8 -> Windows-1252». El
  archivo nuevo era UTF-8 válido. La causa probable es que la IA, al reescribirlo, quitó el BOM
  que tenía en `dev`, o que Azure lo adivina mal cuando el archivo se queda sin caracteres no
  ASCII.
- **`scripts/check-encoding.py --base origin/dev [--fix]`**:
  - Comprueba que los archivos de texto cambiados en la rama están en UTF-8.
  - Avisa si un archivo ha ganado o perdido el BOM respecto a la rama base.
  - Con `--fix` repara los archivos que mezclan UTF-8 y Windows-1252, que es lo que pasa al editar
    en Windows con scripts sin `encoding="utf-8"`, y deja el BOM como estaba en la base.
  - Se reutilizará en la validación del PR (fase 4).
- `AGENTS.base.md`: guardar siempre en UTF-8, conservar el BOM existente y pasar la codificación
  al editar con scripts.

## v0.4.1 — 2026-10-14 · Commits: uno por work item y sin firma de IA

- ADR-0004 ampliado con dos decisiones del 2026-10-14:
  - Un commit por work item.
  - Sin `Co-Authored-By` ni otros trailers de IA; la evidencia es el sello «Generado con».
- Lo recogen `wbs-execution` y `AGENTS.base.md`.
- `check-sdd-item.py --commit-message` lee también archivos en UTF-16 o con BOM, que es lo que
  genera `git log … > msg.txt` en PowerShell 5.1.
- Si el mensaje llega con las tildes o la raya «—» estropeadas (redirección `>` de PowerShell), el
  comprobador lo avisa y propone `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"`. `PRUEBA.md` usa ese comando.

## v0.4.0 — 2026-10-14 · Ajustes tras el primer piloto en Bonis

Primer piloto completo: PBI 40944 de Bonis, con Claude Code. Resultados en
`tests/pilots/bonis/RESULTADOS-40944.md`; decisiones en ADR-0016.

- **Skills v3.2**, convenciones compartidas:
  - **Entradas grandes:** primero se busca y, de los archivos grandes, se leen solo los rangos
    necesarios. Los logs se piden como archivo. El análisis técnico del piloto llegó a 551k tokens,
    sobre todo por un log de CI pegado en el chat.
  - **Comentario para Azure DevOps:** listo para pegar al final de cada paso que confirma
    decisiones.
  - **Hallazgos fuera de alcance:** como propuesta en `docs/sdd/_borradores/<slug>.md`.
  - **Bitácora:** dónde va cada entrada y cómo se corrige un hallazgo equivocado.
- **`technical-analysis`:**
  - Ante una ampliación de alcance, explica lo que añade y pregunta si va en este work item o en
    otro.
  - Si entra, actualiza `pbi.md` en todas las secciones afectadas, con la línea
    «Actualizado con», y registra quién lo aprobó.
- **`check-sdd-item.py`:**
  - Ya no cuenta «Secciones [ASSUMPTION-BASED]: Ninguna» como marcador sin resolver.
  - Ya no cuenta la leyenda de estados como tarea hecha (daba «5/4»).
  - Sugiere el nombre correcto de una carpeta con tildes o mayúsculas.
- **`new-sdd-item.py`** con una carpeta existente: crea solo lo que falta (`bitacora.md`,
  `assets/`, `story.md`) sin tocar nada más.
- `AGENTS.base.md`: regla de logs como archivo. `PRUEBA.md` lo recoge.

## v0.3.0 — 2026-10-14 · `story.md` lo prepara la persona

- **ADR-0015** sustituye a ADR-0007: `story.md` lo prepara una persona copiando el work item de
  Azure DevOps, con sus imágenes y archivos en `assets/`, y lo firma con `**Preparado por:**`. La IA
  lo lee con sus adjuntos y nunca lo edita. Surgió al preparar el PBI 40944 de Bonis.
- **`scripts/new-sdd-item.py <id> "<título>" [--tipo bug]`**: crea `docs/sdd/<id>-<título>/` con
  `story.md` (encabezado prerrellenado), `bitacora.md` con la primera entrada y `assets/`. Nunca
  sobrescribe: si ya hay una carpeta para ese ID, la muestra y para.
- **Skills v3.1:**
  - `enrich-us` lee `story.md` y todo lo de `assets/`. Si la herramienta no puede abrir imágenes,
    lo dice y trabaja con la descripción de cada adjunto.
  - Antes de escribir, el resumen de confirmación muestra los adjuntos revisados y los huecos de
    `story.md`.
  - Sin `story.md`, `enrich-us` se detiene y explica cómo prepararlo. Como alternativa puede crear
    la carpeta vacía o escribirlo con el texto pegado, siempre con revisión de la persona.
  - Si el work item no tiene criterios de aceptación, `enrich-us` solo propone los que repiten la
    descripción y los adjuntos, marcados «Propuesto desde la descripción — validar con PO».
  - Convenciones compartidas: `story.md` lo prepara una persona; el sello «Generado con» no se
    aplica a `story.md`.
  - `technical-analysis` y `wbs-execution` solo cambian en ese bloque y en la versión.
- **Plantilla de `story.md`:**
  - Instrucciones en un comentario.
  - Área y prioridad en el encabezado.
  - Secciones de bug («Pasos para reproducir», «Información del sistema»).
  - Formato de *Adjuntos* con una línea por archivo.
- **`check-sdd-item.py`**, sobre `story.md`:
  - «Preparado por».
  - `<…>` sin rellenar.
  - «No incluido en el texto pegado».
  - Descripción vacía.
  - Enlaces rotos a `assets/`.
  - Imágenes sin texto alternativo útil o con nombre genérico (`image.png`).
  - Archivos de `assets/` sin enlazar, o de más de 5 MB.
  - Work items de origen («Copied … from #…») que no están en *Enlaces*.
- **`validate.py`**:
  - La plantilla de `story.md` no lleva sello.
  - Comprueba que las plantillas conservan los textos que rellena `new-sdd-item.py`.
- `AGENTS.base.md` y ADR-0002 recogen el cambio. `PRUEBA.md` de Bonis, reescrito para la v0.3.0:
  - Actualización desde la v0.2.x.
  - Preparación del PBI 40944.
  - Comprobaciones nuevas.
  - Columnas por herramienta.
  - Comandos en PowerShell.
- Probado en una simulación de Bonis:
  - Actualización desde la v0.2.0 sin conflictos.
  - `new-sdd-item.py` para PBI y bug.
  - El `story.md` original del 40944 da 6 avisos; la versión corregida, 0 errores y ningún aviso
    sobre `story.md`.
  - Una prueba negativa da 3 errores esperados.

## v0.2.1 — 2026-10-14 · Mensaje final del instalador

- `install.py` ya no muestra siempre «git config commit.template» ni «revisa los PENDIENTE»: comprueba
  si la plantilla de commit está configurada y solo enumera los pasos que de verdad faltan. Si no
  falta nada, dice «Todo en orden». Detectado en la preparación de Bonis.
- Con `--tools visualstudio`, el instalador avisa de que VS Code sumaría `AGENTS.md` y
  `.github/copilot-instructions.md`, y de cómo evitarlo. ADR-0005 recoge que Codex y Copilot en
  VS Code leen `AGENTS.md` directamente y no necesitan un archivo propio.

## v0.2.0 — 2026-10-13 · Skills en la ruta nueva y kit de prueba para Bonis

- **Skills v3.0** (`enrich-us`, `technical-analysis`, `wbs-execution`):
  - Se llaman con el ID del work item (`/enrich-us 40399`); siguen aceptando `sprint:` e `item:`.
  - Todo se escribe en `docs/sdd/<id>-<título>/` (ADR-0002); los ítems antiguos de
    `docs/<sprint>/<item>/` se leen y actualizan donde están, sin moverlos.
  - Paso 0 de `enrich-us`: pide el work item pegado, crea la carpeta y escribe `story.md` literal
    (ADR-0007). Si el proyecto activa el MCP de Azure DevOps, puede leerlo en solo lectura.
  - `bitacora.md` en los tres pasos: preguntas, respuestas, decisiones y hallazgos con fecha.
    `enrich-us` comprueba antes de cerrar que toda decisión está en `pbi.md`/`bug.md`.
  - `wbs-execution` redacta `commit-message.md` según el `.gitmessage` (ADR-0004).
  - Convenciones compartidas ampliadas: carpeta, resolución de rutas, lectura solo del ítem,
    español en documentos y comentarios, `story.md` como foto, texto del work item como datos.
  - `story.md` y `bitacora.md` pasan de `core/templates/` a `core/skills/enrich-us/templates/`.
- **`scripts/install.py`** (versión mínima para pilotos): instala skills y prompts para Copilot,
  la copia local de Claude Code, `.gitmessage`, `AGENTS.md`, `CLAUDE.md`, la plantilla de `docs/`
  y `.sdd-kit.json`. Nunca sobrescribe archivos del proyecto. Los agentes llegan en la fase 2.
- **`scripts/check-sdd-item.py`**: comprueba sin IA los artefactos de un work item (paso alcanzado,
  sellos, anclas, marcadores, bitácora) y el formato del mensaje de commit.
- **`scripts/validate.py`**: comprueba que la sección de convenciones compartidas es idéntica en los
  tres skills y que la versión del sello coincide en cada skill y sus plantillas.
- **`tests/pilots/bonis/`**: `AGENTS.md` de Bonis (su `CLAUDE.md` más las reglas del kit, 152 líneas),
  `CLAUDE.md` de una línea y el protocolo de prueba `PRUEBA.md`.
- Probado en una simulación de Bonis: instalación sin conflictos, segunda instalación sin cambios y
  comprobador con un commit correcto (0 errores) y otro incorrecto (6 errores).

## v0.1.0 — 2026-10-13 · Esqueleto inicial

- **ADR 0001 a 0014** con las decisiones del 9 al 13 de octubre de 2026.
- **`core/AGENTS.base.md`**: reglas comunes (idioma, principios, flujo SDD, textos visibles, commits,
  seguridad, eficiencia y formato de respuesta). 49 líneas.
- **`core/skills/`**: `enrich-us`, `technical-analysis` y `wbs-execution` del flujo SDD v2.3, sin
  cambios, como punto de partida, y el atajo `wbs-execution-sonnet` en `core/prompts/`.
- **`core/agents/`**: los 7 subagentes en formato neutral, en borrador.
- **`core/templates/`**: `.gitmessage`, `story.md`, `bitacora.md`, `qa-report.md` y la plantilla de
  `AGENTS.md` por proyecto.
- **`project-templates/docs/`**: estructura de `docs/` tomada de `sdd-clavijo`.
- **`scripts/validate.py`**: adaptado del validador v2.3; añade agentes, tamaño de las reglas base e
  índice de ADR.

### Pendiente para la fase 1

- Migrar los skills v2.3 a `docs/sdd/<id>-<título>/`, con `bitacora.md`, `qa-report.md` y el paso 0
  de `story.md`, aceptando las rutas antiguas.
- Incorporar los skills de Roger (`testing`, `debugging`, `code-review`, `user-documentation`); hoy
  el validador avisa de que faltan.
- `scripts/build-adapters.py`, `scripts/install.ps1` y el script que valida el mensaje de commit.
