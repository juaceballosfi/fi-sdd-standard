# ADR-0004 · Formato de commit: el `.gitmessage` de Bonis

- **Estado:** Aceptada (ampliada el 2026-10-14)
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

Cada proyecto escribía los commits a su manera. Bonis tiene un `.gitmessage` probado que se
reutiliza como descripción del PR y evita cerrar work items sin querer.

## Decisión

Todos los proyectos siguen `core/templates/.gitmessage`:

- Primera línea `tipo(ámbito): descripción`, en minúscula, sin punto final, 72 caracteres como máximo.
- Línea de título `BUG-XXXXX / PBI-XXXXX — [MÓDULO] Título del ticket`.
- Bloques en negrita: **Problema**, **Causa** (solo en fix), **Cambios**, **Alcance y no regresión**, **Pruebas**.
- Sin encabezados Markdown (git borra las líneas que empiezan por `#`).
- Mensaje completo de menos de 4000 caracteres.
- `Ref: #12345` para enlazar el work item; nunca `fix`, `fixes` o `fixed` delante del número.
- **Un commit por work item** (decisión del 2026-10-14, tras el piloto de Bonis), aunque el WBS
  tenga varias tareas. Incluye el código y la carpeta `docs/sdd/<id>-<título>/`.
- **Sin firma de IA en el commit** (decisión del 2026-10-14): ni `Co-Authored-By` ni otros
  trailers. La evidencia de que se trabajó con IA es el sello «Generado con» de los documentos
  SDD, que viajan en el mismo commit.

## Consecuencias

- El skill `commit-message` rellena este formato en `docs/sdd/<id>-<título>/commit-message.md`.
- La validación del PR comprueba el formato con un script, sin IA.
- Se recomienda *squash merge* para que el mensaje final sea la descripción del PR.

## Alternativas consideradas

- Conventional Commits sin cuerpo estructurado: pierde Problema, Causa y Pruebas.
- Un commit por tarea del WBS: separa mejor una refactorización grande, pero multiplica los
  mensajes y no encaja con el *squash merge*. Si una tarea es muy grande, mejor otro work item.
- Trailer `Co-Authored-By` en cada commit hecho con IA: redundante con el sello y depende de la
  herramienta.
