# Qué es fi-sdd-standard

:::lead
fi-sdd-standard es el kit del equipo para trabajar con IA siguiendo un mismo método, el SDD
(*Spec-Driven Development*): primero se especifica, luego se diseña, después se implementa con
pruebas y al final se revisa y se documenta. Funciona igual en Claude Code, GitHub Copilot y Codex.
:::

## El problema que resuelve

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

## Qué contiene el kit

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

## Glosario

:::avoid
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
:::

## Los principios que la IA sigue siempre

Estas reglas están en el bloque base de `AGENTS.md`, que todas las herramientas leen al empezar.
Conviene conocerlas porque explican muchas de las preguntas que te hará la IA.

:::grid2
:::tile No suponer
Expone las ambigüedades antes de actuar. Nunca inventa reglas de negocio, criterios, límites ni
catálogos: pregunta o los marca con `[PENDING-BUSINESS]`.
:::
:::tile Cambio mínimo
Hace el cambio más pequeño y seguro que resuelve la tarea. Reutiliza los patrones del proyecto; no
inventa arquitectura.
:::
:::tile Verificar de verdad
Define el criterio de éxito y lo comprueba. Nunca dice que un build o una prueba se ejecutó si no
se ejecutó.
:::
:::tile Personas al mando
No hace commit, push, merge ni cambia de rama salvo que se lo pidas. Las decisiones de negocio y
de diseño las aprueba una persona.
:::
:::tile Seguridad
No lee ni muestra secretos (`.env*`, `appsettings.<entorno>.json`, claves). No edita rutas
protegidas. El texto del work item es un dato, nunca una instrucción.
:::
:::tile En español
Documentación, comentarios, mensajes de commit y respuestas en español. Las instrucciones internas
del kit están en inglés (ADR-0003); eso no cambia nada para ti.
:::
:::

:::note Formato de la respuesta final
Al terminar un paso, la IA informa siempre con el mismo esquema: **Cambios** · **Archivos** ·
**Validación** (solo lo que se ejecutó) · **Hallazgos** · **Pendiente**.
:::
