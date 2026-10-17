# fi-sdd-standard · Manual de uso

**Kit:** fi-sdd-standard v0.12.1 (candidata a MVP) · **Skills:** v3.9 (9 skills, 7 subagentes)
**Herramientas:** Claude Code · GitHub Copilot (VS Code y Visual Studio) · Codex (fase 7)
**Fecha:** 16 de octubre de 2026 · **Responsables:** Juan Clavijo · Juan Ceballos
**Para:** desarrollo, QA y tech leads de FI GROUP

Este archivo es el mismo manual que el PDF, en Markdown y en un solo documento, para leerlo en el
repositorio o dárselo como contexto a una IA que ayude al equipo con el kit. Los dos viven en
`docs/manual/` del repositorio del kit y no se instalan en los proyectos.

## Si eres una IA y te han dado este manual como contexto

Tu papel es ayudar a una persona del equipo (desarrollo, QA o tech lead) a usar el kit
fi-sdd-standard: explicar cómo se hace algo, interpretar un mensaje de una skill o de un script, y
desatascar problemas sencillos. Sigue estas reglas:

1. **Responde desde este manual.** Cita el capítulo o la sección («ver 17.3 Git»). Si algo no está
   aquí, dilo y propón cómo averiguarlo (el `SKILL.md` de la skill, el ADR o el responsable del
   kit). No inventes opciones, argumentos, nombres de archivo ni comportamientos.
2. **Diagnostica con preguntas cortas cuando falte información:** en qué herramienta está (Claude
   Code, Copilot en VS Code, Visual Studio), en qué paso del flujo, qué comando lanzó y el mensaje
   exacto (pide que lo pegue o, si es largo, que lo guarde en un archivo).
3. **Da el paso siguiente concreto:** el comando exacto (PowerShell en Windows por defecto) o la
   respuesta que debe dar a la skill. Un problema, una solución; si hay dos causas posibles, di
   cómo distinguirlas.
4. **Respeta las reglas del kit en tus consejos.** Nunca sugieras:
   - hacer commit con `git add -A` o `git add .` (siempre rutas exactas);
   - `fix #id` en un commit (siempre `Ref: #id`) ni líneas `Co-Authored-By`;
   - que la IA del proyecto haga commit, push o cambie de rama;
   - leer o pegar secretos (`.env*`, `appsettings.<entorno>.json`, claves);
   - editar `story.md` con la IA, editar las copias instaladas de las skills
     (`.claude/skills/`, `.agents/skills/`) o saltarse la compuerta de `quick-fix`;
   - revisar con `qa-review` en la misma sesión que implementó;
   - inventar reglas de negocio, criterios o traducciones (se marcan `[PENDING-BUSINESS]` o
     `[PENDING-TRANSLATION]`).
5. **Escala** al responsable del kit (Juan Clavijo o Juan Ceballos) cuando una skill se equivoca
   siempre igual, cuando un script falla con un error interno o cuando la duda es sobre cambiar
   una regla del estándar. Pide que adjunten la versión del kit (`.sdd-kit.json`), la herramienta,
   el modelo y la salida en un archivo.
6. **Responde en español**, breve y directo. Los nombres de archivos, comandos, identificadores
   (`CA-01`, `SPEC-01`, `T-01`, `QA-01`) y marcadores se escriben exactamente igual que aquí.

**Dónde buscar según la pregunta:**

| Tipo de pregunta | Sección |
| --- | --- |
| «¿Qué es…?» (skill, subagente, marcador, compuerta, sello) | 2.3 Glosario |
| «¿Qué paso sigue?» / «¿Qué archivo crea…?» | 3. El flujo de un work item |
| Instalar, actualizar, proyecto nuevo o existente | 5. Instalación |
| Una skill concreta: argumentos, pasos, confirmaciones, paradas | 6, 7 y 8 |
| Un subagente | 9. Subagentes |
| Una plantilla o un archivo de la carpeta del work item | 10. Prompts y plantillas |
| Un script: opciones y salida | 11. Scripts |
| Un bloqueo del hook, permisos, `sdd-guardrails.json`, pruebas de arquitectura | 12. Guardarraíles |
| Marcadores, sello, anclas, bitácora | 13 |
| Commit, PR, ramas | 14. Git, commit y PR |
| «¿Cómo hago…?» de principio a fin | 15. Recetas |
| Cómo responder a la IA de la skill | 16. Cómo hablarle a la IA |
| Un error o síntoma | 17. Solución de problemas y Preguntas frecuentes (al final) |
| Chuleta | 18. Referencia rápida |

## Contenido

1. Cómo usar este manual
2. Qué es fi-sdd-standard
3. El flujo de un work item
4. Herramientas y dónde vive cada cosa
5. Instalación
6. Skills del flujo principal (`enrich-us`, `technical-analysis`, `wbs-execution`, `qa-review`, `document-code`)
7. Vía rápida y QA (`quick-fix`, `enrich-us … qa`, `test-cases`)
8. Skills de proyecto (`project-context`, `document-project`)
9. Subagentes
10. Prompts y plantillas
11. Scripts
12. Guardarraíles
13. Marcadores, sellos, anclas y bitácora
14. Git, commit y PR
15. Recetas
16. Cómo hablarle a la IA
17. Solución de problemas
18. Referencia rápida
- Anexo · Decisiones del estándar (ADR)
- Preguntas frecuentes

**Convenciones de este archivo:** los bloques **Lo que pides** son mensajes que se escriben en el
chat de la herramienta; **Lo que responde**, lo que devuelve la skill o el script; **Comando**, lo
que se ejecuta en la terminal; **Archivo**, el contenido de un archivo. Las salidas de los scripts
son reales (kit v0.12.1); las respuestas de la IA siguen el formato exacto de cada skill, pero su
texto varía de una sesión a otra. Los avisos usan alertas de GitHub: `[!NOTE]` nota, `[!TIP]`
consejo, `[!WARNING]` atención, `[!CAUTION]` nunca.

---

## 1. Cómo usar este manual

Este manual explica de principio a fin cómo se trabaja con **fi-sdd-standard**: qué es cada pieza,
cuándo se usa, qué le pides a la IA, qué te devuelve y qué haces tú en cada momento. Al terminarlo
deberías poder instalar el kit en un proyecto, llevar un work item de Azure DevOps hasta el PR y
saber qué hacer cuando algo se para.

### 1.1 Qué encontrarás

El manual va de lo general a lo concreto. Los primeros capítulos dan el mapa; los del centro son la
referencia de cada pieza, y los últimos son recetas y soluciones para el día a día.

| Parte | Capítulos | Para qué |
| --- | --- | --- |
| El mapa | 2 · Conceptos · 3 · El flujo · 4 · Herramientas | Entender qué es el kit, cómo se encadenan los pasos y dónde vive cada cosa |
| Empezar | 5 · Instalación | Instalar el kit en un proyecto existente o nuevo, y actualizarlo |
| Referencia | 6 a 13 | Cada skill, subagente, prompt, plantilla, script, guardarraíl y marcador, en detalle |
| Trabajo diario | 14 · Git y PR · 15 · Recetas · 16 · Cómo pedir | Casos completos, de principio a fin, y cómo hablarle a la IA |
| Cuando algo falla | 17 · Problemas · 18 · Referencia rápida | Errores frecuentes y una hoja de consulta |

### 1.2 Por dónde empezar según tu rol

**Desarrollo**

1. Capítulos 2 y 3: el flujo completo.
2. Capítulo 6: las skills del flujo, sobre todo `enrich-us`, `technical-analysis` y `wbs-execution`.
3. Capítulo 7: `quick-fix` para bugs pequeños.
4. Capítulos 14 y 15: el commit, el PR y las recetas.

**QA**

1. Capítulos 2 y 3: el flujo y dónde entra QA.
2. Capítulo 7: el modo `qa` de `enrich-us` y `test-cases`.
3. Capítulo 6: `qa-review`, la revisión independiente antes del PR.
4. Capítulo 15: las recetas de QA.

**Tech lead**

1. Capítulo 5: instalación y actualización.
2. Capítulo 8: `project-context` y `document-project`.
3. Capítulo 12: los guardarraíles y `sdd-guardrails.json`.
4. Capítulo 14: llevar el piloto a `dev`.

### 1.3 Convenciones de este manual

Los ejemplos usan un proyecto ficticio con el work item **#40399 «Sección de ofertas en el menú
lateral»** y el bug **#41020 «El total de la factura redondea mal los céntimos»**. Las salidas de
scripts son reales: se generaron con el kit v0.12.0. Las respuestas de la IA son representativas:
siguen el formato exacto que fija cada skill, pero el texto varía de una sesión a otra.

**Lo que pides:**

```text
Así se ve un mensaje que tú escribes en el chat de la herramienta.
```

**Lo que responde:**

```text
Así se ve lo que la IA o un script te devuelve.
```

**Comando:**

```text
python .agents/scripts/pr-check.py    # así, un comando que ejecutas en la terminal
```

> [!NOTE]
> **Nota**
>
> Información que conviene saber.

> [!TIP]
> **Consejo**
>
> Una forma mejor de hacer algo.

> [!WARNING]
> **Atención**
>
> Algo que, si se ignora, cuesta tiempo o rehacer trabajo.

> [!CAUTION]
> **Nunca**
>
> Algo que rompe una regla del equipo.

Otras convenciones:

- `<id>` es el ID del work item en Azure DevOps (por ejemplo `40399`) y `<carpeta>` es su carpeta,
  `docs/sdd/<id>-<título>/`.
- `<kit>` es la ruta donde tienes el kit descargado (por ejemplo `C:\Users\tu-usuario\Documents\fi-sdd-standard`).
- Los comandos van en PowerShell (Windows) salvo que se diga otra cosa. En macOS o Linux cambia `\`
  por `/`.
- Los nombres de archivos, identificadores (`CA-01`, `SPEC-01`, `T-01`, `QA-01`) y marcadores se
  escriben siempre igual: las skills los buscan por su nombre exacto.

### 1.4 Qué no es este manual

No sustituye a los archivos del kit. Las instrucciones exactas que sigue la IA están en cada
`SKILL.md`, y las decisiones del estándar en los ADR de `docs/adr/` del kit. Si algo de este manual
contradice un `SKILL.md`, manda el `SKILL.md`, y conviene avisar al responsable del kit para
corregir el manual.

El manual vive en `docs/manual/` del repositorio del kit, en PDF y en Markdown (este último, pensado
para dárselo de contexto a una IA). No se copia a los proyectos al instalar el kit.

---

## 2. Qué es fi-sdd-standard

fi-sdd-standard es el kit del equipo para trabajar con IA siguiendo un mismo método, el SDD
(*Spec-Driven Development*): primero se especifica, luego se diseña, después se implementa con
pruebas y al final se revisa y se documenta. Funciona igual en Claude Code, GitHub Copilot y Codex.

### 2.1 El problema que resuelve

Sin un método común, cada persona usa la IA a su manera: unos le piden el código directamente,
otros le pegan medio work item, otros le dejan hacer commit. El resultado es desigual y difícil de
revisar: no se sabe qué decidió la IA, de dónde sacó una regla de negocio ni si las pruebas se
ejecutaron de verdad.

El kit fija **el mismo camino para todos**:

- El requisito sale de Azure DevOps y se copia, tal cual, en un archivo del repositorio.
- Cada paso deja un documento versionado con lo que se decidió y quién lo confirmó.
- La IA no inventa reglas de negocio, criterios ni traducciones: pregunta o los marca.
- La IA nunca hace commit, push ni cambia de rama. Las personas aprueban en cuatro puntos fijos.
- Las reglas obligatorias se comprueban con scripts y pruebas, no solo con instrucciones.

### 2.2 Qué contiene el kit

| Pieza | Qué es | Cuántas | Dónde se instala en tu proyecto |
| --- | --- | --- | --- |
| **Reglas base** | Las reglas comunes a todos los proyectos que la IA lee siempre | 1 bloque | `AGENTS.md` (entre marcadores del kit) |
| **Skills** | Instrucciones de un paso del flujo, con plantillas y scripts | 9 | `.agents/skills/` y `.claude/skills/` |
| **Subagentes** | Asistentes especializados a los que una skill delega una tarea acotada | 7 | `.github/agents/` y `.claude/agents/` |
| **Prompts** | Atajos de Copilot que fijan el modelo de una skill | 1 | `.github/prompts/` |
| **Plantillas** | Estructura fija de cada documento del flujo | 32 | Dentro de cada skill (`templates/`), en la raíz y en `docs/adr/` |
| **Scripts** | Comprobaciones y utilidades deterministas en Python | 11 | En el kit y en `.agents/scripts/` o dentro de cada skill |
| **Guardarraíles** | Permisos, un hook y una configuración que frenan lo prohibido | 3 piezas | `.claude/settings.json`, `.agents/hooks/`, `sdd-guardrails.json` |
| **Plantilla de commit** | El formato de mensaje de commit del equipo | 1 | `.gitmessage` |

### 2.3 Glosario

| Término | Significado |
| --- | --- |
| **SDD** | *Spec-Driven Development*: el código se escribe a partir de una especificación aprobada (criterios, diseño, SPECs), no al revés. |
| **Work item** | El PBI o bug de Azure DevOps. Es la fuente del requisito. Su ID da nombre a la carpeta de trabajo. |
| **PBI** | *Product Backlog Item*: una funcionalidad nueva o un cambio. Sale `pbi.md`. |
| **Bug** | Un defecto. Sale `bug.md`. Si es pequeño, puede ir por la vía rápida. |
| **Carpeta del work item** | `docs/sdd/<id>-<título>/`. Todo lo que el flujo produce para ese work item vive ahí y se versiona. |
| **`story.md`** | El work item copiado de Azure DevOps por una persona, con sus imágenes en `assets/`. La IA lo lee y **nunca lo edita**. |
| **Skill** | Un paso del flujo empaquetado: un `SKILL.md` con las instrucciones, más plantillas y scripts. Se invoca con `/nombre`. |
| **Subagente** | Un asistente con un rol, permisos y modelo propios. La skill le pasa un *paquete cerrado* con todo lo que necesita y recibe un informe. |
| **Paquete cerrado** | Lo que una skill le da a un subagente: la tarea, sus SPECs, los archivos, los comandos y las reglas. El subagente no lee el diseño por su cuenta. |
| **Sesión principal** | La conversación en la que tú escribes. Las skills que piden confirmación corren ahí. |
| **Sesión nueva** | Una conversación vacía. Se usa para cada paso grande y, obligatoriamente, para `qa-review`. |
| **Compuerta (G1–G4)** | Un punto donde una persona aprueba antes de seguir. |
| **SPEC** | Una especificación verificable en formato *Dado / Cuando / Entonces*, en `04-implementation-plan.md`. Cada criterio de aceptación tiene al menos una. |
| **WBS** | *Work Breakdown Structure*: la lista de tareas `T-01`, `T-02`… con sus puntos de historia, en `05-wbs-estimation.md`. |
| **Marcador** | Una etiqueta en el texto que señala un hueco: `[PENDING-BUSINESS]`, `[REQUIRES-VALIDATION]`, `[ASSUMPTION-BASED]`, `[PENDING-TRANSLATION]`. |
| **Sello** | La línea `**Generado con:** <skill> v3.9 · <herramienta> · <modelo>` al inicio de cada documento generado. Es la evidencia de que lo hizo la IA. |
| **Ancla** | Un comentario `<!-- sdd:... -->` que marca una sección para que la siguiente skill la encuentre, aunque cambie el título. |
| **Bitácora** | `bitacora.md`: las notas de trabajo con fecha (preguntas, respuestas, decisiones, hallazgos). Solo crece. |
| **Guardarraíl** | Un mecanismo que impide o detecta lo prohibido: permisos `deny`, el hook `sdd_guard.py`, las pruebas de arquitectura y `pr-check.py`. |
| **Hook** | Un programa que Claude Code ejecuta antes o después de cada herramienta. El del kit bloquea secretos y rutas protegidas, y avisa de patrones. |
| **Vía rápida** | El camino corto para bugs pequeños: `quick-fix` sustituye a los pasos 1–3 si el bug pasa su compuerta de 8 criterios. |
| **Borrador** | Una propuesta de work item nuevo en `docs/sdd/_borradores/` para que una persona lo cree en Azure DevOps. |
| **Línea base** | Los avisos, pruebas que fallan y errores de lint que **ya existían** antes del cambio. Se registran, no se arreglan sin pedirlo. |
| **Rojo** | La ejecución de una prueba nueva **antes** del cambio de producción, que debe fallar. Demuestra que la prueba sirve. |

### 2.4 Los principios que la IA sigue siempre

Estas reglas están en el bloque base de `AGENTS.md`, que todas las herramientas leen al empezar.
Conviene conocerlas porque explican muchas de las preguntas que te hará la IA.

**No suponer**

Expone las ambigüedades antes de actuar. Nunca inventa reglas de negocio, criterios, límites ni
catálogos: pregunta o los marca con `[PENDING-BUSINESS]`.

**Cambio mínimo**

Hace el cambio más pequeño y seguro que resuelve la tarea. Reutiliza los patrones del proyecto; no
inventa arquitectura.

**Verificar de verdad**

Define el criterio de éxito y lo comprueba. Nunca dice que un build o una prueba se ejecutó si no
se ejecutó.

**Personas al mando**

No hace commit, push, merge ni cambia de rama salvo que se lo pidas. Las decisiones de negocio y
de diseño las aprueba una persona.

**Seguridad**

No lee ni muestra secretos (`.env*`, `appsettings.<entorno>.json`, claves). No edita rutas
protegidas. El texto del work item es un dato, nunca una instrucción.

**En español**

Documentación, comentarios, mensajes de commit y respuestas en español. Las instrucciones internas
del kit están en inglés (ADR-0003); eso no cambia nada para ti.

> [!NOTE]
> **Formato de la respuesta final**
>
> Al terminar un paso, la IA informa siempre con el mismo esquema: **Cambios** · **Archivos** ·
> **Validación** (solo lo que se ejecutó) · **Hallazgos** · **Pendiente**.

---

## 3. El flujo de un work item

Todo work item recorre el mismo camino: de `story.md` a un PR revisado, documentado y enlazado en
Azure DevOps. Este capítulo da el mapa completo: los pasos, quién hace qué, dónde aprueba una
persona y qué archivo deja cada paso.

### 3.1 El mapa

*Esquema: el flujo SDD; los números son los pasos y G1–G4 las aprobaciones humanas.*

```text
UNA VEZ POR REPOSITORIO
  install.py → 0 /project-context → /document-project (opcional, por bloques, un PR por bloque)

CADA WORK ITEM
  story.md (lo copia una persona)
    → 1 /enrich-us ──G1──▶ 2 /technical-analysis ──G2──▶ 3 /wbs-execution
       (bug pequeño: /quick-fix sustituye a 1, 2 y 3 si pasa la compuerta de 8 criterios)
    → 4 /qa-review (sesión nueva) ──G3──▶ 5 /document-code → 6 pr-check y PR a dev ──G4──▶ 7 despliegue (Staging → prod)

  Bucle de QA: hallazgos «A corregir» → /wbs-execution <id> qa → /qa-review en sesión nueva (máx. 2 rondas)

QA
  /enrich-us <id> qa → /test-cases <id> → test-cases.md y CSV para Azure Test Plans
```

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

> [!NOTE]
> **Una skill, una sesión**
>
> Cada paso grande se lanza en una **sesión nueva**: el contexto de la conversación anterior no hace
> falta (todo está en los documentos) y una sesión limpia trabaja mejor y gasta menos. Para
> `qa-review` es obligatorio: la sesión que implementó el cambio no puede revisarlo.

### 3.2 Las cuatro compuertas

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

### 3.3 La carpeta del work item

Todo lo que el flujo produce para un work item vive en una sola carpeta junto al código (ADR-0002):
`docs/sdd/<id>-<título>/`. El título va en minúsculas, sin acentos y con guiones, como máximo 40
caracteres: `docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/`. Casi todo se versiona; lo que
duplica algo ya guardado o se regenera igual se queda en tu equipo (ADR-0027, columna *¿Se versiona?*).

*Esquema: los archivos de la carpeta del work item, quién o qué paso crea cada uno y para qué sirve.*

```text
docs/sdd/<id>-<título>/
├── story.md              persona       el work item tal cual
├── assets/               persona       imágenes y archivos del work item (local, no se versiona)
├── bitacora.md           todas         preguntas, decisiones, hallazgos
├── pbi.md | bug.md       paso 1        requisito técnico completo (contrato funcional)
├── 00 … 06               paso 2        diseño, plan, WBS, riesgos
├── fix-plan.md           vía rápida    sustituye a 00–06
├── CHANGELOG.md          paso 3        qué se hizo y cómo se verificó
├── commit-message.md     paso 3        mensaje del commit y del PR (local, no se versiona)
├── qa-report.md          paso 4        hallazgos y decisiones
└── test-cases.md · .csv  QA            casos; el CSV de Azure Test Plans es local
```

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

### 3.4 Reglas que no cambian nunca

> [!CAUTION]
> **Las reglas fijas del flujo**
>
> - `story.md` lo prepara una persona y la IA nunca lo edita. Si algo falta, se corrige en Azure
>   DevOps y se vuelve a copiar.
> - La IA nunca hace commit, push, merge ni cambia de rama salvo que se lo pidas. Los permisos de
>   Claude Code lo bloquean además.
> - Un commit por work item. Siempre `Ref: #<id>`, nunca `fix #<id>` (Azure Repos cerraría el work
>   item). Sin líneas `Co-Authored-By`: el sello SDD es la evidencia.
> - `git add` con rutas exactas, nunca `git add -A` ni `git add .`.
> - `qa-review` siempre en una sesión distinta de la que implementó.
> - Nada de secretos: ni leerlos ni copiarlos en comentarios, documentos o commits.
> - Al repositorio no van `assets/`, `commit-message.md`, `test-cases.csv` ni los borradores (ADR-0027).
> - Toda decisión confirmada pasa de `bitacora.md` a `pbi.md`/`bug.md`, que es el contrato.

### 3.5 Ramas y despliegue

El modelo de ramas es el de ADR-0006:

| Rama | Para qué | Quién la crea |
| --- | --- | --- |
| `feature/<id>-<título>` | Un PBI | El dev, desde `dev` |
| `fix/<id>-<título>` | Un bug (vía rápida o flujo completo) | El dev, desde `dev` |
| `chore/…` · `docs/…` | Cambios del kit, del contexto o de documentación | El dev o el tech lead |
| `dev` | Integración; destino de los PR | — |
| `main` | Staging, y de ahí producción | El pipeline, tras aprobar |

> [!TIP]
> **Las skills comprueban la rama**
>
> `quick-fix`, `project-context` y `document-project` se paran si estás en `dev` o `main`, y te piden
> crear la rama. `wbs-execution` te recuerda al final cuál es la rama esperada antes del commit.

---

## 4. Herramientas y dónde vive cada cosa

El kit tiene una sola fuente (`core/` del repositorio del kit) y el instalador la copia al formato
que lee cada herramienta. Así, una misma skill funciona igual en Claude Code y en Copilot, y una
corrección se hace una sola vez.

### 4.1 Herramientas soportadas

| Herramienta | Estado en el MVP | Subagentes | Hooks | Cómo se invoca una skill |
| --- | --- | --- | --- | --- |
| **Claude Code** (terminal, VS Code, escritorio) | Flujo completo, probado en Bonis | Sí (herramienta *Agent*) | Sí | `/enrich-us 40399` |
| **GitHub Copilot en VS Code** (modo agente) | Flujo completo, en pruebas (ola 3) | Sí (`runSubagent`) | No: el pipeline y `pr-check.py` cubren las reglas | `/enrich-us 40399` |
| **GitHub Copilot en Visual Studio** | Carga de reglas y skills, y pasos sueltos | No: la sesión hace todo el trabajo | No | `/enrich-us 40399` (desde 17.14/18.5) o pidiéndolo en el chat |
| **Codex** | Fase 7 | — | — | — |

> [!NOTE]
> **Si la herramienta no tiene subagentes**
>
> Todas las skills funcionan sin subagentes: la sesión principal hace el trabajo con las mismas
> reglas y lo dice en su confirmación («*Writer: this session (the tool has no subagents)*»). Solo
> se pierde la separación de contexto y, en `qa-review`, conviene elegir a mano un modelo de
> razonamiento.

### 4.2 Qué se instala y dónde

*Esquema: el instalador copia la fuente única del kit al formato de cada herramienta.*

```text
fi-sdd-standard (core/, fuente única)
  └─ install.py --tools copilot,claude,visualstudio
       ├─ .agents/skills/    versionado · Copilot, Codex
       ├─ .claude/skills/    local (gitignore) · Claude Code
       ├─ .github/agents/    versionado · Copilot
       └─ .claude/agents/    local (gitignore) · Claude Code
Lo versionado viaja con el repositorio; lo local lo regenera install.py en cada equipo.
```

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

> [!WARNING]
> **No edites las copias generadas**
>
> Los archivos de `.claude/skills/` y `.claude/agents/` empiezan con
> `# GENERATED from fi-sdd-standard by scripts/install.py - do not edit this copy`. Si cambias algo
> ahí, el próximo `install.py` lo sobrescribe. Las mejoras se hacen en el kit (`core/`) y se
> reinstalan. Lo mismo vale para `.agents/skills/`: `pr-check.py` da error si una rama cambia un
> archivo del kit sin un commit `chore(sdd)`.

### 4.3 El archivo AGENTS.md

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

> [!TIP]
> **Por qué los encabezados están en inglés**
>
> Las instrucciones internas del kit están en inglés (ADR-0003) y las skills buscan las secciones de
> *Project context* por su nombre exacto. El contenido puede estar en español.

### 4.4 Modelos

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

### 4.5 MCP de Azure DevOps

El kit trae plantillas para conectar el MCP de Azure DevOps en **solo lectura** (ADR-0008,
propuesta): `core/templates/mcp/vscode-mcp.json` (VS Code), `claude-mcp.json` y
`claude-settings-mcp.json` (Claude Code). Con el MCP activo y declarado en `AGENTS.md`,
`enrich-us` puede leer el work item y escribir `story.md` por ti, que luego **revisas**. Mientras
TI no confirme el acceso con Entra ID, `story.md` se copia a mano. La guía está en
`docs/guias/mcp-azure-devops.md` del kit.

---

## 5. Instalación

El kit se instala en cada repositorio con un script. En un proyecto existente, después viene
`/project-context`, que escribe el contexto real del proyecto; en uno nuevo, lo mismo cuando haya
algo de código. Este capítulo cubre los dos casos y cómo actualizar el kit más adelante.

### 5.1 Requisitos

| Requisito | Para qué | Cómo comprobarlo |
| --- | --- | --- |
| Python 3.10 o superior | Instalador, scripts, hook | `python --version` |
| Git | Todo el flujo | `git --version` |
| El kit descargado | La fuente de la instalación | Zip `fi-sdd-standard-v<versión>.zip` descomprimido, o un clon del repositorio del kit |
| Claude Code y/o GitHub Copilot (agente) | Ejecutar las skills | `/` en el chat muestra las skills tras instalar |
| El SDK y las herramientas del proyecto (.NET, Node…) | Que la IA pueda compilar y probar | Lo que diga el README del proyecto |

> [!TIP]
> **Dónde dejar el kit**
>
> Ponlo al lado de tus repositorios, por ejemplo `C:\Users\<tú>\Documents\fi-sdd-standard`, y
> comprueba la versión antes de instalar:
> 
> ```powershell
> cd C:\Users\<tú>\Documents\fi-sdd-standard
> git log --oneline -1          # v0.12.0
> python scripts\validate.py    # 9 skills · 7 agents checked · 0 errors · 0 warnings
> ```

### 5.2 El instalador: install.py

```powershell
python <kit>\scripts\install.py --target <ruta-del-proyecto> --tools copilot,claude [--dry-run]
```

| Opción | Valores | Qué hace |
| --- | --- | --- |
| `--target` | Ruta del repositorio | Dónde se instala (obligatorio) |
| `--tools` | `copilot`, `claude`, `visualstudio`, separados por comas | `copilot` instala `.agents/skills/` y `.github/agents/` (versionados); `claude` genera las copias locales de `.claude/`, los permisos y los hooks; `visualstudio` genera `.github/copilot-instructions.md` desde `AGENTS.md`. Por defecto: `copilot` |
| `--dry-run` | — | Muestra lo que haría sin escribir nada. Úsalo siempre la primera vez |

**Nunca sobrescribe archivos del proyecto.** Solo crea lo que falta y actualiza lo que instaló el
propio kit (lista en `.sdd-kit.json`). Cada línea de su salida dice qué pasó:

| Estado | Significado | Qué haces |
| --- | --- | --- |
| `creado` | El archivo no existía y lo ha creado | Nada |
| `actualizado` | Era del kit y ha cambiado con la nueva versión | Revisa el diff antes del commit |
| `igual` | Ya estaba en esta versión | Nada |
| `existe` | Es un archivo de configuración del proyecto que ya existía: no se toca | Nada |
| `PENDIENTE` | Falta un paso tuyo | Lee el mensaje: casi siempre es `/project-context` |
| `REVISAR` | Hay algo que conviene mirar a mano | Lee el mensaje (por ejemplo, un `.gitignore` que ignora `.claude/settings.json`) |
| `CONFLICTO` | Hay un archivo con ese nombre que **no es del kit**: no se toca | Decide si el del proyecto se queda o se sustituye a mano |

### 5.3 Proyecto existente, paso a paso

Ejemplo: un repositorio .NET + React que nunca ha usado el kit.

**1. Rama de trabajo.** La instalación es un cambio como cualquier otro:

```powershell
cd C:\repos\mi-proyecto
git switch dev; git pull
git switch -c chore/sdd-kit
```

**2. Simulación y luego instalación:**

```powershell
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude --dry-run
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
```

**Salida real del instalador (resumida):**

```text
fi-sdd-standard v0.12.0 · Instalación en C:\repos\mi-proyecto

  creado       .agents/skills/document-code/SKILL.md
  ...                                              (las 9 skills con plantillas y scripts)
  creado       .github/prompts/wbs-execution-sonnet.prompt.md
  creado       .claude/skills/...                  (copia local para Claude Code)
  actualizado  .gitignore (+9 líneas)
  creado       .github/agents/backend-dev.agent.md
  creado       .claude/agents/backend-dev.md
  ...                                              (los 7 subagentes, en los dos formatos)
  actualizado  .gitignore (+7 líneas)
  creado       .agents/hooks/sdd_guard.py
  creado       .agents/scripts/pr-check.py
  creado       .agents/scripts/check-sdd-item.py
  creado       .agents/scripts/check-encoding.py
  creado       sdd-guardrails.json
  PENDIENTE    sdd-guardrails.json: /project-context añade las rutas protegidas y los patrones
  creado       .claude/settings.json (+20 reglas deny, hooks del kit)
  creado       .gitmessage
  creado       AGENTS.md
  PENDIENTE    AGENTS.md: ejecuta /project-context para escribir «Project context»
  creado       CLAUDE.md
  creado       docs/adr/0000-plantilla.md
  creado       docs/sdd/
  actualizado  .gitignore (+5 líneas)                (lo que no se versiona, ADR-0027)
  creado       .sdd-kit.json

  PENDIENTE: 2 · actualizado: 2 · creado: 105

  Siguiente: revisa los PENDIENTE / REVISAR de arriba  ·  git config commit.template .gitmessage
             ·  /project-context en una sesión nueva (contexto del proyecto, documentación base y pruebas)
```

Si el proyecto ya tenía un `AGENTS.md` o un `CLAUDE.md` propios, el instalador no los pisa:

- `AGENTS.md` sin las marcas del kit → `PENDIENTE AGENTS.md sin marcas del kit`. `/project-context`
  usa su contenido como fuente y reconstruye el archivo con las marcas.
- `CLAUDE.md` con contenido propio → `PENDIENTE CLAUDE.md no importa @AGENTS.md`. `/project-context`
  propone pasar ese conocimiento a `AGENTS.md` o a `docs/` y dejar `CLAUDE.md` en `@AGENTS.md`.
- Un `.gitignore` que ignora `.claude/` entero → `REVISAR`: añade `!.claude/settings.json` al
  final, porque los permisos y hooks del equipo se versionan.

**3. Plantilla de commit** (una vez por equipo y repositorio):

```powershell
git config commit.template .gitmessage
```

**4. Primer commit, con rutas exactas:**

```powershell
git status --short
git add .agents .github/agents .github/prompts .claude/settings.json AGENTS.md CLAUDE.md `
        .gitignore .gitmessage .sdd-kit.json sdd-guardrails.json docs/adr docs/sdd
git status --short          # no debe quedar nada del kit fuera, salvo .claude/skills y .claude/agents
git commit -m "chore(sdd): instalar fi-sdd-standard v0.12.0"
```

> [!NOTE]
> **Lo que no entra en el commit**
>
> El instalador añade al `.gitignore` lo que no se versiona (ADR-0027): de cada work item, `assets/`,
> `commit-message.md` y `test-cases.csv`; y `.claude/settings.local.json` y
> `.github/copilot-instructions.md`. Además, `.claude/skills/` y `.claude/agents/` son copias locales:
> y cada persona las genera en su equipo con `install.py`.

**5. Contexto del proyecto.** Cierra y vuelve a abrir la herramienta (para que cargue las skills, los
agentes y los hooks) y, en una **sesión nueva**:

**Lo que pides:**

```text
/project-context
```

La skill inventaría el repositorio, ejecuta build, pruebas, lint y type check para verificar los
comandos y registrar la línea base, te hace las preguntas que el código no responde y te enseña un
borrador. Al aprobarlo escribe *Project context*, los seis `docs/*.md` base, el proyecto de
pruebas si no había, las pruebas de arquitectura y `sdd-guardrails.json`. Detalle en el capítulo 8.

Al terminar, comprueba:

```powershell
python .agents\skills\project-context\scripts\check_project.py     # 0 errores
```

y haz el commit que te propone: `chore(sdd): añadir el contexto del proyecto y la documentación base`.

**6. (Opcional) Documentación completa.** `/document-project` crea un plan por áreas y documenta
el proyecto por bloques, un PR por bloque. Detalle en el capítulo 8.

**7. Llevarlo a `dev`.** PR de `chore/sdd-kit` a `dev` con el tech lead como revisor (capítulo 14).
Después del merge, cada desarrollador, en su copia:

```powershell
git switch dev; git pull
python <kit>\scripts\install.py --target . --tools copilot,claude   # genera sus copias de .claude/
git config commit.template .gitmessage
```

### 5.4 Proyecto nuevo

En un repositorio vacío o recién creado la instalación es la misma; lo único que cambia es el
contexto, que todavía no tiene de dónde salir.

```powershell
mkdir C:\repos\nuevo; cd C:\repos\nuevo
git init -b dev
python <kit>\scripts\install.py --target . --tools copilot,claude
git config commit.template .gitmessage
git add .agents .github .claude/settings.json AGENTS.md CLAUDE.md .gitignore .gitmessage .sdd-kit.json sdd-guardrails.json docs
git commit -m "chore(sdd): instalar fi-sdd-standard v0.12.0"
```

`check_project.py` dará errores de `docs/` y del contexto: es lo esperado mientras no haya código.

**check_project.py en un repositorio recién instalado:**

```text
Contexto del proyecto: nuevo

  ✓ AGENTS.md — bloque del kit
  ✗ Project context — faltan los encabezados fijos: What this is, Commands, Local run, ...
  ⚠ Project context — sin el sello «Generado con: project-context» (¿escrito a mano?)
  ✓ AGENTS.md — 69 líneas
  ⚠ Project context — sin la marca sdd:context (fecha y fuentes): no se pueden detectar cambios
  ✓ CLAUDE.md — importa @AGENTS.md
  ✗ docs/architecture.md — no existe
  ...
  7 errores · 2 avisos
```

Orden recomendado en un proyecto nuevo:

1. Crea el esqueleto de la solución (proyectos, capas, proyecto de pruebas) como de costumbre, o
   con un primer work item cuyo `story.md` describa la estructura deseada.
2. En cuanto haya algo que compilar, `/project-context` en `new`: registra los comandos, crea lo que
   falte del proyecto de pruebas y las pruebas de arquitectura **desde el primer día**, y deja
   `docs/` con sus encabezados fijos.
3. Rellena `sdd-guardrails.json` (rutas protegidas, formateadores, patrones) con la propuesta de
   `/project-context`.
4. Cada work item siguiente sigue el flujo normal. `document-code` mantiene `docs/` al día work
   item a work item, así que `/document-project` no hace falta.

### 5.5 Actualizar el kit

Cuando sale una versión nueva:

```powershell
cd <kit>; git pull        # o descomprime el zip nuevo en lugar del anterior
python scripts\validate.py
cd <proyecto>
git switch -c chore/sdd-kit-v0.13.0 origin/dev
python <kit>\scripts\install.py --target . --tools copilot,claude
git status --short
git diff --stat
```

- Los archivos del kit salen como `actualizado`; los tuyos, nunca.
- El bloque del kit de `AGENTS.md` se reemplaza; *Project context* no se toca.
- `.claude/settings.json` se fusiona: se sustituyen los hooks del kit y se añaden las reglas `deny`
  que falten, sin borrar las tuyas.
- Lee el `CHANGELOG.md` del kit: algunas versiones piden un paso (por ejemplo,
  `/project-context check` para rellenar una clave nueva de `sdd-guardrails.json`).

Commit con un mensaje fijo y rutas exactas:

```powershell
git add .agents .github/agents .github/prompts .claude/settings.json AGENTS.md .gitignore .sdd-kit.json sdd-guardrails.json
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.13.0"
```

> [!WARNING]
> **Por qué el prefijo chore(sdd)**
>
> `pr-check.py` da error si una rama cambia archivos del kit sin un commit `chore(sdd)`: así nadie
> modifica una skill instalada a mano por accidente.

### 5.6 Qué se versiona y qué no

El criterio (ADR-0027): se versiona lo que un paso posterior o una persona necesita desde otra
máquina, o lo que es una decisión o una evidencia que no se puede reproducir. No se versiona lo que
duplica algo ya guardado (git, el PR, Azure DevOps), lo que un script regenera igual ni lo personal.

| Se versiona | No se versiona (`.gitignore`) |
| --- | --- |
| `.agents/` (skills, hook, scripts): Copilot lo lee de ahí y todo el equipo usa la misma versión | `.claude/skills/`, `.claude/agents/`: copias que genera `install.py` |
| `.github/agents/`, `.github/prompts/` | `.github/copilot-instructions.md`: copia de `AGENTS.md` para Visual Studio, la genera `install.py --tools visualstudio` |
| `.claude/settings.json` (permisos y hooks del equipo) | `.claude/settings.local.json` (personal) |
| `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`, `sdd-guardrails.json` | — |
| `docs/`: contexto, ADR y `docs/sdd/` | De cada work item: `assets/`, `commit-message.md`, `test-cases.csv` |
| `docs/sdd/_documentacion/` mientras dure el plan | `docs/sdd/_borradores/`: no llega a `dev` (`pr-check.py` lo bloquea) |

> [!TIP]
> **Un adjunto que es la especificación**
>
> Si un mockup aprobado es la única especificación posible y quieres que viaje con el código,
> añádelo a propósito: `git add -f docs/sdd/<carpeta>/assets/<archivo>`. `pr-check.py` lo deja
> pasar con un aviso.

#### Si el proyecto ya versionaba esos archivos

En un proyecto que usaba el kit antes de la v0.12.0, `install.py` avisa con `REVISAR` de los que
ya estaban en git (por ejemplo, `commit-message.md` de work items antiguos). No borra nada. Para
dejar de versionarlos sin borrarlos de tu disco:

```powershell
git rm -r --cached --ignore-unmatch "docs/sdd/*/commit-message.md" "docs/sdd/*/test-cases.csv" "docs/sdd/*/assets/*"
git commit -m "chore(sdd): dejar de versionar los archivos locales del flujo (ADR-0027)"
```

Lo que ya estaba en el historial sigue ahí; a partir de este commit no se vuelve a subir.

#### El manual

El manual (PDF y Markdown) vive en `docs/manual/` del repositorio del kit, con sus fuentes. No se
instala en los proyectos: se consulta en el kit, y el Markdown se puede dar de contexto a una IA.

---

## 6. Skills del flujo principal

Una skill es un paso del flujo empaquetado: instrucciones, plantillas y scripts que la IA sigue al
pie de la letra. Este capítulo explica cómo es una skill por dentro y detalla las cinco del flujo
principal: `enrich-us`, `technical-analysis`, `wbs-execution`, `qa-review` y `document-code`.

### 6.1 Cómo es una skill

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

#### Invocar una skill

Escribe `/` y el nombre en el chat, seguido de los argumentos:

```text
/enrich-us 40399
/wbs-execution 40399 from:T-03
/qa-review 40933 base:9e07c66d head:99e5da20
```

También puedes pedirlo con palabras («ejecuta enrich-us para el 40399»): la descripción de la
skill hace que la herramienta la elija. El comando con `/` es más fiable.

> [!NOTE]
> **Copilot y $ARGUMENTS**
>
> Claude Code sustituye `$ARGUMENTS` en el `SKILL.md` por lo que escribes tras el nombre. Copilot no
> lo hace: cada skill lo detecta («*if the Arguments line still shows a placeholder…*») y toma el ID
> de tu mensaje. Por eso en Copilot conviene escribir el ID en la misma línea: `/enrich-us 40399`.

#### Lo que todas las skills tienen en común

- **Confirman antes de escribir.** Te muestran un bloque de resumen y esperan un «sí» o tus
  correcciones. Sin respuesta, no escriben nada.
- **Se paran con ⛔** cuando falta algo imprescindible (la carpeta, el documento del paso anterior,
  la rama) y te dicen qué ejecutar.
- **Registran en `bitacora.md`** una línea por pregunta, respuesta, decisión o hallazgo.
- **Terminan con un informe** fijo, el siguiente paso y, si cambió algo del work item, un bloque
  *Comentario para Azure DevOps* listo para pegar.
- **Nunca hacen commit**: te dan el `git add` con rutas exactas.

### 6.2 enrich-us · del work item al requisito técnico

| Ficha | |
| --- | --- |
| **Paso** | 1 · compuerta G1 |
| **Quién** | Dev que toma el work item; QA con el modo `qa` |
| **Comando** | `/enrich-us <id>` · `/enrich-us <id> qa` · legado: `sprint:<s> item:<i>` |
| **Lee** | `story.md`, todo `assets/`, el código (con `code-explorer`), `AGENTS.md` |
| **Escribe** | `pbi.md` o `bug.md`, `bitacora.md` |
| **Modelo** | Uno de razonamiento (Opus) |
| **Rol de la IA** | *Technical Product Owner* y arquitecto |

#### Para qué sirve

Convierte el work item que copiaste de Azure DevOps en un documento técnico completo
(`pbi.md` o `bug.md`) con el que un desarrollador puede implementar **sin volver al work item**:
criterios de aceptación, campos y entidades afectados, endpoints, archivos a modificar, reglas de
negocio, textos e idiomas, pruebas necesarias y Definición de Hecho. Cada dato dice de dónde sale
(columna *Origen*): `story.md`, `Inferido del código`, `Confirmado por <persona> (<fecha>)` o
`[PENDING-BUSINESS]`.

#### Antes de lanzarla

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

#### Qué hace, paso a paso

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

#### Ejemplo

**Lo que pides:**

```text
/enrich-us 40399
```

**Confirmación que te muestra (G1):**

```text
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
```

**Tu respuesta:**

```text
La ven Comercial y Jefe de ventas; lo confirmó Laura (PO) hoy. El resto, correcto.
```

**Informe final:**

```text
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
```

#### Qué deja

`pbi.md` (secciones: descripción funcional, criterios `CA-XX`, campos y entidades, endpoints,
archivos, reglas `BR-XX`, clasificación de QA, textos e idiomas, requisitos no funcionales, pruebas,
Definición de Hecho, notas, campos pendientes) o `bug.md` (descripción, pasos de reproducción,
esperado frente a actual, causa raíz inferida, archivos, criterios de corrección, clasificación de
QA, textos, pruebas, impacto, DoD, notas, pendientes).

#### Paradas y cómo resolverlas

| Mensaje | Causa | Qué haces |
| --- | --- | --- |
| *No hay story.md para el work item…* | No existe la carpeta o `story.md` | `new-sdd-item.py` y copia el work item; o deja que la IA cree la carpeta |
| Un adjunto enlazado no existe | Falta el archivo en `assets/` | Guárdalo con el nombre del enlace y vuelve a lanzar |
| *⚠️ Not enough information…* | 3 o más campos críticos sin definir | Pide las respuestas al PO o corrige el work item y vuelve a copiarlo |
| *pbi.md already exists* | Ya se ejecutó antes | A) sobrescribir (git guarda la versión anterior) o B) cancelar |

> [!TIP]
> **Consejos**
>
> - Si el PO responde fuera del chat, pega la respuesta y di quién la dio: la IA la registra con su
>   nombre y fecha.
> - Los textos visibles sin redacción en `story.md` salen como `Propuesto — validar con PO`: no
>   bloquean, pero el PO debe verlos.
> - Un criterio que no está en el work item pero se deduce de un mockup sale como `Propuesto desde la
>   descripción — validar con PO`.

### 6.3 technical-analysis · el diseño

| Ficha | |
| --- | --- |
| **Paso** | 2 · compuerta G2 (aprobar 03 y 04) |
| **Quién** | Dev |
| **Comando** | `/technical-analysis <id>` |
| **Lee** | `pbi.md`/`bug.md`, el código (con `code-explorer`) |
| **Escribe** | `00`–`06`, `bitacora.md` |
| **Modelo** | Uno de razonamiento (Opus) |
| **Rol de la IA** | Arquitecto y *tech lead* |

#### Para qué sirve

Produce los siete documentos de diseño que `wbs-execution` implementará tarea por tarea. Separa con
cuidado lo que **afirma del código** (estado actual, deuda, patrones, cobertura), lo que **propone
con justificación** (puntos de historia, patrones, alternativas) y lo que **no puede afirmar** sin
evidencia (reglas de negocio, sistemas externos, impacto en usuarios), que marca
`[REQUIRES-VALIDATION]`.

#### Los siete archivos

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

#### Ejemplo

**Lo que pides:**

```text
/technical-analysis 40399
```

**Confirmación:**

```text
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
```

Tras tu «sí» genera los archivos en orden, con una línea de progreso por archivo
(`✓ 01-current-state-report.md`…), y termina con la tabla de estado, los marcadores abiertos y el
total de SP y tareas.

#### Tu compuerta G2

Lee **`03` y `04` enteros** antes de aprobar. Son contrato: una vez aprobados, solo cambian con tu
aprobación explícita, una nueva versión y quién la aprobó. Comprueba sobre todo:

- que cada criterio `CA-XX` tiene su `SPEC-XX` y que las SPECs son verificables;
- que los contratos (firmas, DTO, rutas) son los que quieres;
- que la WBS no tiene tareas mezcladas de capas ni una tarea de pruebas al final;
- los `[REQUIRES-VALIDATION]` y `[ASSUMPTION-BASED]` del resumen ejecutivo.

Para aprobar, pide que actualice la línea *Estado* de 03 y 04: «Aprueba 03 y 04, aprobado por Ana
Pérez hoy».

#### Paradas frecuentes

| Mensaje | Causa | Qué haces |
| --- | --- | --- |
| *⛔ pbi.md or bug.md not found* | No se hizo el paso 1 | `/enrich-us <id>` |
| *⚠️ The input document has unresolved fields* | `pbi.md` tiene `[PENDING-BUSINESS]` | A) resolverlos antes (recomendado) o B) seguir: las secciones afectadas salen `[ASSUMPTION-BASED]` |
| *⚠️ Analysis files already exist* | Ya se generó | A) sobrescribir o B) cancelar |
| Pides añadir trabajo fuera del work item | Deuda, otro bug, un refactor | Te dice lo que añade y pregunta: ¿entra aquí (con aprobación del PO) o va a `_borradores/`? |

### 6.4 wbs-execution · implementar

| Ficha | |
| --- | --- |
| **Paso** | 3 |
| **Quién** | Dev |
| **Comando** | `/wbs-execution <id>` · `from:T-03` · `qa` · en Copilot: `/wbs-execution-sonnet` |
| **Lee** | `00`–`06`, la configuración del proyecto (comandos) |
| **Escribe** | Código y pruebas (por medio de los subagentes), `05` (estado), `CHANGELOG.md`, `bitacora.md`, `commit-message.md` |
| **Subagentes** | `backend-dev`, `frontend-dev`, `migration-reviewer`, `code-explorer` |
| **Modelo** | Sonnet (fijado en Claude Code) |

#### Para qué sirve

Ejecuta la WBS aprobada **tarea por tarea**, con pruebas primero y verificación real después de
cada tarea. No rediseña: si el diseño no se puede implementar tal cual, se para y te propone el
ajuste mínimo.

#### Qué hace, paso a paso

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

> [!WARNING]
> **El informe del subagente no es evidencia**
>
> La sesión vuelve a ejecutar build y pruebas aunque el subagente diga que están en verde. Si una
> tarea con pruebas nuevas no trae línea *Rojo*, lo registra como desviación y comprueba que las
> pruebas de caracterización afirman el comportamiento que ya existía en `HEAD`.

#### Bucles y sus límites

| Bucle | Límite | Después |
| --- | --- | --- |
| El subagente corrige su propia comprobación que falla | 3 intentos | Devuelve un bloqueo |
| La verificación de la sesión falla → vuelve al subagente | 2 rondas | Bloqueo para ti |
| El subagente se para sin informe | 1 reanudación | Decides: la sesión termina la tarea o se divide |
| Hallazgos de QA devueltos a implementación (`qa`) | 2 rondas de QA | Decides cada hallazgo abierto |
| Hace falta cambiar el diseño ya empezado | — | Primero se actualizan 03/04 con tu aprobación |

Pasado un límite, **decides tú**; la IA nunca sigue reintentando por su cuenta.

#### Ejemplo

**Lo que pides:**

```text
/wbs-execution 40399
```

**Confirmación de inicio:**

```text
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
```

**Progreso tras cada tarea:**

```text
✅ T-01 hecha: Permiso «ver ofertas» por rol — 40399
📋 Progreso: 1/2 tareas · 2/4 SP
🌐 Traducciones: N/A · pendientes: ninguna
⏭️ Siguiente: T-02 — Entrada «Ofertas» en el menú lateral. ¿Continúo?
```

**Cierre:**

```text
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
```

#### Modos y argumentos

| Forma | Qué hace |
| --- | --- |
| `/wbs-execution <id>` | Empieza o **reanuda**: lee la columna Estado de `05`, ejecuta build y pruebas antes de seguir y continúa por la primera tarea pendiente |
| `/wbs-execution <id> from:T-03` | Empieza en `T-03`, solo si sus dependencias están hechas |
| `/wbs-execution <id> qa` | Corrige los hallazgos de `qa-report.md` marcados `A corregir`, uno por uno como pequeñas tareas, y reescribe `commit-message.md` |

> [!TIP]
> **Bloques de 6 tareas**
>
> Con más de 6 tareas pendientes, trabaja en bloques de 6 y, en Claude Code, usa `/compact` entre
> bloques (o abre una sesión nueva: la reanudación lee el estado de `05`).

### 6.5 qa-review · la revisión independiente

| Ficha | |
| --- | --- |
| **Paso** | 4 · compuerta G3 |
| **Quién** | Dev o QA, **siempre en una sesión nueva** |
| **Comando** | `/qa-review <id> [base:<ref>] [head:<ref>]` |
| **Lee** | `pbi.md`, `04` (SPECs), estado de `05`, `06`, `CHANGELOG.md`, `fix-plan.md`, `test-cases.md`, el diff |
| **Escribe** | `qa-report.md`, `bitacora.md`, una viñeta en `commit-message.md`, borradores |
| **Subagentes** | `qa-reviewer` (obligatorio), `runtime-tester` (opcional) |
| **Modelo** | `qa-reviewer` en Opus; en Copilot, elige uno de razonamiento |

#### Para qué sirve

Una revisión **adversarial** del cambio ya implementado contra su diseño aprobado, las reglas de
`AGENTS.md`, la seguridad y las regresiones. `qa-reviewer` intenta romperlo; `runtime-tester`
(opcional) lo prueba con la aplicación arrancada; la sesión **verifica cada hallazgo** antes de
escribirlo. Nunca corrige código: las correcciones van a `/wbs-execution <id> qa`.

#### Alcance: base y head

| Argumento | Por defecto | Cuándo indicarlo |
| --- | --- | --- |
| `base:<ref>` | `git merge-base HEAD origin/dev` | Si la rama tiene commits ajenos (por ejemplo, la rama del piloto con el kit) |
| `head:<ref>` | El árbol de trabajo (commits + cambios sin commit + nuevos) | Para revisar un commit concreto. Si no coincide con el árbol, el revisor lee con `git show` y no ejecuta pruebas |

Los archivos del cambio que no son del work item (por ejemplo, archivos del kit) se dejan fuera y el
informe lo dice. La carpeta `docs/sdd/` se lista pero no se revisa como código.

#### Severidad

| Severidad | Cuándo | Efecto |
| --- | --- | --- |
| **Alta** | Rompe una SPEC o un criterio; seguridad (autorización, exposición de datos, inyección, secretos); pérdida de datos; regresión en otro rol o flujo | Bloquea el PR |
| **Media** | Defecto con alternativa; SPEC sin prueba negativa; traducción que falta; contrato distinto de 03/04 | Se corrige antes del PR, salvo que aceptes el riesgo |
| **Baja** | Mantenibilidad, nombres, un comentario, un hueco menor de pruebas | No bloquea |

#### Ejemplo

**Sesión nueva:**

```text
/qa-review 40399
```

**Confirmación:**

```text
## Revisión de QA — 40399 Sección de ofertas en el menú lateral
Alcance: 3f1c2a0..árbol de trabajo · 4 archivos de código (2 nuevos) · docs/sdd/ no se revisa como código
Ronda: 1
Revisor: qa-reviewer (subagente)
Pruebas: dotnet test MiProyecto.Tests · cd ClientApp; yarn test
Runtime: runtime-tester propuesto — cambia una pantalla y AGENTS.md tiene los comandos de arranque
¿Empiezo?
```

**Informe y decisión (G3):**

```text
## 🔎 Revisión de QA — 40399 · ronda 1
Resultado: 0 altos · 1 medio · 1 bajo

QA-01 · Media · ClientApp/src/layout/SideMenu.tsx:88 — el rol «Jefe de ventas» no ve «Ofertas»
       (CA-02): la comprobación usa === 'Comercial'. Confirmado con: yarn test (prueba añadida).
QA-02 · Baja · Api/Authorization/Permissions.cs:41 — nombre de constante poco claro.

Para QA-01: A) corregir · B) aceptar el riesgo · C) work item aparte
```

**Tu decisión:**

```text
QA-01 A, QA-02 aceptado por Ana Pérez.
```

Después: `/wbs-execution 40399 qa` (en la sesión de implementación o en otra nueva, **nunca** en la de
QA) y `/qa-review 40399` en otra sesión nueva para la **ronda 2**, que revisa solo las correcciones.
No hay ronda 3: lo que quede abierto lo decides tú.

#### Estados de un hallazgo

`Abierto` → `A corregir` → `Corregido (<fecha>)` (lo pone `wbs-execution`) → `Corregido (verificado
<fecha>)` (lo pone la ronda 2). Otros: `Aceptado (riesgo asumido por <persona>, <fecha>)`,
`Descartado (<motivo>)` (la fila no se borra) y `Borrador (_borradores/<slug>.md)`, que pasa a
`Work item #<id>` cuando se crea en Azure DevOps (el borrador se borra antes del PR).

### 6.6 document-code · documentar lo que cambió

| Ficha | |
| --- | --- |
| **Paso** | 5 |
| **Quién** | Dev, después de `qa-review` y antes del commit o el PR |
| **Comando** | `/document-code <id> [base:<ref>]` |
| **Lee** | `pbi.md`, `03`, `04` §4.4, `06`, `CHANGELOG.md` (o `fix-plan.md`) |
| **Escribe** | Comentarios de documentación, `docs/`, `CHANGELOG.md`, una viñeta en `commit-message.md` |
| **Subagentes** | `doc-writer`, `code-explorer` (si hay más de 5 archivos) |
| **Script** | `comment_only.py` (prueba que solo cambiaron comentarios) |

#### Para qué sirve

Documenta **solo lo que el work item tocó**: comentarios `///` (C#) o TSDoc en tipos y miembros
nuevos o cambiados, comentarios de *por qué* donde una decisión no es obvia, y las secciones de
`docs/` afectadas. Nunca cambia comportamiento, y lo demuestra con un script.

#### Qué se documenta y dónde

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

#### Cómo garantiza que solo cambian comentarios

1. Antes de delegar: `comment_only.py save <temp>/sdd-doc-<id> <archivos>` guarda una copia.
2. `doc-writer` escribe.
3. `comment_only.py check …` compara línea a línea: toda línea añadida, quitada o cambiada debe
   ser un comentario o estar en blanco, y la codificación (BOM) y los finales de línea deben ser
   los mismos. Si no, vuelve a `doc-writer` (máximo 2 rondas) o se restaura el archivo.
4. Build sin avisos nuevos (en C#, un XML mal formado da CS1570–CS1587) y lint/tipos en frontend.
5. Lee el diff de `docs/`: cada afirmación debe salir de `pbi.md`, `03`, `04` o el código.

**Lo que dice el script:**

```text
✓ Api/Controllers/OffersController.cs: solo comentarios (6 línea(s) de comentario)
✓ ClientApp/src/layout/SideMenu.tsx: solo comentarios (4 línea(s) de comentario)

Solo cambiaron comentarios
```

**Informe final:**

```text
## 📝 Documentación — 40399
Cambios: 5 comentarios de documentación (3 nuevos, 2 actualizados) · 1 de porqué · docs/: frontend.md · ADR: ninguno
Validación: comment_only → solo comentarios · build → sin avisos nuevos · lint/tipos → OK
Pendiente: ninguno
Siguiente: el commit con el work item
git add ClientApp/src/layout/SideMenu.tsx Api/Authorization/Permissions.cs docs/frontend.md docs/sdd/40399-…/
```

> [!NOTE]
> **Si el work item ya está mezclado**
>
> La documentación va en un commit de seguimiento con su propio mensaje completo:
> `docs(<ámbito>): documentar <qué>` · `Ref: #<id>`.

---

## 7. Vía rápida y QA

Dos caminos complementan el flujo principal. La vía rápida (`quick-fix`) lleva un bug pequeño de
`story.md` a una corrección probada en una sola sesión, con una página de diseño en lugar de siete.
El camino de QA (`enrich-us … qa` y `test-cases`) convierte los criterios de aceptación en casos de
prueba con datos reales y un CSV para Azure Test Plans.

### 7.1 quick-fix · la vía rápida para bugs pequeños

| Ficha | |
| --- | --- |
| **Sustituye** | Los pasos 1, 2 y 3. Los pasos 4 (QA), 5 (documentación) y 6 (PR) no cambian |
| **Quién** | Dev, en una rama `fix/<id>-<título>` |
| **Comando** | `/quick-fix <id>` |
| **Lee** | `story.md` y `assets/`, *Project context*, el código |
| **Escribe** | `bug.md`, `fix-plan.md`, código y prueba, `CHANGELOG.md`, `commit-message.md`, `bitacora.md` |
| **Subagentes** | `code-explorer` (causa), `backend-dev` o `frontend-dev` (corrección) |
| **Modelo** | Sonnet (fijado en Claude Code) |

#### La compuerta: 8 criterios

El mismo rigor que el flujo completo (evidencia en el código, pruebas primero, verificación real),
pero solo para bugs cuya causa y corrección caben en pocos archivos. **Un solo ✗ saca el bug de la
vía rápida** (ADR-0024).

| Criterio | Se cumple cuando |
| --- | --- |
| **Causa** | Se ve en el código con `archivo:línea`. Una afirmación, no una hipótesis |
| **Tamaño** | Como máximo 3 archivos de producción, de una sola capa (backend o frontend); las pruebas aparte |
| **Datos** | Sin migración ni cambio de una entidad o su configuración |
| **Contratos** | Sin cambios de rutas, forma de peticiones o respuestas, DTO que usen otros sistemas, eventos ni horarios de jobs |
| **Seguridad** | Sin cambios de autorización, roles, tenants ni autenticación |
| **Negocio** | Sin `[PENDING-BUSINESS]`: el comportamiento esperado sale de `story.md` o es obvio por el defecto |
| **Textos** | Ningún texto visible nuevo, o todos con su traducción en todos los idiomas |
| **Dependencias** | Ningún paquete nuevo ni actualizado |

#### Qué hace, paso a paso

1. **Precondiciones:** no estás en `dev` ni `main`; no hay cambios sin commit fuera de la carpeta;
   lee comandos, línea base, rutas protegidas y reglas de traducción de *Project context*. Si la
   carpeta ya tiene `03`–`05`, está en el flujo completo: te manda a `/wbs-execution`.
2. **Lee el work item**: qué falla, cómo reproducirlo, qué se esperaba, dónde se vio.
3. **Busca la causa** con una pregunta precisa a `code-explorer` y abre solo las líneas que la
   prueban.
4. **Aplica la compuerta.** Con un ✗, se para **sin escribir `bug.md` ni código** y deja lo
   encontrado en `bitacora.md` para que el flujo completo empiece desde ahí.
5. **Confirmación** en un solo bloque: causa, cambio, prueba que fallará primero, regresión.
6. **Escribe el diseño**: `bug.md` (sello `quick-fix`) y `fix-plan.md` con la compuerta y su
   evidencia, la causa, el cambio, las pruebas con el *Rojo* esperado, los riesgos y la tarea
   `T-01` aprobada.
7. **Implementa `T-01`** con el subagente de la capa: prueba → *Rojo* → corrección → verde. Una
   prueba que pasa antes de la corrección no demuestra el bug: vuelve al subagente.
8. **Verifica** build, la suite de la capa, lint y tipos, el alcance (`git status`) y cada criterio
   de `bug.md`.
9. **Cierra**: `T-01` hecha, `CHANGELOG.md`, `commit-message.md` (`fix(<ámbito>): …`,
   `BUG-<id> — …`, **Causa**, `Ref: #<id>`) y el `git add`.

#### Ejemplo: un bug que pasa

**Lo que pides:**

```text
/quick-fix 41020
```

**Confirmación:**

```text
## Corrección rápida — 41020 El total de la factura redondea mal los céntimos
Causa: el total se redondea por línea antes de sumar · Api/Services/InvoiceService.cs:212
Cambio: Api/Services/InvoiceService.cs → redondear una vez el total (1 archivo, backend)
Prueba primero: CalculateTotal_TresLineasConMedioCentimo_RedondeaUnaVez en
                MiProyecto.Tests/Services/InvoiceServiceTests.cs — hoy falla: devuelve 10,02 y no 10,01
Regresión: InvoiceServiceTests (14 pruebas) deben seguir en verde
Compuerta: ✓ todos · Riesgos: ninguno
Implementa: backend-dev (subagente)
¿Empiezo?
```

**Cierre:**

```text
## 🩹 Corrección rápida — 41020 El total de la factura redondea mal los céntimos
Causa: Api/Services/InvoiceService.cs:212 · Cambio: InvoiceService.cs · Pruebas: 1 nueva (Rojo → verde) + 14 en la suite
Verificado: build sin avisos nuevos · pruebas 312/312 · lint N/A
Siguiente: /qa-review 41020 en una sesión nueva (lee fix-plan.md como diseño) · después /document-code 41020
git add Api/Services/InvoiceService.cs MiProyecto.Tests/Services/InvoiceServiceTests.cs docs/sdd/41020-el-total-de-la-factura-redondea-mal-los/
```

#### Ejemplo: un bug que no pasa

**Lo que responde:**

```text
⛔ No es una corrección rápida — 41077: Datos · la causa está en la configuración de la entidad
   Invoice (Api/Data/Configurations/InvoiceConfiguration.cs:31: precisión decimal(18,2)) y
   corregirla exige una migración.
Siguiente: /enrich-us 41077 (flujo completo). Lo encontrado está en bitacora.md.
```

> [!TIP]
> **No fuerces la compuerta**
>
> Que un bug no pase no es un fallo: es la vía rápida haciendo su trabajo. La causa ya encontrada
> queda en la bitácora y `enrich-us` la aprovecha.

### 7.2 enrich-us en modo qa · clasificar los criterios

El modo QA es `enrich-us` con un paso más (ADR-0025): **cada criterio de aceptación se clasifica**
según lo seguro que es, con su fuente. Lo usa QA cuando prepara el work item o antes de
`/test-cases`.

**Lo que pides:**

```text
/enrich-us 40933 qa
```

| Clasificación | Cuándo | Qué necesita |
| --- | --- | --- |
| **Definido** | `story.md` lo dice: la acción, los datos y el resultado esperado | La cita |
| **Deducción directa** | Se sigue sin elección posible de `story.md`, un adjunto o el código actual (una validación que ya existe, un patrón de la misma pantalla) | La fuente: `story.md` §, `assets/…` o `archivo:línea` |
| **A confirmar** | Todo lo demás: un límite, un mensaje, un rol, un caso que `story.md` no decide | Una pregunta concreta para el PO; además es un `[PENDING-BUSINESS]` |

Un criterio nunca pasa a *Definido* porque «suene razonable». La clasificación va en la sección
*Clasificación de QA* (`<!-- sdd:qa-classification -->`) de `pbi.md`/`bug.md`, y la confirmación
muestra el recuento: `Clasificación QA: 3 Definido · 1 Deducción directa · 2 A confirmar`.

**Sección «Clasificación de QA» resultante en pbi.md:**

| Criterio | Clasificación | Fuente | Pregunta para el PO |
| --- | --- | --- | --- |
| CA-01 | Definido | story.md §Criterios: «El delegado ve solo sus clientes» | — |
| CA-02 | Deducción directa | Api/Services/ClientService.cs:88 (filtro por delegación) | — |
| CA-03 | A confirmar | — | ¿Qué ve el delegado si no tiene clientes asignados? |

### 7.3 test-cases · casos de prueba y CSV

| Ficha | |
| --- | --- |
| **Paso** | QA, después de `enrich-us` (idealmente en modo `qa`); puede ir en paralelo a la implementación |
| **Quién** | QA |
| **Comando** | `/test-cases <id>` |
| **Lee** | `pbi.md`/`bug.md` (criterios, clasificación, roles, campos, i18n), SPECs de `04` si existe, `fix-plan.md` |
| **Escribe** | `test-cases.md`, `test-cases.csv`, `bitacora.md`, los `[PENDING-BUSINESS]` de `pbi.md` |
| **Script** | `test_cases_csv.py` |
| **Modelo** | Sonnet (fijado en Claude Code) |

#### Tipos de caso

| Tipo | Qué prueba |
| --- | --- |
| **Funcional** | El criterio tal como está escrito, con sus datos |
| **Negativo** | Cada validación y cada error que nombran el criterio o las reglas (vacío, fuera de rango, formato, no permitido), con el mensaje o código esperado |
| **Borde** | Los límites que da el work item (fechas, importes, longitudes, cantidades), a cada lado |
| **Permisos** | Un caso por rol que puede y otro por rol que no, cuando el work item nombra roles |
| **Idioma** | Un caso por idioma del proyecto, cuando el criterio muestra textos |
| **Regresión** | (bugs) Los pasos reportados con el resultado esperado, y el comportamiento vecino que no debe romperse |

Reglas que la skill no se salta:

- Los datos y los resultados esperados salen de `pbi.md`/`bug.md`. Un valor que no dan → el caso
  lleva `[PENDING-BUSINESS: <pregunta>]` y queda **Bloqueado**. Nunca inventa límites, mensajes ni
  catálogos.
- Un criterio *A confirmar* deja **todos sus casos Bloqueados** hasta que se confirme.
- Un caso prueba una sola cosa; los pasos son acciones de una persona con un resultado observable.
- Dice si es automatizable y a qué nivel (unitaria, integración, e2e), o por qué no. Con `04`,
  marca qué casos ya cubre una SPEC automatizada.

#### Ejemplo

**Lo que pides:**

```text
/test-cases 40399
```

**Confirmación:**

```text
## Casos de prueba — 40399 Sección de ofertas en el menú lateral
Criterios: 2 (1 Definido · 0 Deducción directa · 1 A confirmar · 0 sin clasificar)
Casos: 3 · Funcional 2 · Negativo 0 · Borde 0 · Permisos 1 · Idioma 0 · Regresión 0
Bloqueados: 1 — TC-03: ¿orden ascendente o descendente? · Ya automatizados (SPECs): 1
¿Empiezo?
```

**test-cases.md (un caso):**

```text
### TC-02 · No ver la sección Ofertas como consultor

- **Criterio:** CA-01 · **Tipo:** Permisos · **Prioridad:** Alta · **Estado:** Diseñado
- **Rol:** Consultor · **Idioma:** es
- **Precondiciones:** usuario con rol Consultor
- **Datos:** —
- **Automatizable:** Sí (integración)

| # | Acción | Resultado esperado |
| --- | --- | --- |
| 1 | Iniciar sesión como consultor y abrir el menú lateral | No aparece «Ofertas» |
```

El CSV lo genera el script (salida real):

**Comando:**

```text
python .agents/skills/test-cases/scripts/test_cases_csv.py docs/sdd/40399-…/test-cases.md --area "MiProyecto\Comercial"
```

**Lo que responde:**

```text
✓ 2 casos y 3 pasos en docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/test-cases.csv
```

**test-cases.csv:**

```text
ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,State
,Test Case,TC-01 · Ver la sección Ofertas como comercial,,,,MiProyecto\Comercial,Design
,,,1,Iniciar sesión como comercial,Se muestra el panel principal,,
,,,2,Abrir el menú lateral,Aparece «Ofertas» debajo de «Clientes»,,
,Test Case,TC-02 · No ver la sección Ofertas como consultor,,,,MiProyecto\Comercial,Design
,,,1,Iniciar sesión como consultor y abrir el menú lateral,No aparece «Ofertas»,,
```

El caso bloqueado (TC-03) no está en el CSV. Para incluirlo, `--include-blocked`. El archivo va en
UTF-8 con BOM para que Excel y Azure DevOps lean bien las tildes. El CSV **no se versiona**
(ADR-0027): lo que va al repositorio es `test-cases.md`, y el script vuelve a generar el CSV cuando
haga falta.

#### Importarlo en Azure Test Plans

1. Revisa `test-cases.md` (QA es quien lo aprueba).
2. En Azure DevOps: **Test Plans → tu plan → suite → Test cases → Import** (o *Import test cases
   from CSV*), elige `test-cases.csv` y revisa la vista previa.
3. Si el PO responde una pregunta, vuelve a lanzar `/test-cases <id>`: actualiza el archivo
   conservando los IDs y los casos ya revisados, y desbloquea los que correspondan.

> [!NOTE]
> **Relación con qa-review**
>
> Si existe `test-cases.md`, `qa-review` comprueba que cada caso de **prioridad Alta** tiene una
> prueba automatizada o una comprobación en ejecución.

---

## 8. Skills de proyecto

Dos skills trabajan sobre el repositorio entero, no sobre un work item. `project-context` se ejecuta
una vez tras instalar el kit (y cuando cambia el stack): escribe lo que todas las demás skills dan
por cierto. `document-project` documenta todo el proyecto existente, por bloques, cuando el equipo
decide hacerlo.

### 8.1 project-context · el contexto del proyecto

| Ficha | |
| --- | --- |
| **Paso** | 0 · una vez por repositorio, y al cambiar el stack |
| **Quién** | Tech lead (o un dev que conozca el proyecto) |
| **Comando** | `/project-context` · `/project-context fresh` · `/project-context check` |
| **Lee** | Todo el repositorio (con `inventory.py` y `code-explorer`), README, `CLAUDE.md`, `docs/` existentes |
| **Ejecuta** | Build, todas las pruebas, lint y type check (verifica los comandos y registra la línea base) |
| **Escribe** | *Project context* de `AGENTS.md`, los seis `docs/*.md`, proyecto de pruebas, pruebas de arquitectura, `sdd-guardrails.json` |
| **Subagentes** | `code-explorer`, `backend-dev`, `doc-writer` |
| **Modelo** | Opus (fijado en Claude Code) |

#### Por qué importa tanto

Las demás skills **confían ciegamente** en *Project context*: si un comando está mal escrito aquí, se
repite mal en cada work item. Por eso todo lo que escribe sale de un archivo, de un comando que ha
ejecutado o de una respuesta tuya, y lo que no pudo verificar queda marcado `[REQUIRES-VALIDATION]`.

#### Modos

| Modo | Cuándo | Qué hace |
| --- | --- | --- |
| *new* (sin argumento, sin contexto previo) | Primera vez | Todo el proceso |
| *update* (sin argumento, con contexto) | El stack o los comandos cambiaron | Todo el proceso y te presenta una lista de cambios (añadir, corregir, mover a `docs/`, quitar), cada uno con su fuente. Nunca quita texto escrito por una persona sin aprobación |
| `fresh` | Quieres rehacerlo sin dejarte llevar por el actual | Ignora el contexto actual y compara al final |
| `check` | `check_project.py` da avisos o errores | Pasada corta: convierte cada aviso en una fila con su resolución, sin inventario ni build |

#### Qué hace, paso a paso

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

#### Los encabezados fijos de Project context

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

#### Ejemplo de cierre

**Lo que responde:**

```text
## 🧭 Contexto del proyecto — mi-proyecto
Modo: new · AGENTS.md: 178 líneas · docs/: creados architecture, backend, database, api-reference, frontend, reglas-negocio
Verificado: build OK (1 min 40 s, 15 avisos) · pruebas 298 OK, 2 fallaban antes · lint 0 errores · tipos 3 errores previos
Proyecto de pruebas: creado MiProyecto.Tests (4 pruebas) · CI: dotnet test añadido (aprobado)
Decisiones: yarn.lock es el válido; i18n/*.json se editan a mano; CLAUDE.md → @AGENTS.md
Pendiente: [REQUIRES-VALIDATION] usuario local de pruebas · _borradores/pruebas-frontend.md
Siguiente: /document-project (documentación completa) o el primer work item con /enrich-us
git add AGENTS.md CLAUDE.md docs/ MiProyecto.Tests/ MiProyecto.sln sdd-guardrails.json azure-pipelines.yml
```

#### El modo check

**Lo que pides:**

```text
/project-context check
```

Ejecuta `check_project.py` y te propone una tabla, por ejemplo:

| Aviso | Resolución | Quién |
| --- | --- | --- |
| Sección por encima de su presupuesto | Mover el detalle (nunca una regla) a `docs/` con enlace | La sesión |
| Sección vacía o encabezado que falta | Rellenarla con una búsqueda dirigida | La sesión |
| `[REQUIRES-VALIDATION]` | Decir qué falta y cómo verificarlo (un comando, una pantalla, una persona); al resolverlo, cambiar el marcador por el hecho | La sesión o una persona |
| Fuentes cambiadas después de la fecha del contexto | Releer solo esas fuentes y proponer el cambio | La sesión, con aprobación |
| `sdd-guardrails.json` sin rutas protegidas · sin pruebas de arquitectura | Proponer la configuración y las pruebas | La sesión, con aprobación |
| Sin proyecto de pruebas · `CLAUDE.md` con contenido propio | El modo completo | `/project-context` |

### 8.2 document-project · documentar todo el proyecto

| Ficha | |
| --- | --- |
| **Cuándo** | Una vez, después de `project-context`, en proyectos con código sin documentar |
| **Quién** | Tech lead o un dev; un bloque por sesión |
| **Comando** | `/document-project` · `plan` · `status` · `block:B-NN` · `area:A-NN` |
| **Lee** | El código del área, el historial git, ADR, `docs/`, `_borradores/` |
| **Escribe** | Comentarios de documentación, resúmenes de clases de prueba, `docs/`, `docs/sdd/_documentacion/` |
| **Subagentes** | `doc-writer`, `code-explorer` |
| **Scripts** | `doc_coverage.py`, `comment_only.py`, `check_project.py` |

#### Para qué sirve

Es `document-code` aplicado al código que ningún work item tocó: comentarios `///`/TSDoc en todo el
código público, un resumen en cada clase de pruebas y `docs/` completos (cada endpoint, entidad y
pantalla; solo reglas de negocio confirmadas). Como el proyecto es grande, trabaja **por áreas
agrupadas en bloques: un bloque por sesión, un commit y un PR por bloque**, con un plan reanudable.

#### Modos

| Forma | Qué hace |
| --- | --- |
| `/document-project` | Sin `plan.md`: crea el plan. Con plan: documenta el siguiente bloque no `Hecha` |
| `/document-project plan` | Rehace el plan: añade áreas nuevas, mantiene las `Hecha` |
| `/document-project block:B-03` | Documenta ese bloque |
| `/document-project area:A-12` | Documenta solo esa área |
| `/document-project status` | Solo informa: cobertura frente a la línea base, bloques hechos y pendientes, áreas en `Revisar`, hallazgos abiertos y archivos cambiados después de documentarse. No escribe; funciona en cualquier rama |

#### El plan

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

#### Un bloque

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

**Cierre de un bloque:**

```text
## 📝 Documentación — B-01 · Base, autorización y errores
Cambios: 64 comentarios (58 nuevos, 6 corregidos) · pruebas: 9 resúmenes · docs/: architecture.md, backend.md
Cobertura del bloque: 12 % → 97 % · proyecto: 18 % → 26 %
Validación: comment_only → solo comentarios · build → 0 avisos nuevos (226 = línea base) · lint/tipos → OK
Sin documentar: 2, ver B-01.md · Hallazgos: 3
Siguiente: commit y PR de este bloque · después /document-project en una sesión nueva (B-02: Datos)
git add <cada archivo cambiado, de git status> docs/sdd/_documentacion/
```

> [!WARNING]
> **Un bloque, un commit**
>
> Nunca empieces un bloque sobre otro sin commit: la skill se para si el árbol no está limpio (salvo
> el `plan.md` todavía sin commit, que entra con el primer bloque). La rama sugerida es
> `docs/document-project-b01`.

> [!NOTE]
> **Cuándo no hace falta**
>
> En un proyecto nuevo, o si el equipo prefiere documentar sobre la marcha, `document-code` mantiene
> la documentación al día work item a work item. `document-project` es para la deuda de
> documentación acumulada.

---

## 9. Subagentes

Un subagente es un asistente con un rol estrecho, permisos limitados y un modelo propio. La skill
de la sesión principal le pasa un paquete cerrado con todo lo que necesita, él hace un trabajo
acotado y devuelve un informe con un formato fijo. Tú normalmente no los invocas: los usan las
skills.

### 9.1 Por qué subagentes

*Esquema: la sesión principal decide y verifica; los subagentes hacen trabajo acotado con un paquete cerrado.*

```text
Sesión principal (la skill: decide, pregunta, verifica)
  ── paquete cerrado ──▶ code-explorer                 busca y mapea código
  ── paquete cerrado ──▶ backend-dev / frontend-dev    implementa una tarea
  ── paquete cerrado ──▶ qa-reviewer                   revisa e intenta romper
  ── paquete cerrado ──▶ doc-writer                    escribe comentarios y docs/
  ◀── informe (la sesión lo verifica: no es evidencia)
```

- **Contexto limpio.** La búsqueda en 40 archivos o la implementación de una tarea ocurre en el
  contexto del subagente; a la sesión principal solo llega el resumen. Las sesiones duran más y
  gastan menos.
- **El modelo adecuado.** Buscar es barato (Haiku); revisar exige razonamiento (Opus).
- **Independencia.** `qa-reviewer` recibe fuentes, no conclusiones: no hereda la opinión de quien
  implementó.
- **Permisos mínimos.** Quien busca no puede editar; quien revisa no puede tocar el código.

> [!WARNING]
> **Los subagentes no tienen memoria**
>
> Cada llamada empieza de cero: por eso el paquete lleva todo (tarea, SPECs literales, archivos con
> rangos de líneas, comandos exactos, reglas). Y su informe **no es evidencia**: la sesión principal
> vuelve a ejecutar las comprobaciones.

### 9.2 Formato y adaptadores

Cada subagente se define una vez en el kit (`core/agents/<nombre>.md`), en formato neutral, y el
instalador genera el de cada herramienta:

```yaml
---
name: backend-dev
description: Implements exactly one backend task of an approved WBS ... Use when wbs-execution
  delegates a task whose role is Backend; not for design, analysis or open-ended changes.
permissions: [read, edit, execute]   # read | edit | execute
model_tier: standard                 # fast | standard | reasoning
sdd_steps: [3]                       # pasos del flujo donde participa
skills: []
status: stable                       # solo se instalan los stable
---
Instrucciones (en inglés). El informe que devuelve, en español.
```

| Neutral | Claude Code (`.claude/agents/*.md`) | Copilot (`.github/agents/*.agent.md`) |
| --- | --- | --- |
| `read` | `Read, Grep, Glob` | `read`, `search` |
| `edit` | `Edit, Write` | `edit` |
| `execute` | `Bash` | `execute` |
| `model_tier` | `haiku` / `sonnet` / `opus` | El modelo de la conversación |

En Claude Code los ves con `/agents`; en VS Code, en el selector de agentes. En Copilot se marcan
`user-invocable: false`: los usan las skills con `runSubagent`.

### 9.3 Resumen de los siete

| Subagente | Hace | Permisos | Modelo | Lo usan |
| --- | --- | --- | --- | --- |
| `code-explorer` | Busca y mapea código para responder una pregunta | Lectura | fast (Haiku) | Casi todas las skills |
| `backend-dev` | Implementa **una** tarea de backend, pruebas primero | Lectura, edición, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix`, `project-context` |
| `frontend-dev` | Implementa **una** tarea de frontend, con traducciones | Lectura, edición, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix` |
| `qa-reviewer` | Revisa el cambio e intenta romperlo | Lectura, ejecución | reasoning (Opus) | `qa-review` |
| `runtime-tester` | Arranca la aplicación en local y comprueba pantallas o endpoints | Lectura, ejecución | standard (Sonnet) | `qa-review` (opcional) |
| `doc-writer` | Escribe comentarios y `docs/` desde un paquete de hechos | Lectura, edición | fast (Haiku) | `document-code`, `document-project`, `project-context` |
| `migration-reviewer` | Revisa migraciones de EF Core antes de cerrar una tarea | Lectura, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix`, `qa-review` |

### 9.4 code-explorer

**Rol:** búsqueda de solo lectura. Responde **una** pregunta precisa (un flujo, una entidad, un
patrón, dónde se decide algo) para que la sesión principal lea la respuesta y no el repositorio.

**Cómo trabaja:** busca primero por nombre y por texto; abre un archivo solo cuando la búsqueda
muestra que responde; en archivos de más de unas 300 líneas, solo los rangos; **como máximo 15
archivos**. Nunca lee `bin/`, `obj/`, `node_modules/`, lockfiles ni código generado. Nunca abre
`.env*`; los `appsettings*.json`, solo por los nombres de sección. Si encuentra un secreto literal,
lo reporta como `ruta:línea — literal sensible` sin copiar el valor. Busca siempre las pruebas que
cubren lo que reporta. Lo que infiere sin verlo va marcado *(no verificado)*.

**Informe (máximo 60 líneas):**

```text
**Respuesta:** el menú lateral se construye en SideMenu.tsx a partir de una lista fija; la visibilidad
por rol la decide hasPermission() de core/permissions.ts.
**Archivos:**
- ClientApp/src/layout/SideMenu.tsx:40-96 — construye las entradas del menú
- ClientApp/src/core/permissions.ts:12-35 — hasPermission(rol, permiso)
- Api/Authorization/Permissions.cs:8-60 — catálogo de permisos del backend
**Patrones a reutilizar:** entrada de menú con permiso → «Clientes» en SideMenu.tsx:52
**Pruebas existentes:** ClientApp/src/layout/SideMenu.test.tsx · MiProyecto.Tests/Authorization/PermissionsTests.cs
**No cubierto / dudas:** cómo llegan los roles al cliente (no verificado: parece venir del token)
```

> [!TIP]
> **Tú también puedes usarlo**
>
> En Claude Code puedes pedir directamente «usa code-explorer para encontrar dónde se calcula el
> total de una factura y qué pruebas lo cubren». Mantiene limpia tu sesión.

### 9.5 backend-dev

**Rol:** implementa **exactamente una** tarea de backend de una WBS aprobada (.NET, EF Core,
servicios, controllers, jobs, autorización). No diseña.

**Paquete que recibe:** ID, título y descripción de la tarea · sus SPECs, literales · los contratos
que debe respetar · los archivos con rangos de líneas · los comandos exactos de build, test y lint ·
las convenciones de `AGENTS.md` · los riesgos.

**Cómo trabaja:**

1. **Pruebas primero, antes de tocar producción.** Escribe las pruebas de las SPECs y las ejecuta:
   deben fallar por el motivo esperado. Guarda esa línea como *Rojo*. Las pruebas de
   caracterización (fijan el comportamiento actual) deben pasar con el código de hoy.
2. Si la tarea **solo añade pruebas** de algo que ya existe, demuestra que pueden fallar con una
   **mutación temporal** del código (invertir una condición), las ejecuta, revierte y comprueba que
   el diff de producción queda vacío: *Rojo (mutación)*.
3. Implementa el cambio mínimo siguiendo los patrones del proyecto. Comentarios en español con
   `#<id>` cuando el cambio no es obvio.
4. Verifica con los comandos del paquete. **Hasta 3 intentos** con la misma comprobación; al
   tercero, devuelve un bloqueo.

**Límites:** solo los archivos del paquete y sus pruebas (otro estrictamente necesario, en *Fuera
del paquete*). Nunca `docs/sdd/`, rutas protegidas, migraciones ni contratos públicos salvo que el
paquete lo diga. Nunca commit, cambios de rama ni versiones de paquetes. Nunca secretos.

**Se para y pregunta** ante una regla o valor que el paquete no define, un diseño no
implementable, pruebas que ya fallaban, o si hace falta una migración, un cambio de contrato o un
archivo de otra capa.

**Informe (máximo 80 líneas):**

```text
**Estado:** ✅ Hecha
**Cambios:** Permissions.cs — nuevo permiso ViewOffers para Comercial y JefeVentas
**Archivos:** Api/Authorization/Permissions.cs · MiProyecto.Tests/Authorization/PermissionsTests.cs (nuevo) · Fuera del paquete: ninguno
**Pruebas:** 3 escritas · Rojo: dotnet test --filter PermissionsTests → 3 fallidas (ViewOffers no existe) · Verde: 3 pasan
**Validación:** dotnet build → 0 errores, 15 avisos (línea base 15) · dotnet test → 301/301
**Hallazgos:** Api/Authorization/Permissions.cs:77 — permiso Legacy sin uso
```

### 9.6 frontend-dev

**Rol:** implementa **exactamente una** tarea de frontend (React, TypeScript, componentes,
formularios, **traducciones en todos los idiomas**). Igual que `backend-dev`, con estas diferencias:

- Pruebas primero **cuando el proyecto puede probarlo** con sus herramientas. Si no (por ejemplo,
  no hay librería de pruebas de componentes), lo dice y escribe los pasos de comprobación manual.
- **Textos visibles** por el sistema de traducción, en todos los idiomas del paquete, en la misma
  tarea. Reutiliza claves; ante una casi igual (mayúsculas, espacios) pregunta. Nunca inventa una
  traducción: la deja fuera y reporta `[PENDING-TRANSLATION: <clave> → <idioma>]`. Mantiene orden,
  sangría y codificación de los archivos.
- Verifica con lint, pruebas, type check y build si se pide.
- Nunca toca submódulos compartidos ni rutas protegidas (por ejemplo `core-ui`) ni añade
  dependencias. Se para si la tarea necesita un cambio de backend.
- Su informe añade **Traducciones:** claves añadidas por idioma y pendientes.

### 9.7 qa-reviewer

**Rol:** revisión independiente y adversarial de un work item implementado. **Nunca edita** nada:
devuelve hallazgos a `qa-review`, que los verifica.

**Recibe fuentes, no conclusiones:** el ID y la carpeta, los archivos a leer, `base`/`head` y el
comando para ver cada diff, los archivos con su tamaño, `AGENTS.md`, los comandos de prueba y si
puede ejecutarlos; en la ronda 2, los hallazgos a revisar y el diff de la corrección.

**Qué busca, en cada cambio:**

- **SPECs y criterios:** implementados de verdad, con sus bordes (vacío, nulo, otros roles,
  límites, primer y último elemento).
- **Contratos** de 03/04 y el contrato de errores de `AGENTS.md`.
- **Seguridad:** autorización y aislamiento de tenant en cada endpoint o rama nueva, validación de
  entrada, secretos, datos personales en logs.
- **Regresiones:** quién llama a cada método cambiado, otros roles o flujos que comparten código,
  firmas de jobs o datos serializados.
- **Pruebas:** cada SPEC con prueba o comprobación manual documentada; casos negativos; pruebas que
  fallarían sin el cambio.
- **Traducciones**, **reglas del proyecto y rutas protegidas**, y las mitigaciones de `06`.

Puede ejecutar las pruebas; nunca arranca la aplicación, instala paquetes ni ejecuta git que
cambie estado (solo `diff`, `show`, `log`, `grep`, `blame`).

**Reglas:** cada hallazgo tiene `ruta:línea`, qué está mal, la SPEC o regla que incumple, un
**escenario concreto** (entrada o estado → resultado incorrecto) y cómo lo confirmó. Si no puede
escribir el escenario, no es un hallazgo (como mucho 3 *Dudas*). Nada de formato ni estilo.

**Informe (extracto):**

```text
**Resultado:** 0 altos · 1 medio · 1 bajo
QA-01 · Media · ClientApp/src/layout/SideMenu.tsx:88
**Qué:** el rol JefeVentas no ve «Ofertas».
**Por qué:** SPEC-02 (CA-02: la ven Comercial y Jefe de ventas).
**Escenario:** usuario con rol JefeVentas abre el menú → no aparece la entrada.
**Confirmado con:** yarn test SideMenu → 1 fallida (prueba añadida en una copia temporal)
**Cobertura de SPECs:** SPEC-01 → PermissionsTests · SPEC-02 → SideMenu.test.tsx (sin caso JefeVentas)
**Pruebas ejecutadas:** dotnet test → 301/301 · yarn test → 48/48
**Dudas:** ninguna
```

### 9.8 runtime-tester

**Rol:** arranca la aplicación en local con los comandos documentados, comprueba las pantallas o
endpoints que cambiaron y **para lo que arrancó**. Nunca edita código, configuración, secretos ni
datos.

1. **Requisitos:** lee en `AGENTS.md` qué necesita (servicios, base de datos, usuario y roles
   locales). Si falta algo o pide credenciales, devuelve `No ejecutado (<motivo>)` y los pasos
   manuales.
2. **Arranca** en segundo plano, con la salida en un archivo; espera como máximo unos 3 minutos.
   Hasta 2 intentos.
3. **Endpoints:** los llama en local (`curl` o `Invoke-WebRequest`) y compara código de estado y
   la parte relevante del cuerpo.
4. **Pantallas:** con la herramienta de automatización del proyecto si existe (Playwright); si no,
   no finge: lista las comprobaciones manuales.
5. **Para** cada proceso que arrancó, y solo esos. Dice qué datos locales creó.

Solo URLs locales: nunca Dev, Staging ni producción. Un arranque fallido es `No ejecutado`, nunca
un aprobado.

### 9.9 doc-writer

**Rol:** escribe la documentación que define el paquete, con los hechos que da. **Nunca cambia
código.**

**Reglas de escritura:**

- C#: `/// <summary>` de una o dos frases; `<remarks>` para la regla o decisión con su fuente
  (`#<id>`, `BR-XX`). `<param>` es todo o nada (documentar solo algunos da CS1573).
- TypeScript: `/** … */`, con `@param` y `@returns` solo si aportan.
- Dice para qué sirve y por qué, desde los hechos; nunca narra el código línea a línea.
- Un símbolo marcado **«desde el código»** se describe por lo que hace (propósito, parámetros,
  retorno, excepciones, efectos: escrituras, caché, llamadas externas), **nunca la intención**.
- **Nunca** cita números de línea (caducan), ni lista quién llama a un símbolo, ni copia un secreto.
  En XML, los nombres de código van en `<c>` o `<see cref>`, nunca entre comillas invertidas.
- Edita en el sitio, manteniendo codificación, BOM y finales de línea. Nada de formato, imports,
  renombrados ni reordenaciones: `comment_only.py` lo detectaría.

**Informe (máximo 40 líneas):**

```text
**Estado:** ✅ Hecha
**Comentarios:** Api/Controllers/OffersController.cs → 4 añadidos · 1 actualizado
**docs/:** api-reference.md → Ofertas
**Sin documentar:** GetLegacy (el código no muestra para qué se usa)
**Fuera del paquete:** ninguno
```

### 9.10 migration-reviewer

**Rol:** revisa las migraciones de Entity Framework Core de una tarea antes de cerrarla. Solo
lectura.

**Lista de comprobación:**

1. **Coincide con el modelo:** cada operación de `Up()` sale de un cambio de entidad o
   configuración de la tarea, y viceversa; el *snapshot* concuerda.
2. **`Down()` revierte `Up()`**, operación a operación, en orden inverso. Si no puede restaurar
   datos (una columna borrada), lo dice.
3. **Pérdida de datos:** `DropColumn`, `DropTable`, estrechar un tipo, un renombrado que EF generó
   como borrar + añadir.
4. **NOT NULL sin valor por defecto** en una tabla con filas.
5. **Bloqueos y tiempo:** índices en tablas grandes sin `ONLINE`, reconstruir columnas, actualizar
   todas las filas.
6. **Claves e índices:** índice único sobre datos que pueden repetirse, borrado en cascada no
   pedido, un índice que una consulta usa y desaparece.
7. **SQL a mano** (`migrationBuilder.Sql`): idempotente, en la misma transacción, sin valores de un
   entorno.
8. **Arranque:** si las migraciones se aplican al arrancar, una lenta o fallida para el despliegue.

Puede ejecutar `dotnet ef migrations script <anterior> <esta> --idempotent` para leer el SQL; nunca
`dotnet ef database update`.

**Informe (máximo 30 líneas):**

```text
**Estado:** ⚠️ Riesgos
alta · Migrations/20261015_AddOfferStatus.cs:18 · columna Status NOT NULL sin valor por defecto en
     Offers (tabla con datos) · añadir defaultValue: 0 o un paso de datos previo
**Comprobado:** 1–8 · dotnet ef migrations script 20260930_Init 20261015_AddOfferStatus --idempotent
```

Un riesgo **alta** devuelve la tarea a `backend-dev` antes de marcarla hecha.

---

## 10. Prompts y plantillas

Los prompts son atajos de Copilot que fijan el modelo de una skill. Las plantillas son la estructura
fija de cada documento: secciones, tablas y anclas que la siguiente skill sabe encontrar. Ninguna
se rellena a mano salvo `story.md` y, a veces, `sdd-guardrails.json`.

### 10.1 El prompt wbs-execution-sonnet

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

> [!NOTE]
> **En Claude Code no hace falta**
>
> La copia de `.claude/skills/wbs-execution/SKILL.md` ya lleva `model: sonnet` en su cabecera, igual
> que `quick-fix` y `test-cases`; `project-context` lleva `opus`.

### 10.2 Plantillas de un work item

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

#### story.md: la única que rellenas tú

`new-sdd-item.py` la crea con un comentario de instrucciones. Así queda rellena:

**docs/sdd/40399-…/story.md:**

```text
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
```

> [!WARNING]
> **Reglas de story.md**
>
> - Copia el texto **literal**: sin resumir, corregir ni traducir.
> - Una sección vacía en Azure DevOps se escribe «Sin <sección> en el work item».
> - Imágenes con nombre descriptivo (`40399-menu-lateral.png`, no `image.png`) y una línea que
>   diga qué muestran: no todas las herramientas ven imágenes.
> - Si depende de otro work item, copia aquí lo necesario de ese otro: la IA solo lee este archivo.
> - Nada sensible: ni credenciales ni datos personales de clientes, tampoco en capturas.
> - `assets/` no se versiona (ADR-0027): los adjuntos ya están en Azure DevOps. Quien retome el work
>   item en otro equipo los baja del work item con los mismos nombres que enlaza `story.md`.
> - Si el work item cambia, actualiza `story.md` y anota el motivo en `bitacora.md`.

#### 05-wbs-estimation.md: la fuente de verdad del avance

**Tabla de tareas de 05 (sdd:tasks):**

| ID | Tarea | Descripción | Capa | Deps | SP | Rol | i18n | Origen | Estado |
| -- | ----- | ----------- | ---- | ---- | -- | --- | ---- | ------ | ------ |
| T-01 | Permiso «ver ofertas» | Nuevo permiso y pruebas | Backend | — | 2 | Backend | No | 03 §3.4 | ✅ Hecha |
| T-02 | Entrada en el menú | Entrada, visibilidad y textos | Frontend | T-01 | 2 | Frontend | Sí | 04 §4.2 | ⬜ Pendiente |

Estados: `⬜ Pendiente` · `🔄 En curso` · `✅ Hecha` · `🔴 Bloqueada`. `wbs-execution` solo cambia
la celda *Estado* y añade una línea en *Registro de ejecución*.

#### 04-implementation-plan.md: las SPECs

**Especificaciones SDD de 04 (sdd:specs):**

| ID | Dado / Cuando / Entonces | Tipo | Prioridad | Cubre |
| -- | ------------------------ | ---- | --------- | ----- |
| SPEC-01 | Dado un usuario Comercial, cuando abre el menú, entonces ve «Ofertas» bajo «Clientes» | Unitaria | Alta | CA-01 |
| SPEC-02 | Dado un usuario JefeVentas, cuando abre el menú, entonces ve «Ofertas» | Unitaria | Alta | CA-02 |
| SPEC-03 | Dado un usuario Consultor, cuando abre el menú, entonces no ve «Ofertas» | Unitaria | Media | CA-02 |

#### Una entrada de CHANGELOG.md

**CHANGELOG.md:**

```text
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
```

### 10.3 Plantillas del proyecto

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

> [!TIP]
> **Mejorar una plantilla**
>
> Las plantillas se cambian en el kit (`core/skills/<skill>/templates/`), nunca en la copia
> instalada. Si quitas o renombras un ancla `<!-- sdd:... -->`, `validate.py` lo detecta: la siguiente
> skill dejaría de encontrar la sección.

---

## 11. Scripts

Los scripts hacen la parte que no debe depender de la IA: instalar, crear la carpeta de un work
item, comprobar artefactos y commits, medir cobertura, demostrar que solo cambiaron comentarios.
Son Python sin dependencias externas, dan siempre el mismo resultado y salen con código 0 (bien) o
1 (errores).

### 11.1 Dónde está cada uno

| Script | Dónde | Lo ejecuta | Para qué |
| --- | --- | --- | --- |
| `install.py` | Kit: `scripts/` | Tú | Instalar o actualizar el kit (capítulo 5) |
| `validate.py` | Kit: `scripts/` | Responsable del kit | Validar el propio kit |
| `new-sdd-item.py` | Kit: `scripts/` | Tú | Crear la carpeta de un work item |
| `check-sdd-item.py` | Kit y `.agents/scripts/` | Tú y las skills | Comprobar los artefactos de un work item o un mensaje de commit |
| `check-encoding.py` | Kit y `.agents/scripts/` | Tú y `pr-check.py` | Comprobar (y reparar) UTF-8 |
| `pr-check.py` | Kit y `.agents/scripts/` | Tú, antes del PR | Las reglas obligatorias de una rama |
| `inventory.py` | `.agents/skills/project-context/scripts/` | `project-context` | Inventario del repositorio |
| `check_project.py` | `.agents/skills/project-context/scripts/` | `project-context`, `document-project`, tú | Comprobar el contexto del proyecto |
| `comment_only.py` | `.agents/skills/document-code/scripts/` | `document-code`, `document-project` | Probar que solo cambiaron comentarios |
| `doc_coverage.py` | `.agents/skills/document-project/scripts/` | `document-project` | Cobertura, áreas, bloques, plan y avisos |
| `test_cases_csv.py` | `.agents/skills/test-cases/scripts/` | `test-cases`, QA | `test-cases.md` → CSV de Azure Test Plans |

Además está el hook `sdd_guard.py` en `.agents/hooks/`, que se explica en el capítulo 12.

### 11.2 new-sdd-item.py

Crea la carpeta de un work item para que prepares `story.md`.

```text
python <kit>/scripts/new-sdd-item.py <id> "<título>" [--tipo pbi|bug] [--por "<persona>"] [--target <raíz>]
```

| Opción | Por defecto | Qué hace |
| --- | --- | --- |
| `id` | — | ID del work item en Azure DevOps |
| `titulo` | — | El título tal cual, entre comillas; de él sale el nombre de la carpeta |
| `--tipo` | `pbi` | `bug` añade las secciones de reproducción e información del sistema |
| `--por` | `git config user.name` | Quién prepara `story.md` |
| `--target` | Carpeta actual | Raíz del proyecto |

**Salida real:**

```text
Creado docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
  story.md     ← cópialo desde Azure DevOps (instrucciones en el comentario del archivo)
  bitacora.md  ← notas de trabajo; ya tiene la primera entrada
  assets/      ← imágenes y archivos del work item, con nombre descriptivo

Siguiente:
  1. Rellena story.md y guarda las imágenes en assets/
  2. python <kit>/scripts/check-sdd-item.py docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral
  3. En una sesión nueva: /enrich-us 40399
```

### 11.3 check-sdd-item.py

Comprueba los artefactos de un work item según el paso alcanzado (sellos, anclas, secciones,
marcadores abiertos, coherencia de la WBS…), o solo un mensaje de commit.

Con ADR-0027 entiende lo que no se versiona:

- **Adjuntos que faltan.** Si `story.md` enlaza un adjunto que no está en tu equipo y git lo
  ignora, da un aviso: «bájalo del work item en Azure DevOps con ese nombre». Un enlace a un archivo
  que no existe y que git no ignora sigue siendo un error.
- **Paso 5.** Cuando la carpeta ya está en un commit con `Ref: #<id>`, comprueba ese mensaje (el
  `commit-message.md` ya no viaja con el repositorio). Antes del commit, comprueba `commit-message.md`.

```text
python .agents/scripts/check-sdd-item.py <carpeta>
python .agents/scripts/check-sdd-item.py --commit-message <archivo> --id <id>
```

**Carpeta recién creada, story.md sin rellenar (salida real):**

```text
Work item: 40399-seccion-de-ofertas-en-el-menu-lateral · paso alcanzado: 0 · story.md

  ✓ carpeta — docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral
  ✓ story.md — preparado por Ana Pérez
  ⚠ story.md — 14 campo(s) sin rellenar: <proyecto>, <N>, <estado>, <ruta>, <persona>, <texto literal> …
  ✗ story.md — la descripción está vacía o sin rellenar
  ✓ bitacora.md
  ⚠ pbi.md / bug.md — todavía no existe (paso 1)

  1 errores · 2 avisos
```

**Un mensaje de commit con tres errores (salida real):**

```text
Mensaje de commit: msg.txt

  ✓ commit: primera línea tipo(ámbito): descripción
  ✗ commit: Ref — falta la línea «Ref: #<id>»
  ✗ commit: firma de IA — quita las líneas Co-Authored-By / Generated with: el sello SDD es la evidencia (ADR-0004)
  ✗ commit: cierre automático — no uses fix/fixes/fixed #id: Azure Repos cerraría el work item
  ✓ commit: tamaño — 105 caracteres

  3 errores · 0 avisos
```

Qué comprueba del mensaje: primera línea `tipo(ámbito): descripción` (≤ 72 caracteres), la línea
`PBI-<id>`/`BUG-<id>` con el título, `Ref: #<id>` (opcional, con aviso, en `docs`, `chore`, `ci` y
`style`), sin `fix #id`, sin firmas de IA y como máximo 4000 caracteres.

> [!TIP]
> **Comprobar el commit que acabas de hacer (Windows)**
>
> ```powershell
> cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"
> python .agents\scripts\check-sdd-item.py --commit-message $env:TEMP\msg.txt --id 40399
> ```
> Usa `cmd /c`: el `>` de PowerShell 5.1 estropea las tildes.

### 11.4 pr-check.py

Las reglas obligatorias de una rama, **antes de abrir el PR** (ADR-0023). Es la red que no depende
de que la IA obedezca.

```text
python .agents/scripts/pr-check.py [--base origin/dev] [--root <raíz>]
```

| Comprobación | Error si… |
| --- | --- |
| Commits | Algún commit de la rama no sigue el formato (usa `check-sdd-item.py`) |
| Rutas protegidas | La rama cambia una ruta de `protected` de `sdd-guardrails.json` |
| Archivos de secretos | La rama añade un archivo que coincide con `secrets` |
| Borradores | La rama añade o cambia algo en `docs/sdd/_borradores/` (ADR-0027). Borrarlo está permitido |
| Archivos locales (aviso) | La rama añade a propósito un adjunto, `commit-message.md` o `test-cases.csv`, que no se versionan |
| Archivos del kit | La rama cambia archivos del kit sin un commit `chore(sdd)` |
| `AGENTS.md` | Pasa de 200 líneas |
| Secretos en el diff | El diff contiene patrones de claves, tokens o cadenas de conexión |
| Codificación | Un archivo cambiado no está en UTF-8 |

**Una rama con tres problemas (salida real):**

```text
pr-check · demo · feature/40399-seccion-ofertas..HEAD

  ✗ commit 1423eb02 — «arreglar cosas fix #123»: commit: primera línea (no sigue tipo(ámbito): descripción
    → «arreglar cosas fix #123»); commit: Ref (falta la línea «Ref: #<id>»); commit: cierre automático
    (no uses fix/fixes/fixed #id: Azure Repos cerraría el work item)
  · archivos — 2 cambiados o nuevos, 0 borrados
  ✗ rutas protegidas — Api/Legacy/Old.cs
  ✗ archivos de secretos — .env
  ✓ borradores — ninguno en la rama
  ✓ archivos del kit — sin cambios a mano
  ✓ AGENTS.md — 69 líneas (máximo 200)
  ✓ secretos en el diff — ninguno
  ✓ codificación UTF-8 — correcta

  3 errores · 0 avisos
```

**Una rama con un borrador (salida real):**

```text
  ✗ borradores — docs/sdd/_borradores/tipos.md: crea el work item en Azure DevOps, anota su ID donde
    se citaba el borrador (bitacora.md, qa-report.md, plan.md) y borra el archivo antes del PR (ADR-0027)
```

**Una rama correcta (salida real):**

```text
pr-check · demo · dev..HEAD

  ⚠ commit 66dd21f6 — «chore(sdd): configurar los guardarraíles»: commit: título del ticket; commit: Ref
  · archivos — 1 cambiados o nuevos, 0 borrados
  ✓ rutas protegidas — sin cambios
  ...
  0 errores · 1 avisos
```

Los avisos no bloquean: un commit `chore(sdd)` sin work item no lleva `Ref:` y es lo esperado.

### 11.5 check-encoding.py

```text
python .agents/scripts/check-encoding.py [--base origin/dev] [--fix]
```

Revisa que los archivos de texto cambiados frente a la base están en UTF-8. Con `--fix` convierte
los que no lo están (manteniendo el BOM si lo había). Típico en Windows con archivos guardados en
ANSI por otro editor.

**Lo que responde:**

```text
1 archivo(s) de texto cambiados frente a dev

  ✓ Todos están en UTF-8
```

### 11.6 validate.py (solo el kit)

Valida el kit antes de cada commit al kit: estándar Agent Skills (nombre, descripción, tamaño del
`SKILL.md` ≤ 500 líneas), el bloque de convenciones idéntico en las 9 skills, anclas y sellos de
las plantillas, formato de los agentes, tamaño de `AGENTS.base.md`, versiones y que cada ADR esté
en el índice.

**Lo que responde:**

```text
9 skills · 7 agents checked · 0 errors · 0 warnings
```

### 11.7 inventory.py

Inventario determinista para `project-context`: proyectos .NET y de pruebas, paquetes, lockfiles,
CI, contenedores y submódulos, traducciones, documentación existente, configuración de IA
existente y tabla de endpoints REST.

```text
python .agents/skills/project-context/scripts/inventory.py --out <temp>/inventario.md --endpoints <temp>/endpoints.md
```

**Extracto real:**

```text
# Inventario de `demo`
Generado por inventory.py (fi-sdd-standard). Cada dato indica su archivo.
## CI
- Sin pipelines
## Traducciones
- Sin archivos de traducción detectados
## Configuración de IA existente
- `AGENTS.md`: 68 líneas, bloque del kit sí; secciones de contexto: ninguna
- `CLAUDE.md`: 1 líneas (solo importa `@AGENTS.md`)
- `.sdd-kit.json`: fi-sdd-standard v0.12.0
```

### 11.8 check_project.py

Comprueba el contexto del proyecto: bloque del kit, encabezados fijos de *Project context*, sello y
marca `sdd:context`, tamaño de `AGENTS.md` y de cada sección, `CLAUDE.md`, los seis `docs/`,
`[REQUIRES-VALIDATION]` abiertos, fuentes cambiadas desde la fecha del contexto,
`sdd-guardrails.json` frente a *Protected paths* y la existencia de pruebas de arquitectura.

```text
python .agents/skills/project-context/scripts/check_project.py [--root <raíz>]
```

Debe acabar en **0 errores** antes de `/document-project` y del primer work item. Los avisos se
resuelven con `/project-context check`.

### 11.9 comment_only.py

Demuestra que la documentación solo cambió comentarios.

```text
python comment_only.py save    <copia> <archivo> [...]   # antes: guarda una copia (también de archivos sin seguimiento)
python comment_only.py check   <copia> <archivo> [...]   # después: compara
python comment_only.py restore <copia> <archivo> [...]   # descarta la documentación de un archivo, byte a byte
```

`check` exige que cada línea añadida, quitada o cambiada sea un comentario o esté en blanco, y que
no cambien el BOM ni los finales de línea. Código de salida 0 = solo comentarios, 1 = otra cosa
cambió, 2 = error de uso. No revisa `docs/`.

**Salida real: un cambio que no es comentario:**

```text
✗ Api/Controllers/PingController.cs
    línea 2 (antes) cambió o se borró: public class PingController {}
    línea 3 (ahora) no es comentario: public class PingController { int x; }

1 archivo(s) con cambios que no son comentarios
```

### 11.10 doc_coverage.py

La herramienta de medición de `document-project`. Es una heurística por líneas (no el
compilador): sirve para planificar y medir antes y después.

| Modo | Qué hace |
| --- | --- |
| (sin opciones) | Cobertura del proyecto: símbolos documentados por carpeta |
| `--areas` | Propone áreas, partes y bloques (tablas y lista de archivos por área) |
| `--files <archivos>` | Símbolos sin comentario de esos archivos: línea, tipo, nombre |
| `--build-log <log>` | Cuenta los CS1591 (miembro público sin comentario) de un log de build |
| `--check-plan <plan.md>` | Comprueba el plan: cada archivo a documentar en exactamente un área, sin archivos desconocidos |
| `--warnings <log> --out avisos.md` | Avisos del build por código y archivo (sin duplicados; `NU19xx` aparte) |
| `--warnings <log> --compare avisos.md` | Compara con la línea base; sale con 1 si hay avisos nuevos |
| `--out`, `--json`, `--root` | Dónde escribir el informe, la versión JSON y la raíz |

**Extracto real de --areas:**

```text
| ID | Área | Tipo | Archivos | Pruebas | Sin documentar | Cambios 6 m | Bloque | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | Ping | backend | 1 | 0 | 1/1 | 1 | B-01 |  |

| Bloque | Áreas | Archivos | Sin documentar |
| --- | --- | --- | --- |
| B-01 | A-01 | 1 | 1 |
```

> [!WARNING]
> **Builds comparables**
>
> Compara siempre builds hechos igual: `dotnet build <solución> --no-incremental`. Un build
> incremental se salta proyectos y oculta sus avisos, y la comparación saldría engañosamente mejor.

### 11.11 test_cases_csv.py

```text
python .agents/skills/test-cases/scripts/test_cases_csv.py <test-cases.md> [--out <csv>] [--area "<Area\Path>"] [--include-blocked]
```

Convierte las secciones `### TC-NN` en el CSV que importa Azure Test Plans (columnas `ID`, `Work
Item Type`, `Title`, `Test Step`, `Step Action`, `Step Expected`, `Area Path`, `State`), en UTF-8
con BOM. Los casos `Bloqueado` quedan fuera salvo con `--include-blocked`. Ejemplo completo en el
capítulo 7.

---

## 12. Guardarraíles

Las reglas de `AGENTS.md` dicen a la IA qué no debe hacer, pero una instrucción se puede olvidar.
Los guardarraíles (ADR-0023) hacen que cada regla obligatoria tenga, además, **una comprobación que
no depende de que la IA obedezca**: un permiso que lo impide, un hook que lo bloquea, una prueba
que falla o un script que lo detecta antes del PR.

### 12.1 Las cinco capas

*Esquema: las cinco capas de guardarraíles, de la más temprana a la última.*

```text
Antes de actuar        permisos deny (.claude/settings.json)   bloquea leer secretos y git commit/push
Al usar una herramienta sdd_guard.py pre (hook PreToolUse)     bloquea secretos y rutas protegidas
Tras editar            sdd_guard.py post (hook PostToolUse)    formatea, revisa UTF-8, avisa de patrones
Al compilar y probar   ArchitectureTests (xUnit)               capas y autorización de endpoints
Antes del PR           pr-check.py (.agents/scripts/)          commits, rutas, secretos, kit, UTF-8
```

| Capa | Pieza | Qué hace | En qué herramienta |
| --- | --- | --- | --- |
| 1 | Permisos `deny` en `.claude/settings.json` | Impide leer secretos y ejecutar `git commit`, `git push`, `git reset --hard`, `git clean`, `git branch -D`, `rm -rf` | Claude Code |
| 2 | Hook `sdd_guard.py pre` | Bloquea leer o editar secretos y editar rutas protegidas, también desde comandos de shell | Claude Code |
| 3 | Hook `sdd_guard.py post` | Tras cada edición: formatea, avisa si el archivo dejó de estar en UTF-8 y avisa de patrones obligatorios | Claude Code |
| 4 | `ArchitectureTests.cs` | Pruebas que fallan si se rompe una regla de arquitectura | Todas (`dotnet test`, y el pipeline) |
| 5 | `pr-check.py` | Commits, rutas protegidas, secretos, archivos del kit, tamaño de `AGENTS.md`, UTF-8 | Todas (y el pipeline en la fase 4) |

> [!NOTE]
> **En Copilot no hay hooks**
>
> Copilot no ejecuta hooks ni respeta `.claude/settings.json`. Ahí las capas 4 y 5 son las que
> garantizan las reglas: por eso `pr-check.py` es obligatorio antes de cada PR, uses la herramienta
> que uses.

### 12.2 Permisos deny

El instalador añade 20 reglas a `permissions.deny` de `.claude/settings.json`, sin tocar las que ya
tuvieras:

```json
"deny": [
  "Read(./.env)", "Read(./.env.*)", "Read(./**/.env)", "Read(./**/.env.*)",
  "Read(./**/appsettings.*.json)", "Read(./**/secrets.json)",
  "Read(./**/*.pfx)", "Read(./**/*.pem)", "Read(./**/*.key)",
  "Bash(git commit *)", "Bash(git push *)", "Bash(git push)", "Bash(git reset --hard *)",
  "Bash(git clean *)", "Bash(git branch -D *)", "Bash(rm -rf *)",
  "PowerShell(git commit *)", "PowerShell(git push *)", "PowerShell(git reset --hard *)",
  "PowerShell(Remove-Item * -Recurse *)"
]
```

> [!NOTE]
> **appsettings.json sí se puede leer**
>
> Solo se bloquean los de entorno (`appsettings.Development.json`, `appsettings.Production.json`…),
> que son los que suelen llevar credenciales. `appsettings.json` es configuración compartida. Aun
> así, la regla de `AGENTS.md` pide leer la configuración por su estructura, nunca por sus valores.

### 12.3 El hook sdd_guard.py

Un solo script de Python, sin dependencias, en `.agents/hooks/sdd_guard.py` (versionado). El
instalador lo registra en `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse":  [{ "matcher": "Read|Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell",
                    "hooks": [{ "type": "command", "command": "python",
                                "args": ["${CLAUDE_PROJECT_DIR}/.agents/hooks/sdd_guard.py", "pre"],
                                "timeout": 30 }] }],
  "PostToolUse": [{ "matcher": "Edit|Write|MultiEdit",
                    "hooks": [{ "type": "command", "command": "python",
                                "args": ["${CLAUDE_PROJECT_DIR}/.agents/hooks/sdd_guard.py", "post"],
                                "timeout": 120 }] }]
}
```

| Modo | Evento | Bloquea o avisa | Código de salida |
| --- | --- | --- | --- |
| `pre` | Antes de Read, Edit, Write, MultiEdit, NotebookEdit, Bash, PowerShell | **Bloquea** editar una ruta `protected` y leer o editar un archivo de `secrets`, también si el comando de shell lo nombra | 2 = bloqueado · 0 = sigue |
| `post` | Después de Edit, Write, MultiEdit | Ejecuta el formateador de `format`; **avisa** si el archivo ya no es UTF-8 y de cada `pattern` incumplido. El agente lee el aviso y corrige | 2 = aviso para el agente · 0 = nada |

Si el propio hook falla (un error interno), sale con 0: **nunca bloquea por un fallo propio**.

#### Lo que verás

Salidas reales del hook con la configuración de ejemplo:

**Leer un archivo de entorno:**

```text
fi-sdd-standard · bloqueado: «Api/appsettings.Development.json» puede contener secretos
(patrón «**/appsettings.*.json»); pide a una persona el dato que necesitas (sdd-guardrails.json, ADR-0023)
```

**Un cat .env desde el shell:**

```text
fi-sdd-standard · bloqueado: el comando usa «.env», que puede contener secretos (patrón «.env»)
(sdd-guardrails.json, ADR-0023)
```

**Editar una ruta protegida:**

```text
fi-sdd-standard · bloqueado: «Api/Legacy/Old.cs» es una ruta protegida (patrón «Api/Legacy/**»);
el cambio va en su origen (sdd-guardrails.json, ADR-0023)
```

**Aviso de patrón tras escribir un controller sin autorización:**

```text
fi-sdd-standard · Api/Controllers/PingController.cs:
  - Todo controller declara su autorización ([Authorize] o [AllowAnonymous])
```

#### Probarlo a mano

```powershell
'{"tool_name":"Read","tool_input":{"file_path":"Api/appsettings.Development.json"}}' | python .agents\hooks\sdd_guard.py pre
$LASTEXITCODE     # 2 = bloqueado
'{"tool_name":"Read","tool_input":{"file_path":"Api/appsettings.json"}}' | python .agents\hooks\sdd_guard.py pre
$LASTEXITCODE     # 0 = permitido
```

### 12.4 sdd-guardrails.json

La configuración del hook y de `pr-check.py`, en la raíz del proyecto, versionada. La crea
`install.py` y la completa `/project-context`. Las rutas y globs son relativas a la raíz, con la
sintaxis de `.gitignore` (`**` para cualquier profundidad).

| Clave | Tipo | Para qué | La usa |
| --- | --- | --- | --- |
| `protected` | Lista de globs | Rutas que la IA nunca edita: librerías compartidas, submódulos, código generado, documentación de otro equipo | Hook `pre`, `pr-check.py` |
| `secrets` | Lista de globs | Archivos que nadie lee ni sube | Hook `pre`, `pr-check.py` |
| `secretsAllowed` | Lista de globs | Excepciones a `secrets` (por ejemplo, una plantilla `.env.example` sin valores). Cada una, justificada en el PR | Hook, `pr-check.py` |
| `format` | Extensión → comando | Formateador tras cada edición; `{file}` es el archivo | Hook `post` |
| `patterns` | Lista de `{glob, require/forbid, message}` | Reglas que una expresión regular puede comprobar | Hook `post` |

**sdd-guardrails.json (ejemplo completo):**

```text
{
  "protected": [
    "ClientApp/src/core-ui/**",
    "docs/modernizacion/**"
  ],
  "secrets": [".env", ".env.*", "**/appsettings.*.json", "**/secrets.json", "**/*.pfx", "**/*.pem", "**/*.key"],
  "secretsAllowed": [".env.example"],
  "format": {
    ".cs":  ["dotnet", "csharpier", "format", "{file}"],
    ".tsx": ["npx", "prettier", "--write", "{file}"]
  },
  "patterns": [
    {
      "glob": "**/Controllers/*Controller.cs",
      "require": "\\[(Authorize|AuthorizeRoles|AllowAnonymous)",
      "message": "Todo controller declara su autorización ([Authorize] o [AllowAnonymous])"
    },
    {
      "glob": "ClientApp/src/**/*.tsx",
      "forbid": "console\\.log\\(",
      "message": "Sin console.log en componentes: usa el logger del proyecto"
    }
  ]
}
```

> [!WARNING]
> **Revísalo a mano en el PR**
>
> - Las rutas protegidas deben ser las del proyecto (*Protected paths* de `AGENTS.md`):
>   `check_project.py` avisa si no coinciden.
> - Nada en `secretsAllowed` sin un motivo.
> - Un formateador solo si se ejecutó y funciona (lo verifica `/project-context`): un comando
>   que falla en cada edición es ruido.

### 12.5 Pruebas de arquitectura

`/project-context` copia `ArchitectureTests.cs` al proyecto de pruebas
(`<Tests>/Architecture/`) y `backend-dev` rellena sus marcadores. Son pruebas xUnit por reflexión:
corren con el resto de la suite y en el pipeline.

| Prueba | Regla | Falla si… |
| --- | --- | --- |
| `Los_controllers_no_dependen_del_DbContext` | Los controllers usan servicios, nunca el `DbContext` | Un controller lo recibe en el constructor |
| `Todo_endpoint_declara_su_autorizacion` | Autorización explícita | Un controller sin atributo tiene una acción pública sin `[Authorize]`, `[AllowAnonymous]` ni requisito de autorización |
| `La_capa_de_datos_no_depende_de_los_servicios` | Dirección de dependencias | Un tipo de la capa de datos usa un tipo de la capa de servicios |

Los cuatro marcadores que se adaptan:

```csharp
//   {{TestNamespace}}     espacio de nombres del proyecto de pruebas (p. ej. MiProyecto.Tests)
//   {{AppMarkerType}}     un tipo público de la aplicación (p. ej. Program)
//   {{DataNamespace}}     capa de datos (p. ej. MiProyecto.Data)
//   {{ServicesNamespace}} capa de servicios (p. ej. MiProyecto.Services)
```

**Las reglas no se relajan.** Lo que ya las incumple va a una lista de excepciones con su motivo:

```csharp
// Controllers que todavía usan el DbContext directamente (deuda). Nombre de la clase y motivo.
private static readonly HashSet<string> DbContextExceptions = [
    "ReportsController", // consultas de solo lectura heredadas; work item #40712 para moverlas
];
```

Una excepción nueva la decide el tech lead; la lista solo debería encoger con el tiempo.

```powershell
dotnet test MiProyecto.Tests --filter "FullyQualifiedName~Architecture"
```

### 12.6 La matriz: cada regla con su comprobación

| Regla de `AGENTS.md` | Permiso | Hook | Prueba | `pr-check.py` | Otra |
| --- | --- | --- | --- | --- | --- |
| No leer ni imprimir secretos | ✓ lectura | ✓ lectura y shell | — | ✓ archivos y patrones en el diff | `code-explorer` |
| No editar rutas protegidas ni submódulos | — | ✓ | — | ✓ | — |
| La IA no hace commit, push ni cambia de rama | ✓ | — | — | — | — |
| Formato del commit, `Ref: #id`, sin `fix #id`, sin firma de IA | — | — | — | ✓ | `check-sdd-item.py` |
| UTF-8 conservando el BOM | — | ✓ aviso | — | ✓ | `check-encoding.py --fix` |
| Artefactos del work item | — | — | — | ✓ | `check-sdd-item.py` |
| Archivos del kit solo cambian con `install.py` | — | — | — | ✓ | `.sdd-kit.json` |
| Los borradores no llegan a `dev`; adjuntos, `commit-message.md` y CSV fuera del repositorio | — | — | — | ✓ | `.gitignore` de `install.py` (ADR-0027) |
| `AGENTS.md` < 200 líneas | — | — | — | ✓ | `check_project.py` |
| Controllers sin `DbContext` | — | — | ✓ | — | — |
| Todo endpoint con autorización explícita | — | ✓ aviso | ✓ | — | — |
| Capas: datos sin servicios | — | — | ✓ | — | — |
| Documentar solo cambia comentarios | — | — | — | — | `comment_only.py` |
| Patrones obligatorios del proyecto | — | ✓ aviso | si se puede | — | `qa-review` |
| Textos visibles en todos los idiomas | — | — | — | — | `qa-review` (fase 4: en el PR) |
| No inventar reglas de negocio | — | — | — | — | Revisión humana y `qa-review` |

---

## 13. Marcadores, sellos, anclas y bitácora

Son las convenciones que permiten que nueve skills distintas, en herramientas distintas, se
entiendan entre sí y que una persona sepa en todo momento qué está confirmado y qué no. Están en el
bloque *Shared SDD conventions*, idéntico en todas las skills.

### 13.1 Marcadores

Un marcador señala un hueco que la IA **no puede rellenar por su cuenta**. Mientras exista, el
documento no está cerrado.

| Marcador | Significa | Ejemplo | Lo resuelve |
| --- | --- | --- | --- |
| `[PENDING-BUSINESS: <pregunta>]` | Falta información de negocio que solo una persona puede dar | `[PENDING-BUSINESS: ¿cuántos días de antelación como máximo?]` | El PO o quien tenga la respuesta |
| `[REQUIRES-VALIDATION: <motivo>]` | Una afirmación técnica sin evidencia directa en el código | `[REQUIRES-VALIDATION: no se ve si el job se ejecuta en producción]` | Un dev, con un comando, una pantalla o una persona |
| `[ASSUMPTION-BASED: <campo>]` | Una sección construida encima de un campo sin resolver | `[ASSUMPTION-BASED: límite de días]` en 03 §3.4 | Se resuelve al resolver el campo del que depende |
| `[PENDING-TRANSLATION: <clave> → <idioma>]` | Una traducción que la IA no puede dar con seguridad | `[PENDING-TRANSLATION: Offers → fr]` | Alguien con el idioma, o el PO decide dejarlo pendiente |

Dónde frenan:

- `technical-analysis` se para si `pbi.md` tiene `[PENDING-BUSINESS]` y te pregunta si sigues (las
  secciones afectadas saldrían `[ASSUMPTION-BASED]`).
- `wbs-execution` se para si el resumen ejecutivo lista `[ASSUMPTION-BASED]` o
  `[REQUIRES-VALIDATION]`.
- `quick-fix` no admite ningún `[PENDING-BUSINESS]`.
- `test-cases` deja Bloqueados los casos con un `[PENDING-BUSINESS]`.
- `wbs-execution` hace un **barrido** al cerrar: los resueltos se sustituyen por la decisión; los
  abiertos van al informe y a `commit-message.md`.

#### Resolver un marcador

Cuando tengas la respuesta, díselo a la IA con quién la dio:

**Lo que pides:**

```text
El máximo son 30 días; lo confirmó Laura Gómez (PO) hoy.
```

La IA quita el marcador **en todos los archivos de la carpeta** que lo tengan (incluido
`pbi.md`), escribe la respuesta en su lugar, registra quién la resolvió en `bitacora.md` y, al
final, te da el *Comentario para Azure DevOps*.

### 13.2 Sello de trazabilidad

Cada archivo que genera la IA empieza su bloque de metadatos con:

```markdown
**Generado con:** enrich-us v3.9 · Claude Code · claude-opus-5-5
```

- `<skill> v<versión>`: la skill y la versión de las skills del kit.
- `<herramienta>`: `Claude Code`, `GitHub Copilot` o `Codex`.
- `<modelo>`: el de la sesión que ejecutó la skill (los de los subagentes los fija la versión del
  kit). Si la sesión no lo sabe, el modelo por defecto del equipo, `claude-opus-5-5`.

Es **la evidencia verificable** de que el documento lo produjo la IA, y por eso los commits no
llevan `Co-Authored-By` (ADR-0004). Nunca se borra. `story.md`, que lo prepara una persona, lleva
`**Preparado por:**` en su lugar.

Cuando una skill posterior cambia un documento con una decisión confirmada, añade debajo:

```markdown
**Actualizado con:** technical-analysis v3.9 · Claude Code · claude-opus-5-5 (2026-10-16: CA-03 añadido, aprobado por Laura Gómez)
```

### 13.3 Anclas

Las anclas son comentarios HTML que marcan secciones: la skill siguiente busca el ancla, no el
título, así que funciona aunque el título cambie o esté en otro idioma.

| Ancla | Archivo | La lee |
| --- | --- | --- |
| `sdd:description` · `sdd:acceptance-criteria` · `sdd:pending` | `pbi.md`, `bug.md` | `technical-analysis`, `test-cases` |
| `sdd:qa-classification` | `pbi.md`, `bug.md` | `test-cases` |
| `sdd:i18n` | `pbi.md`, `bug.md`, `01` §1.8 | `technical-analysis`, `wbs-execution` |
| `sdd:markers` | `00` | `wbs-execution` |
| `sdd:specs` | `04` | `wbs-execution`, `qa-review`, `test-cases` |
| `sdd:tasks` · `sdd:task-log` | `05`, `fix-plan.md` | `wbs-execution`, `check-sdd-item.py` |
| `sdd:risks` | `06` | `wbs-execution`, `qa-review` |
| `sdd:fix-gate` · `sdd:fix-cause` · `sdd:fix-tests` | `fix-plan.md` | `qa-review`, `check-sdd-item.py` |
| `sdd:qa-findings` | `qa-report.md` | `wbs-execution qa` |
| `sdd:test-cases` | `test-cases.md` | `test_cases_csv.py` |
| `sdd:log` | `bitacora.md`, `plan.md` | Todas |
| `sdd:doc-areas` · `sdd:doc-blocks` · `sdd:doc-findings` | `plan.md` | `document-project`, `doc_coverage.py` |
| `sdd:context` | *Project context* de `AGENTS.md` | `check_project.py` (fecha y fuentes) |
| `sdd-kit:base:start` / `end` | `AGENTS.md` | `install.py` |

> [!CAUTION]
> **No borres un ancla**
>
> Si editas un documento a mano, deja los comentarios `<!-- sdd:... -->` donde están.
> `check-sdd-item.py` avisa si falta una.

### 13.4 La bitácora

`bitacora.md` es la memoria del work item. Cualquier persona que retome el trabajo (o una sesión
nueva) sabe qué se preguntó, qué se respondió y quién lo confirmó.

**bitacora.md:**

```text
# Bitácora — 40399 Sección de ofertas en el menú lateral

**Generado con:** enrich-us v3.9 · Claude Code · claude-opus-5-5
**Work item:** #40399 · **Carpeta:** docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/

## Decisiones

| Fecha | Decisión | Confirmada por | En pbi.md |
| ----- | -------- | -------------- | --------- |
| 2026-10-15 | Ven la sección Comercial y Jefe de ventas | Laura Gómez | Sí |

## Preguntas abiertas

- [ ] 2026-10-15 · ¿Orden de las ofertas: por fecha ascendente o descendente? · para: PO

## Registro

<!-- sdd:log -->
- 2026-10-15 · Ana Pérez · carpeta creada; story.md preparado a partir del work item
- 2026-10-15 · enrich-us · story.md leído · adjuntos revisados: 1 de 1 · huecos: 0
- 2026-10-15 · enrich-us · pbi.md generado · pendientes: 0
- 2026-10-15 · technical-analysis · diseño 00–06 generado · 4 SP · 2 tareas

## Hallazgos

- 2026-10-15 · technical-analysis · SideMenu.tsx:30 — «Inicio» sin i18n (deuda previa, fuera de alcance)
```

Reglas:

- **Solo crece.** Nunca se edita, fusiona ni reordena una línea anterior. Un hallazgo que resulta
  falso no se borra: se añade otro que lo corrige («corrige el hallazgo del 2026-10-15»).
- Una línea por entrada: `<fecha> · <skill o persona> · <qué>`.
- **Toda decisión confirmada pasa también a `pbi.md`/`bug.md`**, que es el contrato que leen los
  pasos siguientes, y se marca «Sí» en la tabla. `enrich-us` no termina con decisiones sin pasar.
- Los nombres de las personas se escriben siempre igual.

### 13.5 Comentario para Azure DevOps

Cuando un paso confirma decisiones que cambian el work item (alcance, criterios, reglas), el
informe final termina con un bloque listo para pegar en Azure DevOps:

**Lo que responde:**

```text
Comentario para Azure DevOps:
2026-10-15 · Decisiones del análisis (enrich-us):
- Ven la sección «Ofertas» los roles Comercial y Jefe de ventas (confirmado por Laura Gómez).
- El texto del menú será «Ofertas» en es, «Offers» en en y «Offres» en fr (propuesto, validado por Laura Gómez).
```

La IA no lo publica: lo pegas tú. Solo lo haría con el MCP de Azure DevOps habilitado con
escritura y si se lo pides.

### 13.6 Borradores de work items

Un problema real que no es de este work item (un bug, una deuda) no se arregla de paso: se escribe
como propuesta en `docs/sdd/_borradores/<slug>.md` para que una persona lo cree en Azure DevOps. Se
registra en la bitácora y se menciona en el informe final. Nunca es un `story.md`.

El borrador es temporal y **no llega a `dev`** (ADR-0027). Antes del PR:

1. Crea el work item en Azure DevOps con el contenido del borrador.
2. Anota su ID donde se citaba: una línea en `bitacora.md`
   (`2026-10-16 · Ana Pérez · borrador build-sin-tipos creado como #41100`), el estado del hallazgo
   en `qa-report.md` (`Work item #41100`) o la fila de *Hallazgos* de `plan.md`.
3. Borra el borrador.

`pr-check.py` da error si la rama añade o cambia un borrador, así que nadie se olvida: el hallazgo
acaba en el backlog, que es donde se prioriza, y no escondido en una carpeta del repositorio.

---

## 14. Git, commit y PR

La IA prepara el mensaje de commit y te da los comandos con rutas exactas, pero el commit, el push y
el PR los haces tú. Este capítulo recoge el formato del mensaje, el camino de un work item terminado
hasta `dev` y cómo llevar el kit de un piloto a `dev`.

### 14.1 El mensaje de commit

Un work item, **un commit** (ADR-0004). El mensaje sigue `.gitmessage` y se reutiliza como
descripción del PR. `wbs-execution` y `quick-fix` lo escriben completo en `commit-message.md` desde
el `CHANGELOG.md`; `qa-review` y `document-code` solo añaden una viñeta.

**docs/sdd/40399-…/commit-message.md:**

```text
feat(menu): añadir la sección de ofertas al menú lateral

PBI-40399 — [MENÚ] Sección de ofertas en el menú lateral

**Problema**
Los comerciales no tenían acceso directo a sus ofertas: debían entrar por Clientes.

**Cambios**
- Backend (Permissions.cs): permiso ViewOffers para Comercial y Jefe de ventas.
- Frontend (SideMenu.tsx): entrada «Ofertas» bajo «Clientes», visible con ViewOffers.
- Traducciones (es.json, fr.json): clave «Offers» en todos los idiomas.
- Documentación: comentarios en 2 archivos; docs/frontend.md.

**Alcance y no regresión**
- No cambian las rutas del API ni los permisos existentes.

**Pruebas**
- PermissionsTests: 3 nuevas (Rojo → verde). dotnet test: 301/301.
- SideMenu.test.tsx: 3 casos por rol. yarn test: 51/51 · lint y tipos OK.
- Revisión de QA (qa-review, ronda 2): sin hallazgos altos ni medios.

Ref: #40399
```

| Regla | Por qué |
| --- | --- |
| Primera línea `tipo(ámbito): descripción`, minúscula, imperativo, sin punto, ≤ 72 caracteres | Legible en `git log --oneline` y como título del PR |
| `tipo`: `feat` · `fix` · `refactor` · `perf` · `docs` · `test` · `chore` · `ci` · `style` · `revert` | Clasificar el cambio |
| Segunda línea en blanco y luego `PBI-<id> — [MÓDULO] <título>` (o `BUG-<id>`) | Enlaza con el work item a simple vista |
| Rótulos en negrita (**Problema**, **Causa**, **Cambios**, **Alcance y no regresión**, **Pruebas**), nunca `#` | Git borra las líneas que empiezan por `#` |
| **Pruebas**: solo lo que se ejecutó de verdad | Es evidencia, no una promesa |
| Última línea `Ref: #<id>` | Enlaza el work item **sin cambiar su estado** |
| Nunca `fix #id`, `fixes #id`, `fixed #id` | Azure Repos cerraría el work item |
| Sin `Co-Authored-By` ni «Generated with» | El sello SDD es la evidencia (ADR-0004) |
| Todo el mensaje < 4000 caracteres | Es la descripción del PR |

### 14.2 De un work item terminado a dev

#### 1 · Rama, antes de empezar

```powershell
git fetch origin
git switch -c feature/40399-seccion-ofertas origin/dev
git push -u origin feature/40399-seccion-ofertas
```

#### 2 · Antes del commit

```powershell
python .agents\scripts\check-sdd-item.py docs\sdd\40399-seccion-de-ofertas-en-el-menu-lateral   # 0 errores
git status --short     # solo el código del work item y su carpeta
```

**Borradores.** Si alguna skill dejó propuestas en `docs/sdd/_borradores/`, crea ahora cada work
item en Azure DevOps y anota su ID donde se citaba el borrador: una línea en `bitacora.md` y, si
venía de QA, el estado del hallazgo en `qa-report.md` (`Work item #41100`). Después borra el
borrador (`git rm`, o bórralo sin más si nunca se versionó). Los borradores no llegan a `dev`:
`pr-check.py` da error si encuentra uno en la rama.

#### 3 · Un solo commit, con rutas exactas

Copia el `git add` que te dio la skill al cerrar (o construye la lista desde `git status --short`):

```powershell
git add Api/Authorization/Permissions.cs MiProyecto.Tests/Authorization/PermissionsTests.cs `
        ClientApp/src/layout/SideMenu.tsx ClientApp/src/layout/SideMenu.test.tsx `
        ClientApp/src/i18n/es.json ClientApp/src/i18n/fr.json docs/frontend.md `
        docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
git status --short     # nada del work item en «??» ni sin preparar
git commit -F docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/commit-message.md
```

Al añadir la carpeta del work item, git salta lo que no se versiona (ADR-0027): `assets/`,
`commit-message.md` y `test-cases.csv` están en el `.gitignore`. `git commit -F` lee
`commit-message.md` de tu disco igualmente, y el mensaje queda guardado en el commit.

> [!CAUTION]
> **Nunca git add -A ni git add .**
>
> Se colarían archivos ajenos: copias locales de `.claude/`, logs, un `.env`. Y recuerda que los
> archivos nuevos (`??`) hay que añadirlos con `git add`: `git commit -- <rutas>` no los incluye.

#### 4 · Comprobar

```powershell
git log --oneline origin/dev..HEAD                 # una sola línea
python .agents\scripts\pr-check.py                 # 0 errores
```

Si hay varios commits, júntalos antes del push: `git reset --soft origin/dev` y vuelve a hacer el
commit con `-F`. Si `dev` avanzó, `git rebase origin/dev` y vuelve a pasar las pruebas.

#### 5 · Push y PR

```powershell
git push -u origin feature/40399-seccion-ofertas
Get-Content -Encoding UTF8 docs\sdd\40399-…\commit-message.md | Select-Object -Skip 2 | Set-Clipboard
```

En Azure Repos: **New pull request** de la rama a `dev`. Título: la primera línea del mensaje.
Descripción: el resto (ya está en el portapapeles). Enlaza el work item `#40399`, añade revisores y,
al aprobarse, **Complete → Squash commit** comprobando que el mensaje conserva `Ref: #40399`.

#### 6 · Después del merge

```powershell
git fetch origin --prune
git switch dev; git merge --ff-only origin/dev
git branch -D feature/40399-seccion-ofertas      # -D: con squash, git no la ve como mezclada
```

El PO valida los criterios de aceptación en el entorno de `dev` (G4) y el work item avanza en
Azure DevOps a mano.

### 14.3 Commits de seguimiento

| Situación | Mensaje |
| --- | --- |
| Correcciones de QA después de mezclar | `fix(<ámbito>): corregir hallazgos de QA` · solo las correcciones · `Ref: #<id>` |
| Documentación después de mezclar | `docs(<ámbito>): documentar <qué>` · `Ref: #<id>` |
| Un bloque de `/document-project` | `docs(<ámbito>): documentar <áreas>` · `Ref: #<id del PBI de documentación>` |
| Instalar o actualizar el kit | `chore(sdd): instalar fi-sdd-standard v<versión>` / `actualizar … a v<versión>` |
| Contexto del proyecto | `chore(sdd): añadir el contexto del proyecto y la documentación base` |

### 14.4 Llevar el piloto a dev

Mientras se prueba, el kit puede vivir en una rama local (`chore/sdd-kit-piloto`). Para que el
equipo lo use, entra en `dev` con un PR como cualquier cambio:

```powershell
git fetch origin
git switch chore/sdd-kit-piloto
git merge origin/dev
python .agents\skills\project-context\scripts\check_project.py   # 0 errores
dotnet build <solución> --no-incremental; dotnet test <pruebas>
git switch -c chore/sdd-kit-en-dev
git push -u origin chore/sdd-kit-en-dev
python .agents\scripts\pr-check.py --base origin/dev
```

- **Entra:** `.agents/`, `.github/agents/`, `.github/prompts/`, `.claude/settings.json`,
  `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`, `sdd-guardrails.json` y `docs/`.
- **No entra:** `.claude/skills/`, `.claude/agents/` (copias locales), `.claude/settings.local.json`,
  `.github/copilot-instructions.md` y, de `docs/sdd/`, los `assets/`, `commit-message.md`,
  `test-cases.csv` y `_borradores/` (ADR-0027). Si alguno ya estaba versionado en el piloto,
  quítalo del índice antes del PR (capítulo 5, *Si el proyecto ya versionaba esos archivos*).
- **Squash**, con `chore(sdd): adoptar fi-sdd-standard v<versión> en <proyecto>`. Sin work item,
  el aviso de `pr-check.py` sobre `Ref:` es esperado.
- **Revisor:** el tech lead. Revisa a mano `sdd-guardrails.json`.

Mientras trabajas en la rama del piloto, el código de cada work item se lleva a una rama limpia
desde `dev` con *cherry-pick* para que su PR no arrastre archivos del kit (guía
`docs/guias/git-por-work-item.md`, variante B).

---

## 15. Recetas

Casos completos, de principio a fin, con lo que pides y lo que haces en cada momento. Úsalos como
lista de comprobación las primeras veces.

### 15.1 Un PBI de principio a fin

| # | Sesión | Tú haces o pides | Resultado | Tiempo orientativo |
| --- | --- | --- | --- | --- |
| 1 | — | Rama `feature/40399-…` desde `dev`; `new-sdd-item.py 40399 "<título>"`; copias el work item y las imágenes; `check-sdd-item.py` | `story.md` listo | 10 min |
| 2 | Nueva (Opus) | `/enrich-us 40399` · respondes o pasas las preguntas al PO · «sí» | `pbi.md` (G1) | 15–30 min |
| 3 | Nueva (Opus) | `/technical-analysis 40399` · «sí» · lees 03 y 04 · «Aprueba 03 y 04» | `00`–`06` (G2) | 20–40 min |
| 4 | Nueva (Sonnet) | `/wbs-execution 40399` · «sí» a cada tarea · resuelves bloqueos | Código, pruebas, `CHANGELOG.md`, `commit-message.md` | Según la WBS |
| 5 | **Nueva** (Opus) | `/qa-review 40399` · decides cada hallazgo | `qa-report.md` (G3) | 15–30 min |
| 6 | La de 4 u otra | Si hay «A corregir»: `/wbs-execution 40399 qa` | Correcciones | — |
| 7 | **Nueva** | `/qa-review 40399` (ronda 2) | Correcciones verificadas | 10 min |
| 8 | Nueva | `/document-code 40399` | Comentarios y `docs/` | 10–20 min |
| 9 | — | `git add <rutas>` · `git commit -F …/commit-message.md` · `pr-check.py` · push · PR | PR a `dev` (G4) | 10 min |

> [!TIP]
> **El work item es lo que se recuerda, no la conversación**
>
> Cada paso empieza en una sesión nueva porque todo lo necesario está en la carpeta. Si cierras el
> portátil a mitad, mañana basta con lanzar el mismo comando: la skill retoma desde los documentos.

### 15.2 Un bug pequeño por la vía rápida

1. Rama `fix/41020-…` desde `dev` y la carpeta con `--tipo bug`:
   ```powershell
   git switch -c fix/41020-redondeo-total origin/dev
   python <kit>\scripts\new-sdd-item.py 41020 "El total de la factura redondea mal los céntimos" --tipo bug
   ```
2. Copia en `story.md` la descripción, los **pasos para reproducir** y la información del sistema,
   y guarda las capturas en `assets/`.
3. Sesión nueva: `/quick-fix 41020`. Revisa la causa (`archivo:línea`) y la compuerta, y responde
   «sí».
4. Comprueba en el cierre la línea *Rojo → verde* de la prueba nueva.
5. Sesión **nueva**: `/qa-review 41020` (lee `fix-plan.md` como diseño y comprueba que el cambio no
   salió de la compuerta).
6. `/document-code 41020`, commit con el `git add` de la skill, `pr-check.py` y PR.

### 15.3 Un bug que no pasa la compuerta

`/quick-fix` responde `⛔ No es una corrección rápida — <criterio> · <evidencia>`. No es un
error: es la señal de que el bug necesita diseño.

1. Lee el motivo: suele ser una migración, un DTO compartido, un cambio de permisos o más de tres
   archivos.
2. Sigue el flujo completo en una sesión nueva: `/enrich-us 41077`. La causa ya encontrada está en
   `bitacora.md` y `enrich-us` la aprovecha.
3. Si crees que la compuerta se equivoca (por ejemplo, contó un archivo de pruebas como de
   producción), díselo con la evidencia; la IA revisa ese criterio, pero no lo fuerza.

### 15.4 QA prepara los casos antes de implementar

1. QA (o el dev) lanza `/enrich-us 40933 qa`: cada criterio sale clasificado *Definido*,
   *Deducción directa* o *A confirmar*, con su fuente y, si hace falta, una pregunta para el PO.
2. Las preguntas *A confirmar* van al PO. Mientras tanto, `/test-cases 40933` ya genera los casos:
   los de criterios confirmados en `Diseñado`, los demás `Bloqueado`.
3. QA revisa `test-cases.md` e importa `test-cases.csv` en Azure Test Plans.
4. Cuando el PO responde, se resuelve el marcador (capítulo 13) y se vuelve a lanzar
   `/test-cases 40933`: actualiza conservando IDs y desbloquea los casos.
5. En el paso 4, `qa-review` comprueba que cada caso de prioridad Alta tiene una prueba automática o
   una comprobación en ejecución.

### 15.5 Hallazgos de QA: dos rondas

1. `/qa-review <id>` en sesión nueva → `qa-report.md` con hallazgos `Abierto`.
2. Decides cada Alta y Media: «QA-01 A, QA-02 B asumido por Ana Pérez, QA-03 C».
   - A → `A corregir` · B → `Aceptado (riesgo asumido por …)` · C → `Borrador (_borradores/…)`;
     antes del PR, crea ese work item en Azure DevOps, pon su ID en el estado y borra el borrador.
3. `/wbs-execution <id> qa` (sesión de implementación o nueva, **nunca** la de QA): cada hallazgo
   es una pequeña tarea con su prueba primero; pone `Corregido (<fecha>)` y reescribe
   `commit-message.md`.
4. `/qa-review <id>` en otra sesión nueva: **ronda 2**, solo las correcciones. Pone
   `Corregido (verificado <fecha>)` o los devuelve a `Abierto`.
5. Lo que siga abierto tras la ronda 2 lo decides tú: no hay ronda 3.

### 15.6 Hace falta cambiar el diseño a mitad de la implementación

`wbs-execution` se para con un bloque *⚠️ Desviación de diseño*: qué sección de `03` no se puede
implementar, por qué, el ajuste mínimo y su impacto.

1. Si apruebas: «Apruebo el ajuste; actualiza 03 §3.4 y 04 §4.4, versión 1.1, aprobado por Ana
   Pérez».
2. La IA actualiza **primero** `03`/`04` (nueva versión y quién aprobó), lo registra en la bitácora
   y sigue con la tarea.
3. Si el ajuste cambia el alcance o un criterio, también pasa a `pbi.md` y genera un *Comentario
   para Azure DevOps* para el PO.

> [!WARNING]
> **Lo que no debes hacer**
>
> Pedirle que «lo haga como crea mejor» sin actualizar el diseño: `qa-review` revisa contra `03` y
> `04`, y encontraría el código fuera de contrato.

### 15.7 Retomar el trabajo otro día

- **A mitad de la WBS:** sesión nueva, `/wbs-execution <id>`. Lee la columna *Estado* de `05`,
  lista lo hecho y lo pendiente, **ejecuta build y pruebas antes de seguir** y, si la base no está
  limpia, te ofrece arreglar primero o revisar a mano lo que quedó a medias.
- **Empezar en una tarea concreta:** `/wbs-execution <id> from:T-04` (solo si sus dependencias están
  hechas).
- **Un subagente se quedó parado** (sin informe): la sesión mira `git status` y `git diff --stat`,
  anota en la bitácora lo hecho y lo que falta, y lo reanuda **una vez** con `Ya hecho / Falta`. Si
  se vuelve a parar, eliges: A) la sesión termina la tarea, B) se divide.

### 15.8 El PO cambia el work item a mitad

1. Actualiza `story.md` con el texto nuevo de Azure DevOps (sube la revisión en la cabecera) y anota
   el motivo en `bitacora.md`.
2. Antes de implementar: vuelve a lanzar `/enrich-us <id>` y elige sobrescribir `pbi.md`; luego
   `/technical-analysis <id>` (los documentos anteriores quedan en git).
3. Ya implementando: trátalo como un cambio de diseño (receta anterior). Si el cambio es grande,
   valora un work item nuevo en `_borradores/`.

### 15.9 Un work item sin criterios de aceptación

`story.md` dirá «Sin criterios de aceptación en el work item». `enrich-us` solo redacta criterios
que **reformulan** lo que ya dicen la descripción y los adjuntos (por ejemplo, el orden del menú
que muestra un mockup), marcados `Propuesto desde la descripción — validar con PO`. Todo lo demás
(otros roles, casos límite, qué pasa sin permiso) son preguntas. Lleva esas preguntas al PO y, a
ser posible, que añada los criterios en Azure DevOps.

### 15.10 Documentar un proyecto heredado

1. Kit instalado y `/project-context` hecho; `check_project.py` en 0 errores.
2. Pide al PO un PBI «Documentación inicial del proyecto» para enlazar los commits.
3. Rama `docs/document-project-plan`, sesión nueva: `/document-project`. Revisa la propuesta de
   áreas y bloques, aprueba, y haz el commit del plan con el primer bloque o aparte.
4. Por cada bloque: rama `docs/document-project-b01`, **sesión nueva**, `/document-project`, revisa
   el diff de comentarios (solo cambian comentarios), commit con el mensaje de `B-01.md`, PR.
5. Entre bloques, `/document-project status` muestra el avance, los hallazgos y los archivos que
   cambiaron después de documentarse.

### 15.11 Usar el kit en un proyecto que ya tenía su propia IA

Proyectos con un `CLAUDE.md` largo, skills propias o hooks en PowerShell:

1. `install.py` no toca nada de eso y marca `PENDIENTE`.
2. `/project-context` lo lee como fuente de conocimiento y propone, una línea por elemento:
   - el conocimiento de `CLAUDE.md` → a *Project context* o `docs/`, y `CLAUDE.md` → `@AGENTS.md`;
   - skills que el flujo sustituye (por ejemplo `/pbi` → `enrich-us`) → eliminar;
   - skills sin equivalente (por ejemplo, una que genera traducciones) → se mantienen y se citan en
     *Internationalization*;
   - hooks que el kit cubre (rutas protegidas, formato, patrones) → sus reglas a
     `sdd-guardrails.json` y se quitan de `.claude/settings.json`; los demás se mantienen.
3. Apruebas cada propuesta por separado.

---

## 16. Cómo hablarle a la IA

Las skills hacen la mayor parte del trabajo de redacción del prompt por ti. Aun así, cómo respondes
a sus confirmaciones y cómo pides lo que se sale del guion marca mucha diferencia en el resultado.

### 16.1 Reglas de oro

**Una skill, una sesión**

Abre una sesión nueva para cada paso grande. El contexto de la conversación anterior no hace falta
(está en los documentos) y una sesión limpia trabaja mejor. Para `qa-review` es obligatorio.

**El ID en la misma línea**

`/enrich-us 40399`, no `/enrich-us` y el ID en otro mensaje. En Copilot es la forma fiable de que
la skill lo encuentre.

**Responde a lo que pregunta**

Ante una confirmación, «sí» o la corrección concreta. Si corriges, la IA rehace el resumen y vuelve
a preguntar: no escribe hasta tu «sí».

**Di quién decidió**

«Lo confirmó Laura Gómez (PO) hoy». La IA lo registra con nombre y fecha en la bitácora y en el
documento, y lo pone en el comentario para Azure DevOps.

**Archivos, no pegados**

Para logs largos o salidas de comandos, da la ruta del archivo: la IA busca en él. Pegar cientos de
líneas en el chat consume contexto y empeora las respuestas.

**Corrige el origen**

Si `story.md` está mal, corrígelo tú (o en Azure DevOps). Si una regla del proyecto falta, va a
*Project context*. Si una skill se equivoca siempre igual, avisa al responsable del kit.

### 16.2 Responder a las confirmaciones

| La IA pregunta | Buena respuesta | Respuesta que da problemas |
| --- | --- | --- |
| ¿Es correcto el análisis? | «Sí» · «El rol es Jefe de ventas, no Supervisor; el resto bien» | «Más o menos» (no sabe qué cambiar) |
| ¿Qué roles ven la sección? `[PENDING-BUSINESS]` | «Comercial y Jefe de ventas; confirmado por Laura Gómez» · «No lo sé: déjalo pendiente, se lo pregunto al PO» | «Pon lo que veas lógico» (le pides que invente una regla) |
| A) Volver a technical-analysis · B) Continuar | «A» · «B, asumo el riesgo» | «Haz lo que sea más rápido» |
| ¿Empiezo con T-01? | «Sí» · «Sí, y T-02 y T-03 en paralelo» (si los propuso) | «Hazlas todas sin preguntar» (se salta la verificación por tarea) |
| QA-01: A) corregir · B) aceptar · C) aparte | «QA-01 A, QA-02 B asumido por Ana Pérez» | «Corrígelo tú» (qa-review no corrige código) |

### 16.3 Pedir cosas fuera del guion

La sesión sigue las reglas de `AGENTS.md` aunque no estés dentro de una skill. Algunos ejemplos
útiles:

**Explorar antes de crear un work item:**

```text
Usa code-explorer para averiguar dónde se calcula el total de la factura y qué pruebas lo cubren.
No propongas cambios.
```

**Revisar un documento:**

```text
Revisa 03-solution-proposal.md del 40399 contra pbi.md: ¿hay algún criterio sin SPEC en 04?
No edites nada; dame la lista.
```

**Aprobar el diseño:**

```text
Aprueba 03 y 04 del 40399: actualiza su línea Estado, aprobado por Ana Pérez hoy.
```

**Un borrador de work item:**

```text
Lo de los textos sin i18n en SideMenu.tsx no es de este work item: escríbelo como borrador en
_borradores para que lo cree el PO.
```

**Saber dónde estamos:**

```text
¿En qué paso está el 40399? Lee la carpeta y dime qué falta para el PR.
```

### 16.4 Lo que no hay que pedir

> [!CAUTION]
> **Peticiones que chocan con las reglas**
>
> - «Haz el commit y súbelo»: la IA no hace commit ni push (y en Claude Code está bloqueado). Te dará
>   los comandos.
> - «Lee el appsettings.Development.json para ver la cadena de conexión»: secretos bloqueados. Si
>   necesita un valor, dáselo tú sin pegar credenciales.
> - «Inventa unos criterios razonables»: los criterios y las reglas los decide el negocio.
> - «Traduce al francés como puedas»: sin seguridad, queda `[PENDING-TRANSLATION]`.
> - «Revisa tú mismo lo que acabas de implementar»: `qa-review` en otra sesión.
> - «Edita story.md para corregir la descripción»: `story.md` lo prepara una persona.
> - «Arregla de paso este otro bug»: va a `_borradores/`; un work item, un alcance.

### 16.5 Cuidar el contexto

- En Claude Code, `/context` muestra cuánto contexto lleva la sesión y `/compact` lo resume. En
  `wbs-execution` con muchas tareas, trabaja por bloques de 6.
- No pidas que imprima tablas enteras de nuevo: las skills escriben una línea de progreso por eso.
- Si la sesión empieza a confundirse (repite pasos, olvida decisiones), abre una nueva: los
  documentos tienen todo.

### 16.6 Elegir el modelo

| Paso | Modelo recomendado | Por qué |
| --- | --- | --- |
| `enrich-us`, `technical-analysis`, `project-context` | Razonamiento (Opus) | Análisis, síntesis, diseño |
| `wbs-execution`, `quick-fix`, `test-cases` | Sonnet | Ciclos rápidos y trabajo estructurado; los subagentes hacen el código |
| `qa-review` | Razonamiento (en Copilot, elígelo tú) | El valor del paso es un revisor fuerte y fresco |
| `document-code`, `document-project` | Cualquiera | `doc-writer` escribe; la sesión decide qué |

En Claude Code, `/model` cambia el modelo de la sesión; las skills con modelo fijado lo usan
igualmente. En Copilot se elige en el selector del chat.

---

## 17. Solución de problemas

Los problemas más frecuentes de los pilotos, con su causa y su arreglo. Casi todos son del entorno
(Windows, codificación, git) y no del flujo.

### 17.1 Instalación y carga

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `/` no muestra las skills | La herramienta se abrió antes de instalar | Cierra y vuelve a abrir. En Claude Code, comprueba `.claude/skills/`; en VS Code, `.agents/skills/` |
| Faltan los subagentes en Claude Code | Solo se instaló `--tools copilot` | `install.py --tools copilot,claude` |
| `CONFLICTO … ya existe y no es del kit` | Un archivo del proyecto se llama como uno del kit | Decide cuál se queda; el instalador no lo toca |
| `UnicodeDecodeError` al instalar | Cachés de Python (`__pycache__`, `.pyc`) en una versión antigua del kit | Usa la v0.11.0 o posterior, o borra las carpetas `__pycache__` del kit |
| VS Code carga las reglas dos veces | Lee `AGENTS.md` y `.github/copilot-instructions.md` | En `.vscode/settings.json`: `"github.copilot.chat.codeGeneration.useInstructionFiles": false` |
| `REVISAR .gitignore ignora .claude/settings.json` | El proyecto ignora `.claude/` entero | Añade `!.claude/settings.json` al final de `.gitignore` |
| La IA responde en inglés | Sesión anterior a la regla de idioma, o `AGENTS.md` sin el bloque del kit | Reinstala; la regla está en el bloque del kit. Puedes pedir «responde en español» |

### 17.2 Skills

| Síntoma | Causa | Solución |
| --- | --- | --- |
| La skill pide el ID aunque lo escribiste | Copilot no sustituye `$ARGUMENTS` y el ID iba en otro mensaje | Escribe `/skill <id>` en una sola línea |
| *Varias carpetas coinciden* | Hay dos carpetas con el mismo ID (por ejemplo, una antigua `docs/<sprint>/<item>`) | Responde cuál; las antiguas no se mueven |
| `technical-analysis` se para por pendientes | `pbi.md` tiene `[PENDING-BUSINESS]` | Resuélvelos (recomendado) o responde B |
| `wbs-execution` no avanza: *la base no está limpia* | Build o pruebas fallan al reanudar | A) arreglar primero · B) revisar a mano lo que quedó |
| *⛔ qa-review must run in a new session* | Lanzaste `qa-review` donde implementaste | Abre una sesión nueva |
| `document-project` se para: *uncommitted changes* | El árbol no está limpio | Commit o descarta lo anterior: un bloque empieza limpio |
| `comment_only.py`: *no es comentario* | `doc-writer` cambió algo más (un `using`, un espacio, el formato) | La skill lo devuelve a `doc-writer`; no lo parchees a mano. Para descartar: `comment_only.py restore` |
| La IA usa un *worktree* | Se le ocurrió para comparar builds | No hace falta: `doc_coverage.py --warnings --compare avisos.md`. Pídele que no use worktrees |

### 17.3 Git

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `nothing added to commit` | Faltó el `git add`, o los archivos nuevos (`??`) no se añadieron | `git add <rutas exactas>` y `git status --short` antes del commit |
| `git add` de la carpeta no añade `assets/` ni `commit-message.md` | Es intencionado: están en `.gitignore` (ADR-0027) | Nada. `git commit -F` lee `commit-message.md` del disco igualmente |
| `pr-check.py`: *secretos en el diff — .agents/scripts/pr-check.py (firma SAS)* | Falso positivo de la v0.12.0: el patrón se encontraba a sí mismo cuando el kit se instala en la misma rama | Actualiza el kit a la v0.12.1 o posterior y haz el commit `chore(sdd)` de la actualización |
| `pr-check.py`: *borradores* | La rama tiene un archivo en `docs/sdd/_borradores/` | Crea el work item en Azure DevOps, anota su ID donde se citaba el borrador y bórralo |
| `check-sdd-item.py`: *… no está en este equipo* | Retomas un work item en otro equipo y los adjuntos no se versionan | Bájalos del work item en Azure DevOps a `assets/` con los nombres que enlaza `story.md` |
| `install.py`: *REVISAR … archivos versionados que ya no se versionan* | El proyecto subía esos archivos antes de la v0.12.0 | `git rm -r --cached` de esas rutas (capítulo 5) y un commit `chore(sdd)` |
| `?? .agents/scripts/__pycache__/` | `pr-check.py` de la v0.11.0 dejaba cachés de Python | Bórrala; desde la v0.12.0 no se crea y está en `.gitignore` |
| `Already up to date` al hacer merge de `dev` | No hiciste `git fetch` antes | `git fetch origin` y luego `git merge origin/dev` |
| Varios commits en la rama | Commits intermedios | Antes del push: `git reset --soft origin/dev` y un commit con `-F` |
| El work item se cerró solo al mezclar | Un `fix #id` en el mensaje | Reábrelo a mano; usa siempre `Ref: #id`. `pr-check.py` lo detecta antes |
| `warning: LF will be replaced by CRLF` | Finales de línea en Windows | Inofensivo. No cambies `core.autocrlf` por esto |
| `git branch -d` no borra la rama tras el PR | El squash cambia los commits | `git branch -D <rama>` (seguro con el PR completado) |
| `pr-check.py`: *archivos del kit cambiados a mano* | Editaste una skill instalada, o actualizaste el kit sin `chore(sdd)` | Revierte el cambio y hazlo en el kit, o haz la actualización con su commit `chore(sdd)` |

### 17.4 Codificación y consola en Windows

| Síntoma | Causa | Solución |
| --- | --- | --- |
| Tildes rotas (`Ã©`, `├®`) al ver un archivo en PowerShell | PowerShell 5.1 lee UTF-8 sin BOM como ANSI | `Get-Content -Encoding UTF8 <archivo>`. El archivo está bien |
| `├®` en la salida de un script | Solo es la consola | Nada; o `chcp 65001` antes de ejecutar |
| Tildes rotas en un mensaje guardado con `>` | El `>` de PowerShell 5.1 escribe en UTF-16/ANSI | `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"` |
| Un archivo dejó de ser UTF-8 | Otro editor lo guardó en ANSI | `python .agents\scripts\check-encoding.py --fix` |

### 17.5 Hooks y permisos (Claude Code)

| Síntoma | Causa | Solución |
| --- | --- | --- |
| El hook no bloquea nada | La herramienta no se reinició, `python` no está en el PATH o `.claude/settings.json` no se cargó | Reinicia; pruébalo a mano como en el capítulo 12 (*Probarlo a mano*) y comprueba que `$LASTEXITCODE` es 2 |
| Bloquea un archivo que necesitas leer | Coincide con `secrets` | Si de verdad no tiene secretos (una plantilla), añádelo a `secretsAllowed` con motivo en el PR |
| Aviso de patrón que no aplica | El patrón es demasiado amplio | Ajusta el `glob` o la expresión en `sdd-guardrails.json` |
| El formateador falla en cada edición | Comando de `format` no instalado | Quítalo de `format` o instala la herramienta (`dotnet tool restore`) |
| Te pide permiso para `git commit` y lo deniega | Es intencionado: está en `deny` | Haz el commit tú en la terminal |

### 17.6 Builds y avisos

| Síntoma | Causa | Solución |
| --- | --- | --- |
| El número de avisos no cuadra (226 frente a 222) | MSBuild cuenta dos veces algunos `NU1902/NU1903`, o el build fue incremental | Compara con `doc_coverage.py --warnings … --compare`: quita duplicados y aparta los `NU19xx` |
| «0 avisos nuevos» sospechoso | Build incremental: se saltó proyectos | `dotnet build <solución> --no-incremental` |
| Avisos `NU19xx` cambian sin tocar nada | Dependen de la base de avisos de seguridad de NuGet, no del código | Se listan aparte y no cuentan como nuevos |
| CS1570–CS1587 tras documentar | Un comentario XML mal formado | La skill lo devuelve a `doc-writer` |

> [!NOTE]
> **Cuando nada de esto encaja**
>
> Guarda la salida en un archivo, anota la versión del kit (`.sdd-kit.json`), la herramienta y el
> modelo, y avisa al responsable del kit. Si la skill se equivocó, el arreglo va al kit para todos,
> nunca a la copia instalada.

---

## 18. Referencia rápida

Todo lo esencial en un par de páginas. Imprímelas o tenlas a mano las primeras semanas.

### 18.1 Comandos de las skills

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

### 18.2 Comandos de terminal

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

### 18.3 Compuertas

| | Cuándo | Decides |
| --- | --- | --- |
| **G1** | Fin del análisis de `enrich-us` | Si el resumen del work item es correcto |
| **G2** | Tras `technical-analysis` | Aprobar `03` y `04` (contrato) |
| **G3** | Tras `qa-review` | Corregir, aceptar o separar cada hallazgo |
| **G4** | PR a `dev` | Aprobar el código; el PO valida los criterios |

### 18.4 Límites de los bucles

| Bucle | Límite |
| --- | --- |
| Un subagente con la misma comprobación fallando | 3 intentos |
| Verificación de la sesión → vuelta al subagente | 2 rondas |
| Subagente parado sin informe | 1 reanudación |
| Rondas de QA | 2 |
| `doc-writer` con cambios que no son comentarios | 2 rondas |
| Tareas seguidas en una sesión de `wbs-execution` | Bloques de 6 |

### 18.5 La compuerta de quick-fix

Causa con `archivo:línea` · ≤ 3 archivos de producción de una capa · sin migración ni entidad · sin
cambio de contrato · sin cambio de autorización · sin `[PENDING-BUSINESS]` · textos nuevos con
todas sus traducciones · sin paquetes nuevos ni actualizados.

### 18.6 Marcadores

| Marcador | Falta |
| --- | --- |
| `[PENDING-BUSINESS: pregunta]` | Información de negocio |
| `[REQUIRES-VALIDATION: motivo]` | Evidencia técnica |
| `[ASSUMPTION-BASED: campo]` | Un campo del que depende la sección |
| `[PENDING-TRANSLATION: clave → idioma]` | Una traducción |

### 18.7 Commit

```text
tipo(ámbito): descripción en imperativo, minúscula, ≤ 72 caracteres

PBI-<id> — [MÓDULO] Título del work item

**Problema** · **Causa** (solo fix) · **Cambios** · **Alcance y no regresión** · **Pruebas**

Ref: #<id>
```

Nunca `fix #id` · nunca `Co-Authored-By` · < 4000 caracteres · un commit por work item ·
`git add` con rutas exactas.

### 18.8 Qué no se versiona (ADR-0027)

De cada work item: `assets/` (los adjuntos están en Azure DevOps), `commit-message.md` (queda en el
commit y en el PR) y `test-cases.csv` (se regenera). Tampoco los borradores de
`docs/sdd/_borradores/` (se crean en Azure DevOps y se borran antes del PR), ni `.claude/skills/`,
`.claude/agents/`, `.claude/settings.local.json` o `.github/copilot-instructions.md`.

### 18.9 Lo que la IA nunca hace

- Commit, push, merge ni cambiar de rama sin que lo pidas.
- Leer o mostrar secretos.
- Editar rutas protegidas o `story.md`.
- Inventar reglas, criterios, límites o traducciones.

- Revisar en la misma sesión lo que implementó.
- Cambiar `03`/`04` aprobados sin tu aprobación.
- Arreglar de paso algo fuera del work item.
- Decir que algo se ejecutó si no se ejecutó.

---

## Anexo · Decisiones del estándar (ADR)

Cada regla del kit tiene detrás una decisión registrada en `docs/adr/` del repositorio del kit. Si
te preguntas por qué algo funciona así, el ADR lo explica: contexto, decisión, consecuencias y
alternativas descartadas.

### A.1 Índice de ADR

| ADR | Decisión | Estado |
| --- | --- | --- |
| 0001 | Registrar las decisiones con ADR | Aceptada |
| 0002 | Azure DevOps es la fuente del requisito; todo el trabajo SDD en `docs/sdd/<id>-<título>/`, versionado | Sustituida en parte por 0027 |
| 0003 | Español para documentación, comentarios y commits; inglés para instrucciones internas | Aceptada |
| 0004 | Formato de commit: `.gitmessage` de Bonis | Aceptada |
| 0005 | Herramientas soportadas y rutas de cada una | Aceptada |
| 0006 | Ramas y despliegue | Aceptada |
| 0007 | `story.md` con el texto pegado es la entrada de `enrich-us` | Sustituida por 0015 |
| 0008 | MCP de Azure DevOps en solo lectura, tras una prueba | Propuesta |
| 0009 | IA dentro del pipeline con Fi Apps | Aceptada |
| 0010 | Responsable y pilotos | Aceptada |
| 0011 | Fuente única y adaptadores generados, sin enlaces simbólicos | Aceptada |
| 0012 | Reglas obligatorias en pruebas y pipeline | Aceptada |
| 0013 | Subagentes y skills de la sesión principal | Aceptada |
| 0014 | Reglas de optimización de tokens | Aceptada |
| 0015 | `story.md` lo prepara la persona, con sus adjuntos en `assets/` | Aceptada |
| 0016 | Ajustes del flujo tras el primer piloto en Bonis | Aceptada |
| 0017 | Adaptadores de agentes: `.github/agents/` versionado y `.claude/agents/` local | Aceptada |
| 0018 | `wbs-execution` delega cada tarea en el agente de su capa, con bucles limitados | Aceptada |
| 0019 | Revisión de QA independiente antes del PR, con `qa-review` | Aceptada |
| 0020 | Documentación del código con `document-code`, solo comentarios y `docs/` | Aceptada |
| 0021 | `/project-context`: contexto del proyecto, documentación base y pruebas desde el inicio | Aceptada |
| 0022 | `/document-project`: documentación inicial y completa del proyecto | Aceptada |
| 0023 | Guardarraíles: permisos `deny`, hook `sdd_guard.py`, pruebas de arquitectura y `pr-check.py`, con la matriz regla → comprobación | Aceptada |
| 0024 | Vía rápida para bugs pequeños con `quick-fix` y su compuerta | Aceptada |
| 0025 | Modo QA de `enrich-us` y skill `test-cases`, con CSV para Azure Test Plans | Aceptada |
| 0026 | El bucle de pipeline en rojo pasa a la fase 4 | Aceptada |
| 0027 | Qué se versiona en un proyecto con el kit: fuera `assets/`, `commit-message.md`, `test-cases.csv` y los borradores | Aceptada |

### A.2 Las que más afectan al día a día

| ADR | Qué significa para ti |
| --- | --- |
| 0002 | Todo el trabajo de un work item vive en `docs/sdd/<id>-<título>/`; qué se versiona, en 0027 |
| 0003 | Documentos, comentarios y commits en español |
| 0004 | Un commit por work item, `Ref: #id`, nunca `fix #id`, sin firma de IA |
| 0006 | Rama `feature/<id>-…` o `fix/<id>-…` desde `dev`, PR a `dev` con squash |
| 0013 | Las skills que piden confirmación corren en tu sesión; el trabajo acotado, en subagentes |
| 0015 | `story.md` lo preparas tú, con los adjuntos en `assets/` |
| 0018 | `wbs-execution` delega cada tarea en el subagente de su capa, con bucles limitados |
| 0019 | `qa-review` siempre en una sesión independiente, antes del PR |
| 0021 | `/project-context` antes del primer work item: contexto, `docs/` y pruebas |
| 0023 | Guardarraíles: cada regla obligatoria con su comprobación |
| 0024 | Vía rápida para bugs pequeños con su compuerta |
| 0025 | Modo QA de `enrich-us` y `test-cases` con CSV para Test Plans |
| 0027 | Qué se versiona: fuera `assets/`, `commit-message.md`, `test-cases.csv` y los borradores |

### A.3 Proponer un cambio al kit

1. Rama desde `main` en el repositorio del kit; un cambio por rama.
2. Si cambia una regla o un comportamiento, un ADR nuevo (o uno que sustituya a otro).
3. Los cambios se hacen en `core/`, nunca en las copias instaladas.
4. `python scripts/validate.py` sin errores y una entrada en `CHANGELOG.md`.
5. Commit según `.gitmessage`.

---

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
y aparta los `NU19xx` de NuGet. (11.10, 17.6)
