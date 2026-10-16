# ADR-0024 · Vía rápida para bugs pequeños: `quick-fix`

- **Estado:** Aceptada (pendiente de probar con un bug real de Bonis)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002, ADR-0012, ADR-0019, ADR-0020

## Contexto

El riesgo «sobrecarga para cambios pequeños» del brief: un bug de una línea no justifica `pbi.md`,
siete documentos de diseño y un WBS. El brief pedía una vía rápida con `backend-dev` o
`frontend-dev` directamente.

## Decisión

1. **Skill `quick-fix` v3.8**, en una sesión: `story.md` → `bug.md` + `fix-plan.md` → una tarea `T-01`
   con la prueba primero (línea *Rojo*) → verificación → `CHANGELOG.md` y `commit-message.md`.
2. **Una compuerta antes de escribir nada.** Todos los criterios deben cumplirse:
   - la causa se ve en el código, con archivo y línea;
   - como máximo 3 archivos de producción, en una sola capa;
   - sin migración ni cambios en entidades;
   - sin cambios de contrato (rutas, DTO, eventos);
   - sin cambios de autorización, roles o tenants;
   - sin `[PENDING-BUSINESS]`;
   - textos nuevos solo con todas sus traducciones;
   - sin paquetes nuevos.

   Si falla uno, el bug va al flujo completo con lo encontrado anotado en `bitacora.md`.
3. **`fix-plan.md`** es el diseño de una página: la compuerta con su evidencia, la causa, el cambio,
   las pruebas, los riesgos y la tarea. `qa-review` y `document-code` lo leen en lugar de 03, 04 y
   06. `check-sdd-item.py` reconoce el ítem de vía rápida.
4. **No se salta la QA:** `qa-review` en una sesión nueva comprueba también que el cambio se quedó
   dentro de la compuerta.

## Consecuencias

- Un bug pequeño cuesta una sesión de implementación más la de QA, frente a cuatro.
- La compuerta es estricta a propósito: ante la duda, el bug va al flujo completo.
