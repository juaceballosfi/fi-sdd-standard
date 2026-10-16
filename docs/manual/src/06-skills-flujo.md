# Skills del flujo principal

:::lead
Una skill es un paso del flujo empaquetado: instrucciones, plantillas y scripts que la IA sigue al
pie de la letra. Este capítulo explica cómo es una skill por dentro y detalla las cinco del flujo
principal: `enrich-us`, `technical-analysis`, `wbs-execution`, `qa-review` y `document-code`.
:::

## Cómo es una skill

Cada skill es una carpeta con un `SKILL.md` y, si los necesita, `templates/` y `scripts/`:

```text
.agents/skills/enrich-us/
├── SKILL.md               ← instrucciones (en inglés): pasos, confirmaciones, límites
└── templates/
    ├── story.md           ← plantilla de lo que prepara la persona
    ├── bitacora.md
    ├── pbi.md
    └── bug.md
```

El `SKILL.md` empieza con una cabecera que la herramienta lee para listar la skill y decidir
cuándo usarla:

```yaml
---
name: enrich-us
description: Step 1 of the SDD flow ... Use when the user asks to run enrich-us or to enrich/refine
  a work item, PBI, bug or user story.
argument-hint: "<work-item-id> [qa]   e.g. 40399 · 40399 qa"
---
```

Y sigue siempre el mismo esquema:

| Sección | Qué contiene |
| --- | --- |
| *Inputs* | Los argumentos que acepta y cómo resolver la carpeta del work item |
| *Shared SDD conventions* | Un bloque **idéntico en las 9 skills**: carpeta, bitácora, marcadores, sello, idioma, exploración con `code-explorer`, entradas grandes, i18n, git. Ver capítulo 13 |
| *Step 0 … Step N* | Los pasos, con los bloques de confirmación exactos que te mostrará |
| *Constraints* | Lo que la skill nunca hace |

### Invocar una skill

Escribe `/` y el nombre en el chat, seguido de los argumentos:

```text
/enrich-us 40399
/wbs-execution 40399 from:T-03
/qa-review 40933 base:9e07c66d head:99e5da20
```

También puedes pedirlo con palabras («ejecuta enrich-us para el 40399»): la descripción de la
skill hace que la herramienta la elija. El comando con `/` es más fiable.

:::note Copilot y $ARGUMENTS
Claude Code sustituye `$ARGUMENTS` en el `SKILL.md` por lo que escribes tras el nombre. Copilot no
lo hace: cada skill lo detecta («*if the Arguments line still shows a placeholder…*») y toma el ID
de tu mensaje. Por eso en Copilot conviene escribir el ID en la misma línea: `/enrich-us 40399`.
:::

### Lo que todas las skills tienen en común

- **Confirman antes de escribir.** Te muestran un bloque de resumen y esperan un «sí» o tus
  correcciones. Sin respuesta, no escriben nada.
- **Se paran con ⛔** cuando falta algo imprescindible (la carpeta, el documento del paso anterior,
  la rama) y te dicen qué ejecutar.
- **Registran en `bitacora.md`** una línea por pregunta, respuesta, decisión o hallazgo.
- **Terminan con un informe** fijo, el siguiente paso y, si cambió algo del work item, un bloque
  *Comentario para Azure DevOps* listo para pegar.
- **Nunca hacen commit**: te dan el `git add` con rutas exactas.

## enrich-us · del work item al requisito técnico

:::card
<dl class="kv">
<dt>Paso</dt><dd>1 · compuerta G1</dd>
<dt>Quién</dt><dd>Dev que toma el work item; QA con el modo <code>qa</code></dd>
<dt>Comando</dt><dd><code>/enrich-us &lt;id&gt;</code> · <code>/enrich-us &lt;id&gt; qa</code> · legado: <code>sprint:&lt;s&gt; item:&lt;i&gt;</code></dd>
<dt>Lee</dt><dd><code>story.md</code>, todo <code>assets/</code>, el código (con <code>code-explorer</code>), <code>AGENTS.md</code></dd>
<dt>Escribe</dt><dd><code>pbi.md</code> o <code>bug.md</code>, <code>bitacora.md</code></dd>
<dt>Modelo</dt><dd>Uno de razonamiento (Opus)</dd>
<dt>Rol de la IA</dt><dd><em>Technical Product Owner</em> y arquitecto</dd>
</dl>
:::

### Para qué sirve

Convierte el work item que copiaste de Azure DevOps en un documento técnico completo
(`pbi.md` o `bug.md`) con el que un desarrollador puede implementar **sin volver al work item**:
criterios de aceptación, campos y entidades afectados, endpoints, archivos a modificar, reglas de
negocio, textos e idiomas, pruebas necesarias y Definición de Hecho. Cada dato dice de dónde sale
(columna *Origen*): `story.md`, `Inferido del código`, `Confirmado por <persona> (<fecha>)` o
`[PENDING-BUSINESS]`.

### Antes de lanzarla

Prepara la carpeta y copia el work item:

```powershell
python <kit>\scripts\new-sdd-item.py 40399 "Sección de ofertas en el menú lateral"   # --tipo bug para un bug
```

Rellena `story.md` siguiendo el comentario que trae: **texto literal** (sin resumir ni traducir),
todos los `<…>` de la cabecera, imágenes en `assets/` con nombre descriptivo y una línea en
*Adjuntos* que diga qué muestra cada una. Comprueba con:

```powershell
python .agents\scripts\check-sdd-item.py docs\sdd\40399-seccion-de-ofertas-en-el-menu-lateral
```

### Qué hace, paso a paso

1. **Contexto:** raíz del repositorio y rama; lee de `AGENTS.md` solo lo que necesita.
2. **Lee `story.md` y todos los adjuntos.** Mira las imágenes si la herramienta puede; si no,
   trabaja con su descripción. Anota los huecos: `<…>` sin rellenar, secciones «No incluido en el
   texto pegado», work items relacionados que habría que copiar. Si no hay `story.md`, se para y
   te explica cómo prepararlo (u ofrece crear la carpeta o escribir `story.md` con el texto que le
   pegues, **literal**).
3. **Clasifica** PBI o bug (por la línea *Fuente* de `story.md`).
4. **Analiza el código** con `code-explorer`: stack, módulos, entidades, DTO, endpoints, pruebas,
   convenciones, work items anteriores del mismo área y el **sistema de traducciones** (archivos,
   idiomas con entradas reales, convención de claves, qué pasa si falta una clave).
5. **Evalúa si hay información suficiente.** Infiere del código lo estructural (forma de un
   endpoint, archivos a tocar, convenciones de prueba). **Nunca** inventa reglas, valores,
   criterios ni casos límite: los pregunta. Con 3 o más campos críticos pendientes se para con
   *⚠️ Not enough information* y una pregunta por campo.
6. **Modo `qa`:** clasifica cada criterio como *Definido*, *Deducción directa* o *A confirmar*
   (capítulo 7).
7. **Confirmación (G1).** Te muestra el resumen y espera.
8. **Escribe** `pbi.md`/`bug.md` desde la plantilla. Si ya existe, pregunta si sobrescribe.
9. **Cierra la bitácora:** toda decisión de la tabla *Decisiones* debe estar en `pbi.md` y marcada
   «Sí»; lo que siga abierto pasa a *Campos pendientes de aclaración* como `[PENDING-BUSINESS]`.

### Ejemplo

:::ask
/enrich-us 40399
:::

:::out Confirmación que te muestra (G1)
## Confirmación del análisis — 40399 Sección de ofertas en el menú lateral

Tipo detectado: PBI
Carpeta: docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
Fuente: story.md (work item #40399, revisión 7, preparado por Ana Pérez)
Adjuntos revisados: assets/40399-menu-lateral.png (mockup del menú con «Ofertas» bajo «Clientes»)
Huecos en story.md: ninguno
Salida propuesta: pbi.md
Stack detectado: Backend: .NET 8 · Frontend: React 18 + TypeScript · BD: SQL Server
Traducciones: ClientApp/src/i18n/*.json · es, en, fr · la clave es el texto en inglés — 2 textos nuevos

Resumen: los comerciales necesitan un acceso directo a sus ofertas desde el menú lateral…

Módulos implicados:
- ClientApp/src/layout/SideMenu.tsx — menú lateral — Inferido del código
- Api/Controllers/OffersController.cs — listado de ofertas — Inferido del código

Campos pendientes:
- [PENDING-BUSINESS: ¿qué roles ven la sección? story.md solo menciona «comerciales»]

¿Es correcto el análisis? Responde «sí» o dime qué corregir.
:::

:::ask Tu respuesta
La ven Comercial y Jefe de ventas; lo confirmó Laura (PO) hoy. El resto, correcto.
:::

:::out Informe final
## ✅ Enriquecimiento completo — 40399 Sección de ofertas en el menú lateral

Tipo: PBI · Carpeta: docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
Archivos: bitacora.md · pbi.md (story.md leído, sin modificar)
- Criterios de aceptación: 4 (3 de story.md, 1 propuesto desde la descripción, a validar)
- Endpoints: 0 · Archivos a modificar: 3 · Pruebas requeridas: 3
- Textos visibles: 2 (2 propuestos, a validar con el PO) · idiomas: es, en, fr
- Campos pendientes de aclaración: 0

Comentario para Azure DevOps:
2026-10-15 · Ven la sección los roles Comercial y Jefe de ventas (confirmado por Laura Gómez).

⏭️ Siguiente paso: /technical-analysis 40399
:::

### Qué deja

`pbi.md` (secciones: descripción funcional, criterios `CA-XX`, campos y entidades, endpoints,
archivos, reglas `BR-XX`, clasificación de QA, textos e idiomas, requisitos no funcionales, pruebas,
Definición de Hecho, notas, campos pendientes) o `bug.md` (descripción, pasos de reproducción,
esperado frente a actual, causa raíz inferida, archivos, criterios de corrección, clasificación de
QA, textos, pruebas, impacto, DoD, notas, pendientes).

### Paradas y cómo resolverlas

| Mensaje | Causa | Qué haces |
| --- | --- | --- |
| *No hay story.md para el work item…* | No existe la carpeta o `story.md` | `new-sdd-item.py` y copia el work item; o deja que la IA cree la carpeta |
| Un adjunto enlazado no existe | Falta el archivo en `assets/` | Guárdalo con el nombre del enlace y vuelve a lanzar |
| *⚠️ Not enough information…* | 3 o más campos críticos sin definir | Pide las respuestas al PO o corrige el work item y vuelve a copiarlo |
| *pbi.md already exists* | Ya se ejecutó antes | A) sobrescribir (git guarda la versión anterior) o B) cancelar |

:::tip Consejos
- Si el PO responde fuera del chat, pega la respuesta y di quién la dio: la IA la registra con su
  nombre y fecha.
- Los textos visibles sin redacción en `story.md` salen como `Propuesto — validar con PO`: no
  bloquean, pero el PO debe verlos.
- Un criterio que no está en el work item pero se deduce de un mockup sale como `Propuesto desde la
  descripción — validar con PO`.
:::

## technical-analysis · el diseño

:::card
<dl class="kv">
<dt>Paso</dt><dd>2 · compuerta G2 (aprobar 03 y 04)</dd>
<dt>Quién</dt><dd>Dev</dd>
<dt>Comando</dt><dd><code>/technical-analysis &lt;id&gt;</code></dd>
<dt>Lee</dt><dd><code>pbi.md</code>/<code>bug.md</code>, el código (con <code>code-explorer</code>)</dd>
<dt>Escribe</dt><dd><code>00</code>–<code>06</code>, <code>bitacora.md</code></dd>
<dt>Modelo</dt><dd>Uno de razonamiento (Opus)</dd>
<dt>Rol de la IA</dt><dd>Arquitecto y <em>tech lead</em></dd>
</dl>
:::

### Para qué sirve

Produce los siete documentos de diseño que `wbs-execution` implementará tarea por tarea. Separa con
cuidado lo que **afirma del código** (estado actual, deuda, patrones, cobertura), lo que **propone
con justificación** (puntos de historia, patrones, alternativas) y lo que **no puede afirmar** sin
evidencia (reglas de negocio, sistemas externos, impacto en usuarios), que marca
`[REQUIRES-VALIDATION]`.

### Los siete archivos

| # | Archivo | Contenido | Regla |
| --- | --- | --- | --- |
| 01 | `01-current-state-report.md` | Módulos, flujo actual, diagrama, dependencias, deuda, cobertura de pruebas, comportamiento del bug, textos e idiomas (§1.8) | **Solo desde el código** |
| 02 | `02-analysis-diagnosis.md` | Criterios, brecha técnica, cuellos de botella, deuda a abordar, causa raíz (bug), supuestos | La brecha entre 01 y los criterios |
| 03 | `03-solution-proposal.md` | Enfoque, diagrama, SOLID, capas, patrones, alternativas descartadas, impacto en contratos | **Contrato** tras G2 |
| 04 | `04-implementation-plan.md` | Estrategia, orden, **SPECs** *Dado/Cuando/Entonces*, contratos e interfaces, migración, *feature flag* y *rollback*, DoD | **Contrato** tras G2. Cada criterio, al menos una SPEC |
| 05 | `05-wbs-estimation.md` | Tareas `T-XX` con capa, dependencias, SP, **Rol**, **i18n**, origen y estado | Cada tarea incluye sus pruebas y sus traducciones |
| 06 | `06-risks-mitigations.md` | Matriz de riesgos `R-XX` ligados a módulos o tareas, contingencia | — |
| 00 | `00-executive-summary.md` | Objetivo, impacto, esfuerzo, riesgos y decisiones clave, **marcadores** | Se escribe el último |

Reglas de la WBS que conviene conocer porque determinan cómo se implementa:

- **Pruebas dentro de cada tarea**, nunca una tarea «escribir pruebas» al final: así
  `wbs-execution` puede escribirlas primero.
- **Traducciones dentro de la tarea** que añade el texto (`i18n = Sí`), nunca una tarea «traducir».
- **Rol** `Backend`, `Frontend` o `Transversal`: decide qué subagente implementa. Una tarea con dos
  capas se divide en dos.
- **Tareas grandes divididas:** más de 2 SP que reestructuran y cambian comportamiento → (a)
  pruebas de caracterización + reestructuración sin cambio, (b) el cambio. Igual si edita zonas
  lejanas de un archivo de más de unas 1500 líneas.

### Ejemplo

:::ask
/technical-analysis 40399
:::

:::out Confirmación
## Confirmación del análisis — 40399 Sección de ofertas en el menú lateral

Tipo: PBI · Entrada: docs/sdd/40399-…/pbi.md
Campos pendientes heredados: ninguno
Stack: Backend: .NET 8 · Frontend: React 18 + TS · BD: SQL Server

Módulos implicados:
- ClientApp/src/layout/SideMenu.tsx — menú lateral — Frontend
- ClientApp/src/core/permissions.ts — visibilidad por rol — Frontend

Deuda técnica detectada: el menú tiene 2 textos fijos fuera de i18n (baja)
Traducciones: ClientApp/src/i18n/*.json · es, en, fr — 2 textos nuevos
Complejidad: baja · Rango estimado: 3–5 SP

Archivos que se generarán en la carpeta: 00 … 06
¿Es correcto el análisis? Responde «sí» o dime qué corregir.
:::

Tras tu «sí» genera los archivos en orden, con una línea de progreso por archivo
(`✓ 01-current-state-report.md`…), y termina con la tabla de estado, los marcadores abiertos y el
total de SP y tareas.

### Tu compuerta G2

Lee **`03` y `04` enteros** antes de aprobar. Son contrato: una vez aprobados, solo cambian con tu
aprobación explícita, una nueva versión y quién la aprobó. Comprueba sobre todo:

- que cada criterio `CA-XX` tiene su `SPEC-XX` y que las SPECs son verificables;
- que los contratos (firmas, DTO, rutas) son los que quieres;
- que la WBS no tiene tareas mezcladas de capas ni una tarea de pruebas al final;
- los `[REQUIRES-VALIDATION]` y `[ASSUMPTION-BASED]` del resumen ejecutivo.

Para aprobar, pide que actualice la línea *Estado* de 03 y 04: «Aprueba 03 y 04, aprobado por Ana
Pérez hoy».

### Paradas frecuentes

| Mensaje | Causa | Qué haces |
| --- | --- | --- |
| *⛔ pbi.md or bug.md not found* | No se hizo el paso 1 | `/enrich-us <id>` |
| *⚠️ The input document has unresolved fields* | `pbi.md` tiene `[PENDING-BUSINESS]` | A) resolverlos antes (recomendado) o B) seguir: las secciones afectadas salen `[ASSUMPTION-BASED]` |
| *⚠️ Analysis files already exist* | Ya se generó | A) sobrescribir o B) cancelar |
| Pides añadir trabajo fuera del work item | Deuda, otro bug, un refactor | Te dice lo que añade y pregunta: ¿entra aquí (con aprobación del PO) o va a `_borradores/`? |

## wbs-execution · implementar

:::card
<dl class="kv">
<dt>Paso</dt><dd>3</dd>
<dt>Quién</dt><dd>Dev</dd>
<dt>Comando</dt><dd><code>/wbs-execution &lt;id&gt;</code> · <code>from:T-03</code> · <code>qa</code> · en Copilot: <code>/wbs-execution-sonnet</code></dd>
<dt>Lee</dt><dd><code>00</code>–<code>06</code>, la configuración del proyecto (comandos)</dd>
<dt>Escribe</dt><dd>Código y pruebas (por medio de los subagentes), <code>05</code> (estado), <code>CHANGELOG.md</code>, <code>bitacora.md</code>, <code>commit-message.md</code></dd>
<dt>Subagentes</dt><dd><code>backend-dev</code>, <code>frontend-dev</code>, <code>migration-reviewer</code>, <code>code-explorer</code></dd>
<dt>Modelo</dt><dd>Sonnet (fijado en Claude Code)</dd>
</dl>
:::

### Para qué sirve

Ejecuta la WBS aprobada **tarea por tarea**, con pruebas primero y verificación real después de
cada tarea. No rediseña: si el diseño no se puede implementar tal cual, se para y te propone el
ajuste mínimo.

### Qué hace, paso a paso

1. **Comprueba** la rama y los cambios sin commit ajenos al work item (te avisa antes de tocar
   nada).
2. **Lee los siete documentos** y los marcadores del resumen ejecutivo. Con `[ASSUMPTION-BASED]` o
   `[REQUIRES-VALIDATION]` abiertos, te pregunta si vuelves a `technical-analysis` o sigues
   asumiendo el riesgo.
3. **Detecta los comandos** reales de build, test y lint (`package.json`, `*.sln`, `pom.xml`…) y
   los archivos de traducción.
4. **Confirmación de inicio:** comandos, puntos clave del diseño, tabla de tareas, quién implementa
   cada una (`backend-dev`, `frontend-dev` o la sesión) y si hay tareas paralelizables.
5. **Ciclo por tarea:**
   - anuncia la tarea (archivos, SPECs, textos, riesgos). Pide confirmación extra si toca un
     contrato público, una migración, borra archivos o cambia infraestructura;
   - **delega** en el subagente de la capa con un *paquete cerrado*: la tarea, sus SPECs
     literales, contratos, archivos con rangos de líneas, comandos exactos, convenciones de
     `AGENTS.md`, archivos de traducción y riesgos;
   - el subagente **escribe primero la prueba y la ve fallar** (línea *Rojo*), implementa y la ve
     pasar;
   - **la sesión verifica por su cuenta**: build, pruebas, lint y tipos, `git status` y
     `git diff --stat` (solo los archivos esperados, nada en rutas protegidas ni en `docs/sdd/`);
     las migraciones pasan por `migration-reviewer`; las traducciones, en todos los idiomas;
   - marca la tarea `✅ Hecha` en `05`, añade una entrada a `CHANGELOG.md` e informa del progreso.
6. **Cierre:** comprobación de traducciones del work item, DoD final, barrido de marcadores,
   `commit-message.md` completo desde el CHANGELOG y los comandos de `git add` y `pr-check.py`.

:::warn El informe del subagente no es evidencia
La sesión vuelve a ejecutar build y pruebas aunque el subagente diga que están en verde. Si una
tarea con pruebas nuevas no trae línea *Rojo*, lo registra como desviación y comprueba que las
pruebas de caracterización afirman el comportamiento que ya existía en `HEAD`.
:::

### Bucles y sus límites

| Bucle | Límite | Después |
| --- | --- | --- |
| El subagente corrige su propia comprobación que falla | 3 intentos | Devuelve un bloqueo |
| La verificación de la sesión falla → vuelve al subagente | 2 rondas | Bloqueo para ti |
| El subagente se para sin informe | 1 reanudación | Decides: la sesión termina la tarea o se divide |
| Hallazgos de QA devueltos a implementación (`qa`) | 2 rondas de QA | Decides cada hallazgo abierto |
| Hace falta cambiar el diseño ya empezado | — | Primero se actualizan 03/04 con tu aprobación |

Pasado un límite, **decides tú**; la IA nunca sigue reintentando por su cuenta.

### Ejemplo

:::ask
/wbs-execution 40399
:::

:::out Confirmación de inicio
## Confirmación de inicio — 40399 Sección de ofertas en el menú lateral

Tipo: PBI · Rama: feature/40399-seccion-ofertas · Stack: .NET 8 + React 18
Comandos:
  - Build: dotnet build MiProyecto.sln            [MiProyecto.sln]
  - Test:  dotnet test MiProyecto.Tests            [MiProyecto.Tests.csproj]
  - Lint:  cd ClientApp; yarn lint                 [package.json]
Traducciones: ClientApp/src/i18n/*.json · es, en, fr · clave = texto en inglés
Marcadores heredados: ninguno

| ID   | Tarea                                  | SP | Deps | i18n | Estado       |
| T-01 | Permiso «ver ofertas» por rol          | 2  | —    | No   | ⬜ Pendiente |
| T-02 | Entrada «Ofertas» en el menú lateral   | 2  | T-01 | Sí   | ⬜ Pendiente |

Total: 2 tareas · 4 SP · Camino crítico: T-01 → T-02
Implementa: T-01 → backend-dev · T-02 → frontend-dev
Paralelo: ninguno
¿Empiezo con T-01?
:::

:::out Progreso tras cada tarea
✅ T-01 hecha: Permiso «ver ofertas» por rol — 40399
📋 Progreso: 1/2 tareas · 2/4 SP
🌐 Traducciones: N/A · pendientes: ninguna
⏭️ Siguiente: T-02 — Entrada «Ofertas» en el menú lateral. ¿Continúo?
:::

:::out Cierre
## 🏁 WBS completa — 40399 Sección de ofertas en el menú lateral
Tareas: 2/2 · 4 SP · Con avisos: ninguna

Rama: feature/40399-seccion-ofertas — esperada: feature/<ID>-<slug> desde dev [OK]
git add Api/Authorization/Permissions.cs MiProyecto.Tests/Authorization/PermissionsTests.cs `
        ClientApp/src/layout/SideMenu.tsx ClientApp/src/layout/SideMenu.test.tsx `
        ClientApp/src/i18n/es.json ClientApp/src/i18n/fr.json `
        docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
git commit -F docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/commit-message.md
python .agents/scripts/pr-check.py

Siguiente: /qa-review 40399 en una sesión nueva, después /document-code 40399.
:::

### Modos y argumentos

| Forma | Qué hace |
| --- | --- |
| `/wbs-execution <id>` | Empieza o **reanuda**: lee la columna Estado de `05`, ejecuta build y pruebas antes de seguir y continúa por la primera tarea pendiente |
| `/wbs-execution <id> from:T-03` | Empieza en `T-03`, solo si sus dependencias están hechas |
| `/wbs-execution <id> qa` | Corrige los hallazgos de `qa-report.md` marcados `A corregir`, uno por uno como pequeñas tareas, y reescribe `commit-message.md` |

:::tip Bloques de 6 tareas
Con más de 6 tareas pendientes, trabaja en bloques de 6 y, en Claude Code, usa `/compact` entre
bloques (o abre una sesión nueva: la reanudación lee el estado de `05`).
:::

## qa-review · la revisión independiente

:::card
<dl class="kv">
<dt>Paso</dt><dd>4 · compuerta G3</dd>
<dt>Quién</dt><dd>Dev o QA, <strong>siempre en una sesión nueva</strong></dd>
<dt>Comando</dt><dd><code>/qa-review &lt;id&gt; [base:&lt;ref&gt;] [head:&lt;ref&gt;]</code></dd>
<dt>Lee</dt><dd><code>pbi.md</code>, <code>04</code> (SPECs), estado de <code>05</code>, <code>06</code>, <code>CHANGELOG.md</code>, <code>fix-plan.md</code>, <code>test-cases.md</code>, el diff</dd>
<dt>Escribe</dt><dd><code>qa-report.md</code>, <code>bitacora.md</code>, una viñeta en <code>commit-message.md</code>, borradores</dd>
<dt>Subagentes</dt><dd><code>qa-reviewer</code> (obligatorio), <code>runtime-tester</code> (opcional)</dd>
<dt>Modelo</dt><dd><code>qa-reviewer</code> en Opus; en Copilot, elige uno de razonamiento</dd>
</dl>
:::

### Para qué sirve

Una revisión **adversarial** del cambio ya implementado contra su diseño aprobado, las reglas de
`AGENTS.md`, la seguridad y las regresiones. `qa-reviewer` intenta romperlo; `runtime-tester`
(opcional) lo prueba con la aplicación arrancada; la sesión **verifica cada hallazgo** antes de
escribirlo. Nunca corrige código: las correcciones van a `/wbs-execution <id> qa`.

### Alcance: base y head

| Argumento | Por defecto | Cuándo indicarlo |
| --- | --- | --- |
| `base:<ref>` | `git merge-base HEAD origin/dev` | Si la rama tiene commits ajenos (por ejemplo, la rama del piloto con el kit) |
| `head:<ref>` | El árbol de trabajo (commits + cambios sin commit + nuevos) | Para revisar un commit concreto. Si no coincide con el árbol, el revisor lee con `git show` y no ejecuta pruebas |

Los archivos del cambio que no son del work item (por ejemplo, archivos del kit) se dejan fuera y el
informe lo dice. La carpeta `docs/sdd/` se lista pero no se revisa como código.

### Severidad

| Severidad | Cuándo | Efecto |
| --- | --- | --- |
| **Alta** | Rompe una SPEC o un criterio; seguridad (autorización, exposición de datos, inyección, secretos); pérdida de datos; regresión en otro rol o flujo | Bloquea el PR |
| **Media** | Defecto con alternativa; SPEC sin prueba negativa; traducción que falta; contrato distinto de 03/04 | Se corrige antes del PR, salvo que aceptes el riesgo |
| **Baja** | Mantenibilidad, nombres, un comentario, un hueco menor de pruebas | No bloquea |

### Ejemplo

:::ask Sesión nueva
/qa-review 40399
:::

:::out Confirmación
## Revisión de QA — 40399 Sección de ofertas en el menú lateral
Alcance: 3f1c2a0..árbol de trabajo · 4 archivos de código (2 nuevos) · docs/sdd/ no se revisa como código
Ronda: 1
Revisor: qa-reviewer (subagente)
Pruebas: dotnet test MiProyecto.Tests · cd ClientApp; yarn test
Runtime: runtime-tester propuesto — cambia una pantalla y AGENTS.md tiene los comandos de arranque
¿Empiezo?
:::

:::out Informe y decisión (G3)
## 🔎 Revisión de QA — 40399 · ronda 1
Resultado: 0 altos · 1 medio · 1 bajo

QA-01 · Media · ClientApp/src/layout/SideMenu.tsx:88 — el rol «Jefe de ventas» no ve «Ofertas»
       (CA-02): la comprobación usa === 'Comercial'. Confirmado con: yarn test (prueba añadida).
QA-02 · Baja · Api/Authorization/Permissions.cs:41 — nombre de constante poco claro.

Para QA-01: A) corregir · B) aceptar el riesgo · C) work item aparte
:::

:::ask Tu decisión
QA-01 A, QA-02 aceptado por Ana Pérez.
:::

Después: `/wbs-execution 40399 qa` (en la sesión de implementación o en otra nueva, **nunca** en la de
QA) y `/qa-review 40399` en otra sesión nueva para la **ronda 2**, que revisa solo las correcciones.
No hay ronda 3: lo que quede abierto lo decides tú.

### Estados de un hallazgo

`Abierto` → `A corregir` → `Corregido (<fecha>)` (lo pone `wbs-execution`) → `Corregido (verificado
<fecha>)` (lo pone la ronda 2). Otros: `Aceptado (riesgo asumido por <persona>, <fecha>)`,
`Descartado (<motivo>)` (la fila no se borra) y `Borrador (_borradores/<slug>.md)`, que pasa a
`Work item #<id>` cuando se crea en Azure DevOps (el borrador se borra antes del PR).

## document-code · documentar lo que cambió

:::card
<dl class="kv">
<dt>Paso</dt><dd>5</dd>
<dt>Quién</dt><dd>Dev, después de <code>qa-review</code> y antes del commit o el PR</dd>
<dt>Comando</dt><dd><code>/document-code &lt;id&gt; [base:&lt;ref&gt;]</code></dd>
<dt>Lee</dt><dd><code>pbi.md</code>, <code>03</code>, <code>04</code> §4.4, <code>06</code>, <code>CHANGELOG.md</code> (o <code>fix-plan.md</code>)</dd>
<dt>Escribe</dt><dd>Comentarios de documentación, <code>docs/</code>, <code>CHANGELOG.md</code>, una viñeta en <code>commit-message.md</code></dd>
<dt>Subagentes</dt><dd><code>doc-writer</code>, <code>code-explorer</code> (si hay más de 5 archivos)</dd>
<dt>Script</dt><dd><code>comment_only.py</code> (prueba que solo cambiaron comentarios)</dd>
</dl>
:::

### Para qué sirve

Documenta **solo lo que el work item tocó**: comentarios `///` (C#) o TSDoc en tipos y miembros
nuevos o cambiados, comentarios de *por qué* donde una decisión no es obvia, y las secciones de
`docs/` afectadas. Nunca cambia comportamiento, y lo demuestra con un script.

### Qué se documenta y dónde

| Qué | Cómo | Cuándo |
| --- | --- | --- |
| Tipo, método público o interno, endpoint, job, DTO, componente, hook nuevo o cambiado | `///` (C#), `/** */` (TS) | Si falta o ya no es correcto |
| Una decisión que alguien podría deshacer por error (03) o un riesgo mitigado (06) | Una o dos líneas `//` con el porqué y `#<id>` | Solo ahí |
| Clase de pruebas nueva | Resumen con las SPECs que cubre | Siempre |
| Endpoint nuevo o cambiado | `docs/api-reference.md`: ruta, método, roles, petición, respuesta, errores | Siempre |
| Regla `BR-XX` no evidente en el código | `docs/reglas-negocio.md` con `#<id>` | Siempre |
| Cambio de capas, patrones o flujo | `docs/architecture.md`, `backend.md` o `frontend.md` | Siempre |
| Entidad o migración | `docs/database.md` | Siempre |
| Decisión de arquitectura que va más allá del work item | Propuesta de ADR en `docs/adr/`, estado `Propuesta` | Pregunta antes |

### Cómo garantiza que solo cambian comentarios

1. Antes de delegar: `comment_only.py save <temp>/sdd-doc-<id> <archivos>` guarda una copia.
2. `doc-writer` escribe.
3. `comment_only.py check …` compara línea a línea: toda línea añadida, quitada o cambiada debe
   ser un comentario o estar en blanco, y la codificación (BOM) y los finales de línea deben ser
   los mismos. Si no, vuelve a `doc-writer` (máximo 2 rondas) o se restaura el archivo.
4. Build sin avisos nuevos (en C#, un XML mal formado da CS1570–CS1587) y lint/tipos en frontend.
5. Lee el diff de `docs/`: cada afirmación debe salir de `pbi.md`, `03`, `04` o el código.

:::out Lo que dice el script
✓ Api/Controllers/OffersController.cs: solo comentarios (6 línea(s) de comentario)
✓ ClientApp/src/layout/SideMenu.tsx: solo comentarios (4 línea(s) de comentario)

Solo cambiaron comentarios
:::

:::out Informe final
## 📝 Documentación — 40399
Cambios: 5 comentarios de documentación (3 nuevos, 2 actualizados) · 1 de porqué · docs/: frontend.md · ADR: ninguno
Validación: comment_only → solo comentarios · build → sin avisos nuevos · lint/tipos → OK
Pendiente: ninguno
Siguiente: el commit con el work item
git add ClientApp/src/layout/SideMenu.tsx Api/Authorization/Permissions.cs docs/frontend.md docs/sdd/40399-…/
:::

:::note Si el work item ya está mezclado
La documentación va en un commit de seguimiento con su propio mensaje completo:
`docs(<ámbito>): documentar <qué>` · `Ref: #<id>`.
:::
