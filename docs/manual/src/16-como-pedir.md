# Cómo hablarle a la IA

:::lead
Las skills hacen la mayor parte del trabajo de redacción del prompt por ti. Aun así, cómo respondes
a sus confirmaciones y cómo pides lo que se sale del guion marca mucha diferencia en el resultado.
:::

## Reglas de oro

:::grid2
:::tile-accent Una skill, una sesión
Abre una sesión nueva para cada paso grande. El contexto de la conversación anterior no hace falta
(está en los documentos) y una sesión limpia trabaja mejor. Para `qa-review` es obligatorio.
:::
:::tile-accent El ID en la misma línea
`/enrich-us 40399`, no `/enrich-us` y el ID en otro mensaje. En Copilot es la forma fiable de que
la skill lo encuentre.
:::
:::tile-accent Responde a lo que pregunta
Ante una confirmación, «sí» o la corrección concreta. Si corriges, la IA rehace el resumen y vuelve
a preguntar: no escribe hasta tu «sí».
:::
:::tile-accent Di quién decidió
«Lo confirmó Laura Gómez (PO) hoy». La IA lo registra con nombre y fecha en la bitácora y en el
documento, y lo pone en el comentario para Azure DevOps.
:::
:::tile-accent Archivos, no pegados
Para logs largos o salidas de comandos, da la ruta del archivo: la IA busca en él. Pegar cientos de
líneas en el chat consume contexto y empeora las respuestas.
:::
:::tile-accent Corrige el origen
Si `story.md` está mal, corrígelo tú (o en Azure DevOps). Si una regla del proyecto falta, va a
*Project context*. Si una skill se equivoca siempre igual, avisa al responsable del kit.
:::
:::

## Responder a las confirmaciones

| La IA pregunta | Buena respuesta | Respuesta que da problemas |
| --- | --- | --- |
| ¿Es correcto el análisis? | «Sí» · «El rol es Jefe de ventas, no Supervisor; el resto bien» | «Más o menos» (no sabe qué cambiar) |
| ¿Qué roles ven la sección? `[PENDING-BUSINESS]` | «Comercial y Jefe de ventas; confirmado por Laura Gómez» · «No lo sé: déjalo pendiente, se lo pregunto al PO» | «Pon lo que veas lógico» (le pides que invente una regla) |
| A) Volver a technical-analysis · B) Continuar | «A» · «B, asumo el riesgo» | «Haz lo que sea más rápido» |
| ¿Empiezo con T-01? | «Sí» · «Sí, y T-02 y T-03 en paralelo» (si los propuso) | «Hazlas todas sin preguntar» (se salta la verificación por tarea) |
| QA-01: A) corregir · B) aceptar · C) aparte | «QA-01 A, QA-02 B asumido por Ana Pérez» | «Corrígelo tú» (qa-review no corrige código) |

## Pedir cosas fuera del guion

La sesión sigue las reglas de `AGENTS.md` aunque no estés dentro de una skill. Algunos ejemplos
útiles:

:::ask Explorar antes de crear un work item
Usa code-explorer para averiguar dónde se calcula el total de la factura y qué pruebas lo cubren.
No propongas cambios.
:::

:::ask Revisar un documento
Revisa 03-solution-proposal.md del 40399 contra pbi.md: ¿hay algún criterio sin SPEC en 04?
No edites nada; dame la lista.
:::

:::ask Aprobar el diseño
Aprueba 03 y 04 del 40399: actualiza su línea Estado, aprobado por Ana Pérez hoy.
:::

:::ask Un borrador de work item
Lo de los textos sin i18n en SideMenu.tsx no es de este work item: escríbelo como borrador en
_borradores para que lo cree el PO.
:::

:::ask Saber dónde estamos
¿En qué paso está el 40399? Lee la carpeta y dime qué falta para el PR.
:::

## Lo que no hay que pedir

:::danger Peticiones que chocan con las reglas
- «Haz el commit y súbelo»: la IA no hace commit ni push (y en Claude Code está bloqueado). Te dará
  los comandos.
- «Lee el appsettings.Development.json para ver la cadena de conexión»: secretos bloqueados. Si
  necesita un valor, dáselo tú sin pegar credenciales.
- «Inventa unos criterios razonables»: los criterios y las reglas los decide el negocio.
- «Traduce al francés como puedas»: sin seguridad, queda `[PENDING-TRANSLATION]`.
- «Revisa tú mismo lo que acabas de implementar»: `qa-review` en otra sesión.
- «Edita story.md para corregir la descripción»: `story.md` lo prepara una persona.
- «Arregla de paso este otro bug»: va a `_borradores/`; un work item, un alcance.
:::

## Cuidar el contexto

- En Claude Code, `/context` muestra cuánto contexto lleva la sesión y `/compact` lo resume. En
  `wbs-execution` con muchas tareas, trabaja por bloques de 6.
- No pidas que imprima tablas enteras de nuevo: las skills escriben una línea de progreso por eso.
- Si la sesión empieza a confundirse (repite pasos, olvida decisiones), abre una nueva: los
  documentos tienen todo.

## Elegir el modelo

| Paso | Modelo recomendado | Por qué |
| --- | --- | --- |
| `enrich-us`, `technical-analysis`, `project-context` | Razonamiento (Opus) | Análisis, síntesis, diseño |
| `wbs-execution`, `quick-fix`, `test-cases` | Sonnet | Ciclos rápidos y trabajo estructurado; los subagentes hacen el código |
| `qa-review` | Razonamiento (en Copilot, elígelo tú) | El valor del paso es un revisor fuerte y fresco |
| `document-code`, `document-project` | Cualquiera | `doc-writer` escribe; la sesión decide qué |

En Claude Code, `/model` cambia el modelo de la sesión; las skills con modelo fijado lo usan
igualmente. En Copilot se elige en el selector del chat.
