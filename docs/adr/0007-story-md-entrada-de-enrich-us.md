# ADR-0007 · `story.md` con el texto pegado es la entrada de `enrich-us`

- **Estado:** Sustituida por ADR-0015 (2026-10-14)
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002, ADR-0008, ADR-0015

## Contexto

El MCP de Azure DevOps aún no está aprobado ni probado. El flujo necesita una entrada que
funcione hoy en todas las herramientas.

## Decisión

El paso 0 de `enrich-us` crea `docs/sdd/<id>-<título>/story.md` a partir del texto del work item
que pega la persona, con el formato de `core/skills/enrich-us/templates/story.md`. El texto se copia literal; si
falta un campo, se escribe «No incluido en el texto pegado». Cuando se adopte el MCP, el formato
de `story.md` será el mismo, así que el resto del flujo no cambia.

## Consecuencias

- El flujo funciona sin conectar nada.
- El texto pegado sigue siendo la alternativa permanente aunque se adopte el MCP.

## Alternativas consideradas

- Esperar al MCP para empezar: retrasa todo el flujo por una pieza opcional.
