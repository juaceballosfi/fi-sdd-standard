# ADR-0015 · `story.md` lo prepara la persona, con sus adjuntos en `assets/`

- **Estado:** Aceptada
- **Fecha:** 2026-10-14
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002, ADR-0007 (la sustituye), ADR-0008

## Contexto

Con ADR-0007, `enrich-us` escribía `story.md` a partir del texto pegado en el chat. En la
preparación del piloto de Bonis (PBI 40944) aparecieron tres problemas:

- Los work items llevan imágenes y archivos (maquetas, capturas del error) que a menudo son el
  requisito real. Pegados en el chat, no todas las herramientas los guardan en disco, y el paso
  siguiente ya no los ve.
- Si la IA escribe la «copia literal», nadie comprueba que lo sea.
- Pedir la carpeta a mano o a la IA generaba dudas sobre quién crea qué.

## Decisión

`story.md` es la entrada del flujo y **lo prepara una persona**: copia el work item de Azure
DevOps en `docs/sdd/<id>-<título>/story.md` y guarda sus imágenes y archivos en `assets/`, con
nombre descriptivo, enlazados y descritos en una línea. Lo firma con `**Preparado por:**`, no con
el sello «Generado con». La IA lo lee con sus adjuntos y nunca lo edita.

- `scripts/new-sdd-item.py <id> "<título>"` crea la carpeta con el nombre correcto, `story.md`
  con el encabezado prerrellenado, `assets/` y `bitacora.md`.
- Si no hay `story.md`, `enrich-us` se detiene y explica cómo prepararlo. Como alternativa puede
  crear la carpeta vacía o escribir `story.md` con el texto pegado; en ambos casos la persona lo
  revisa antes de seguir.
- `check-sdd-item.py` comprueba sin IA que `story.md` está completo: encabezado sin `<…>`,
  enlaces a `assets/` que existen, imágenes con texto alternativo útil y archivos de `assets/`
  enlazados.
- Si el work item no tiene criterios de aceptación, se escribe «Sin criterios de aceptación en el
  work item». `enrich-us` solo propone los que repiten de forma comprobable lo que dicen la
  descripción y los adjuntos, marcados para validar con el PO.
- Lo que haga falta de otro work item (por ejemplo, «Copied from #40942») lo copia la persona en
  `story.md`; la IA no lo busca por su cuenta.
- Cuando se adopte el MCP de Azure DevOps (ADR-0008), podrá rellenar `story.md`, pero la persona
  lo revisa y lo firma igual.

## Consecuencias

- La persona dedica unos minutos más por work item, pero la entrada es verificable y conserva las
  imágenes en el repositorio.
- Funciona igual en Claude Code, Copilot y Codex: no depende de que la herramienta guarde lo que
  se pega en el chat.
- Las herramientas que no pueden abrir imágenes trabajan con la descripción de cada adjunto.
- `story.md` y `assets/` se versionan; no deben llevar credenciales ni datos personales de clientes.
- Skills v3.1 y kit v0.3.0.

## Alternativas consideradas

- Mantener ADR-0007 (la IA escribe `story.md` desde el chat): pierde los adjuntos en algunas
  herramientas y nadie verifica la copia. Queda como alternativa dentro de `enrich-us`.
- Esperar al MCP: sigue sin probarse (ADR-0008) y tampoco evitaría la revisión de la persona.
