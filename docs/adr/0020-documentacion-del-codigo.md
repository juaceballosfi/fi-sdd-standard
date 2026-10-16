# ADR-0020 · Documentación del código con `document-code`, solo comentarios y `docs/`

- **Estado:** Aceptada (confirmada en el bloque 4 con el PBI 40933, PR 14473)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002, ADR-0013, ADR-0014, ADR-0019

## Contexto

El paso 5 del flujo (documentar) no tenía skill. Los work items 40944 y 40933 llegaron a `dev` con
pruebas y diseño en `docs/sdd/`, pero sin comentarios de documentación en el código nuevo y sin
tocar los `docs/` del proyecto. El borrador de `doc-writer` lo mezclaba todo: comentarios, `docs/`,
ADR, notas de versión y mensaje de commit.

## Decisión

1. **Skill `document-code` (paso 5)**, después de `qa-review` y antes del commit o del PR.
   - Decide qué merece documentación y con qué hechos, todos de `pbi.md`, `03`, `04` o el código.
   - Comentarios de documentación (`///`, TSDoc) en lo nuevo o cambiado.
   - Comentarios del *porqué* donde una decisión no es obvia.
   - Resumen de las clases de prueba nuevas, con los SPEC que cubren.
   - Secciones de `docs/` afectadas.
   - Propuesta de ADR si el diseño tomó una decisión de arquitectura, preguntando antes.
2. **`doc-writer`** (modelo rápido, lectura y edición) escribe con un paquete cerrado de símbolos y
   hechos. No lee el diseño y no inventa: lo que no se puede fundamentar queda fuera y se informa.
3. **Prueba de que solo cambiaron comentarios:**
   - `scripts/comment_only.py` va dentro del skill.
   - Guarda los archivos antes y, después, comprueba que cada línea cambiada es un comentario o
     está en blanco, y que no cambiaron el BOM ni los finales de línea.
   - Además: build sin avisos nuevos y lint. No hace falta ejecutar las pruebas.
4. **Mensaje de commit:** `document-code` añade una viñeta *Documentación* al mensaje del work item.
   Si el work item ya está mezclado, escribe el mensaje entero de un commit de seguimiento `docs(…)`.
   No se crea un skill `commit-message` aparte: la regla vive en `wbs-execution` (paso 7) y cada paso
   posterior añade una sola viñeta.
5. **Notas de versión:** no las hace este paso. Las genera el pipeline a partir de los commits
   (fase 4).

## Consecuencias

- La documentación viaja en el mismo commit que el código, antes del PR.
- El script es determinista: un cambio que no sea comentario no pasa, aunque el agente diga lo
  contrario.
- Un `docs/` que sigue siendo la plantilla vacía recibe solo la sección del work item; no se rellena
  entero fuera de alcance.
- `check-sdd-item.py` muestra «sin documentar» como información, sin contarlo como aviso.

## Alternativas consideradas

- **Que `wbs-execution` documente al implementar:** el contexto de implementación ya es grande
  (ADR-0018), y la documentación debe describir el código después de las correcciones de QA.
- **Revisar los comentarios a ojo en el PR:** no garantiza que no se colara un cambio de código.
