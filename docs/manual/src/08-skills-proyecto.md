# Skills de proyecto

:::lead
Dos skills trabajan sobre el repositorio entero, no sobre un work item. `project-context` se ejecuta
una vez tras instalar el kit (y cuando cambia el stack): escribe lo que todas las demás skills dan
por cierto. `document-project` documenta todo el proyecto existente, por bloques, cuando el equipo
decide hacerlo.
:::

## project-context · el contexto del proyecto

:::card
<dl class="kv">
<dt>Paso</dt><dd>0 · una vez por repositorio, y al cambiar el stack</dd>
<dt>Quién</dt><dd>Tech lead (o un dev que conozca el proyecto)</dd>
<dt>Comando</dt><dd><code>/project-context</code> · <code>/project-context fresh</code> · <code>/project-context check</code></dd>
<dt>Lee</dt><dd>Todo el repositorio (con <code>inventory.py</code> y <code>code-explorer</code>), README, <code>CLAUDE.md</code>, <code>docs/</code> existentes</dd>
<dt>Ejecuta</dt><dd>Build, todas las pruebas, lint y type check (verifica los comandos y registra la línea base)</dd>
<dt>Escribe</dt><dd><em>Project context</em> de <code>AGENTS.md</code>, los seis <code>docs/*.md</code>, proyecto de pruebas, pruebas de arquitectura, <code>sdd-guardrails.json</code></dd>
<dt>Subagentes</dt><dd><code>code-explorer</code>, <code>backend-dev</code>, <code>doc-writer</code></dd>
<dt>Modelo</dt><dd>Opus (fijado en Claude Code)</dd>
</dl>
:::

### Por qué importa tanto

Las demás skills **confían ciegamente** en *Project context*: si un comando está mal escrito aquí, se
repite mal en cada work item. Por eso todo lo que escribe sale de un archivo, de un comando que ha
ejecutado o de una respuesta tuya, y lo que no pudo verificar queda marcado `[REQUIRES-VALIDATION]`.

### Modos

| Modo | Cuándo | Qué hace |
| --- | --- | --- |
| *new* (sin argumento, sin contexto previo) | Primera vez | Todo el proceso |
| *update* (sin argumento, con contexto) | El stack o los comandos cambiaron | Todo el proceso y te presenta una lista de cambios (añadir, corregir, mover a `docs/`, quitar), cada uno con su fuente. Nunca quita texto escrito por una persona sin aprobación |
| `fresh` | Quieres rehacerlo sin dejarte llevar por el actual | Ignora el contexto actual y compara al final |
| `check` | `check_project.py` da avisos o errores | Pasada corta: convierte cada aviso en una fila con su resolución, sin inventario ni build |

### Qué hace, paso a paso

1. **Precondiciones:** no en `dev`/`main` (crea `chore/sdd-project-context`), kit instalado. Dice el
   modo y cuánto puede tardar.
2. **Inventario determinista** con `inventory.py`: proyectos, lockfiles, archivos de traducción,
   pipeline, endpoints, proyecto de pruebas, configuración de IA existente. Marca lo que necesita
   una decisión (dos lockfiles, traducciones generadas, sin proyecto de pruebas…).
3. **Exploración** en paralelo con `code-explorer`, una pregunta por área: arquitectura,
   autorización y errores, datos, frontend, traducciones, pruebas y ejecución local. Lee además lo
   que las personas ya escribieron (README, `CLAUDE.md`, `docs/`). Si contradice al código, gana el
   código y la contradicción se pregunta.
4. **Ejecuta todo** (te pide confirmación: tarda minutos): restore y build, toda la suite de
   backend, lint, pruebas y build de frontend, type check. Registra si funciona, cuánto tarda y su
   **línea base** (avisos, pruebas que ya fallan). Nunca arregla lo que ya fallaba.
5. **Infraestructura de pruebas:** sin proyecto de pruebas de backend, lo crea (xUnit v3 y Moq,
   misma versión de .NET, en la solución, con una prueba que ejercita código real). Copia la
   plantilla de **pruebas de arquitectura** y deja que `backend-dev` la complete; lo que ya
   incumple una regla va a su lista de excepciones con el motivo.
6. **Preguntas en un bloque**, solo lo que el repositorio no responde: qué es el producto y quién
   lo usa, quién despliega, convenciones que no están en el código, conflictos encontrados, qué
   hacer con la configuración de IA existente.
7. **Borrador para aprobar:** *Project context* (encabezados fijos, unas 120 líneas, el archivo
   entero por debajo de 185), los seis `docs/`, la integración con el sitio de documentación
   (DocFX), los cambios a la configuración de IA anterior y `sdd-guardrails.json`. Puedes aprobarlo
   por partes.
8. **Escribe:** la sesión escribe `AGENTS.md` (debajo del bloque del kit); `doc-writer`, `docs/`.
9. **Verifica:** `check_project.py` con 0 errores, y lee los diffs.

### Los encabezados fijos de Project context

| Encabezado | Contenido |
| --- | --- |
| *What this is* | El producto y quién lo usa, en un párrafo |
| *Commands* | Build, pruebas, lint, tipos, servidor de desarrollo, con versiones de herramientas y su línea base |
| *Local run* | Qué hace falta para arrancar en local: servicios, usuario y roles locales, modo de build |
| *Architecture* | Capas y dirección de dependencias, dónde se registra la DI, flujo de una petición |
| *Authorization and errors* | Esquema de autenticación, roles, tenants, manejo global de excepciones |
| *Data* | DbContext, configuración de entidades, migraciones, transacciones, otros almacenes |
| *Tests* | Convenciones, fixtures, base de datos en pruebas, pruebas de frontend, pruebas de arquitectura |
| *Internationalization* | Archivos, idiomas, convención de claves, si se generan, cómo se añade una clave |
| *Protected paths* | Rutas que la IA nunca edita (librerías compartidas, código generado, submódulos) |
| *Branches, CI and commits* | Ramas, pipeline, formato de commit |
| *Documentation* | Dónde está la documentación y el sitio (DocFX) |

### Ejemplo de cierre

:::out
## 🧭 Contexto del proyecto — mi-proyecto
Modo: new · AGENTS.md: 178 líneas · docs/: creados architecture, backend, database, api-reference, frontend, reglas-negocio
Verificado: build OK (1 min 40 s, 15 avisos) · pruebas 298 OK, 2 fallaban antes · lint 0 errores · tipos 3 errores previos
Proyecto de pruebas: creado MiProyecto.Tests (4 pruebas) · CI: dotnet test añadido (aprobado)
Decisiones: yarn.lock es el válido; i18n/*.json se editan a mano; CLAUDE.md → @AGENTS.md
Pendiente: [REQUIRES-VALIDATION] usuario local de pruebas · _borradores/pruebas-frontend.md
Siguiente: /document-project (documentación completa) o el primer work item con /enrich-us
git add AGENTS.md CLAUDE.md docs/ MiProyecto.Tests/ MiProyecto.sln sdd-guardrails.json azure-pipelines.yml
:::

### El modo check

:::ask
/project-context check
:::

Ejecuta `check_project.py` y te propone una tabla, por ejemplo:

| Aviso | Resolución | Quién |
| --- | --- | --- |
| Sección por encima de su presupuesto | Mover el detalle (nunca una regla) a `docs/` con enlace | La sesión |
| Sección vacía o encabezado que falta | Rellenarla con una búsqueda dirigida | La sesión |
| `[REQUIRES-VALIDATION]` | Decir qué falta y cómo verificarlo (un comando, una pantalla, una persona); al resolverlo, cambiar el marcador por el hecho | La sesión o una persona |
| Fuentes cambiadas después de la fecha del contexto | Releer solo esas fuentes y proponer el cambio | La sesión, con aprobación |
| `sdd-guardrails.json` sin rutas protegidas · sin pruebas de arquitectura | Proponer la configuración y las pruebas | La sesión, con aprobación |
| Sin proyecto de pruebas · `CLAUDE.md` con contenido propio | El modo completo | `/project-context` |

## document-project · documentar todo el proyecto

:::card
<dl class="kv">
<dt>Cuándo</dt><dd>Una vez, después de <code>project-context</code>, en proyectos con código sin documentar</dd>
<dt>Quién</dt><dd>Tech lead o un dev; un bloque por sesión</dd>
<dt>Comando</dt><dd><code>/document-project</code> · <code>plan</code> · <code>status</code> · <code>block:B-NN</code> · <code>area:A-NN</code></dd>
<dt>Lee</dt><dd>El código del área, el historial git, ADR, <code>docs/</code>, <code>_borradores/</code></dd>
<dt>Escribe</dt><dd>Comentarios de documentación, resúmenes de clases de prueba, <code>docs/</code>, <code>docs/sdd/_documentacion/</code></dd>
<dt>Subagentes</dt><dd><code>doc-writer</code>, <code>code-explorer</code></dd>
<dt>Scripts</dt><dd><code>doc_coverage.py</code>, <code>comment_only.py</code>, <code>check_project.py</code></dd>
</dl>
:::

### Para qué sirve

Es `document-code` aplicado al código que ningún work item tocó: comentarios `///`/TSDoc en todo el
código público, un resumen en cada clase de pruebas y `docs/` completos (cada endpoint, entidad y
pantalla; solo reglas de negocio confirmadas). Como el proyecto es grande, trabaja **por áreas
agrupadas en bloques: un bloque por sesión, un commit y un PR por bloque**, con un plan reanudable.

### Modos

| Forma | Qué hace |
| --- | --- |
| `/document-project` | Sin `plan.md`: crea el plan. Con plan: documenta el siguiente bloque no `Hecha` |
| `/document-project plan` | Rehace el plan: añade áreas nuevas, mantiene las `Hecha` |
| `/document-project block:B-03` | Documenta ese bloque |
| `/document-project area:A-12` | Documenta solo esa área |
| `/document-project status` | Solo informa: cobertura frente a la línea base, bloques hechos y pendientes, áreas en `Revisar`, hallazgos abiertos y archivos cambiados después de documentarse. No escribe; funciona en cualquier rama |

### El plan

1. **El script propone** áreas, partes y bloques (`doc_coverage.py --areas`): un área por
   controller con los servicios y tipos que solo él usa; controllers base, servicios compartidos y
   carpetas restantes como áreas transversales; frontend por carpeta de funcionalidad; pruebas con
   el área de la clase que prueban. Áreas de más de 15 archivos o 60 símbolos sin documentar se
   dividen, sin separar nunca una entidad de su configuración EF, una interfaz de su clase ni las
   partes de una clase parcial. Orden: transversal de backend por dependencia → controllers con
   más cambios recientes → frontend. Bloques de como máximo 5 áreas y 40 archivos del mismo grupo.
2. **Línea base** de avisos: build `--no-incremental` y `doc_coverage.py --warnings` guardan los
   avisos por código y archivo en `docs/sdd/_documentacion/avisos.md` (los `NU19xx` de NuGet,
   aparte). Si el proyecto suprime CS1591, se mide con un build aparte (`-p:NoWarn=`) y el comando
   queda escrito para medir siempre igual.
3. **La sesión corrige solo lo que el script no puede saber** (un archivo en el área equivocada,
   pruebas sin área, código generado que se coló), cada cambio con su motivo.
4. **Pregunta** por el work item del esfuerzo (recomendado: un PBI «Documentación inicial del
   proyecto», para usar `Ref: #<id>` en los commits).
5. **Te enseña el resumen y espera tu aprobación.** Todas las cifras salen del script o de un
   comando, nunca de una estimación.
6. Escribe `plan.md` y lo comprueba con `doc_coverage.py --check-plan`: 0 errores (cada archivo a
   documentar en exactamente un área).

### Un bloque

1. **Hechos por área:** símbolos sin comentario (`doc_coverage.py --files`) y una pregunta a
   `code-explorer` por área (comentarios que contradicen el código, endpoints con rutas, roles y
   códigos de estado, entidades, pantallas). El *porqué* solo de fuentes escritas: historial git
   con `#<id>`, ADR, comentarios existentes. Sin fuente, no hay comentario de porqué.
2. **Hallazgos** (código que parece incorrecto, código muerto, duplicado, documentación que
   contradice el código) a *Hallazgos* de `plan.md`; si merecen un work item, también a
   `_borradores/`. Un hallazgo conocido se cita, no se repite, y su código se deja como está.
   **Nunca se arregla código aquí.**
3. **Confirmación**, copia de seguridad con `comment_only.py save` y delegación en `doc-writer`
   (un paquete por área o cada 10–15 archivos; máximo 2 en paralelo). Lo que el paquete no da y el
   código no muestra se documenta **«desde el código»**: lo que hace, nunca la intención.
4. **Verificación:** `comment_only.py check` (solo comentarios), build igual que la línea base y
   `--warnings --compare avisos.md` con **0 avisos nuevos**, lectura de las afirmaciones del diff
   (autorización, errores, efectos, significado de negocio) contra el código, `check_project.py`.
   La sesión **nunca parchea un comentario**, ni una línea `//`: lo devuelve a `doc-writer`.
5. **Cierre:** `B-NN.md` con resultado, validación, lo que quedó sin documentar y el mensaje de
   commit (`docs(<ámbito>): documentar <áreas>`); `plan.md` con cada área `Hecha (<fecha>)`;
   `avisos.md` actualizado.

:::out Cierre de un bloque
## 📝 Documentación — B-01 · Base, autorización y errores
Cambios: 64 comentarios (58 nuevos, 6 corregidos) · pruebas: 9 resúmenes · docs/: architecture.md, backend.md
Cobertura del bloque: 12 % → 97 % · proyecto: 18 % → 26 %
Validación: comment_only → solo comentarios · build → 0 avisos nuevos (226 = línea base) · lint/tipos → OK
Sin documentar: 2, ver B-01.md · Hallazgos: 3
Siguiente: commit y PR de este bloque · después /document-project en una sesión nueva (B-02: Datos)
git add <cada archivo cambiado, de git status> docs/sdd/_documentacion/
:::

:::warn Un bloque, un commit
Nunca empieces un bloque sobre otro sin commit: la skill se para si el árbol no está limpio (salvo
el `plan.md` todavía sin commit, que entra con el primer bloque). La rama sugerida es
`docs/document-project-b01`.
:::

:::note Cuándo no hace falta
En un proyecto nuevo, o si el equipo prefiere documentar sobre la marcha, `document-code` mantiene
la documentación al día work item a work item. `document-project` es para la deuda de
documentación acumulada.
:::
