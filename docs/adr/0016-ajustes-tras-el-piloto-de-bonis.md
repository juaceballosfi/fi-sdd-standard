# ADR-0016 · Ajustes del flujo tras el primer piloto en Bonis

- **Estado:** Aceptada
- **Fecha:** 2026-10-14
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002, ADR-0014, ADR-0015

## Contexto

El primer piloto completo (Bonis, PBI 40944) funcionó de principio a fin, pero dejó a la vista
cinco carencias. El detalle está en `tests/pilots/bonis/RESULTADOS-40944.md`.

- El análisis técnico usó 551k tokens de contexto, sobre todo por un log de CI pegado en el chat.
- El PBI amplió su alcance en `technical-analysis` y el contrato (`pbi.md`) se cambió sin una regla
  que lo regulara.
- Las decisiones quedaron en el repositorio pero no en Azure DevOps.
- La IA creó una carpeta de borradores de work items sin que existiera convención.
- La bitácora se desordenó: hubo una sección nueva y un hallazgo contradicho sin corregir.

## Decisión

Las convenciones compartidas de los skills (v3.2) añaden:

1. **Entradas grandes:** primero se busca; de archivos grandes se leen solo los rangos necesarios;
   los logs se piden como archivo y nunca se pegan en el chat. También en `AGENTS.base.md`.
2. **Decisiones a Azure DevOps:** cada paso que confirma decisiones termina con un bloque
   «Comentario para Azure DevOps» listo para pegar. La IA solo lo publica si el MCP tiene escritura
   habilitada y la persona lo pide.
3. **Hallazgos fuera de alcance:** se escriben como propuesta en `docs/sdd/_borradores/<slug>.md`,
   nunca como `story.md`. Una persona crea el work item.
4. **Bitácora:** una línea por entrada en *Registro*, hallazgos en *Hallazgos*, sin secciones
   nuevas. Un hallazgo equivocado se corrige con otro, sin borrarlo.

Además, `technical-analysis` debe preguntar si el trabajo extra va en el mismo work item o en otro.
Si entra, actualiza `pbi.md` con la línea «Actualizado con» y registra quién lo aprobó. Sin la
aprobación del PO queda como `[PENDING-BUSINESS]`.

## Consecuencias

- Menos contexto por paso y sesiones más baratas.
- El work item de Azure DevOps refleja el alcance real, aunque la persona tenga que pegar el
  comentario.
- `docs/sdd/_borradores/` se versiona junto al resto. Cada borrador se borra cuando su work item
  existe y tiene carpeta propia.

## Alternativas consideradas

- Prohibir ampliar el alcance en `technical-analysis`: demasiado rígido. A veces la deuda está
  justo en la zona que se toca y conviene resolverla en el mismo cambio.
- Publicar las decisiones en Azure DevOps de forma automática: requiere el MCP con escritura, que
  aún no está aprobado (ADR-0008).
