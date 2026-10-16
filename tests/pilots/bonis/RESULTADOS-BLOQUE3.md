# Resultados del bloque 3 de la fase 2 · `qa-review` · PBI 40933

**Fecha:** 2026-10-14 · **Kit:** v0.7.0 (skills v3.6) · **Quién:** Juan Ceballos
**Alcance:** rango del squash `9e07c66d..99e5da20` (PR 14468, ya en `dev`).

## Resumen

La revisión independiente sí aporta. En el bloque 2, la sesión que implementó verificó todo: 1034
pruebas y SPEC-10 a SPEC-12 a mano. Aun así, `qa-reviewer` encontró 3 hallazgos bajos reales:

- **QA-01 · fallo latente en el modal.** El nombre se lee del formulario en el render y solo sale
  bien por un render extra de React 17.
- **QA-02 · flag sin prueba.** Ninguna prueba comprueba que el flag llegue a los 4 `Enqueue`.
- **QA-03 · huecos de cobertura** en las pruebas de columnas.

No marcó como hallazgos los problemas que ya se conocían (`unicode-bom`, TS2345).

El ciclo completo funcionó: ronda 1 → decisión de la persona → `/wbs-execution 40933 qa` → ronda 2,
que verificó las 3 correcciones y encontró un hallazgo nuevo, QA-04 (aceptado). Se respetó el límite
de 2 rondas. `runtime-tester` arrancó la aplicación, no editó nada y dijo con claridad lo que no
pudo probar.

## Tabla de resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos y 5 agentes visibles | ✓ | El commit del kit solo llevó archivos del kit (`b7db6bac`) |
| 2 | Alcance correcto y pruebas ejecutables | ✓ | Detectó que el código de `head` es el del árbol de trabajo |
| 3 | Paquete con fuentes, sin conclusiones | ✓ | El revisor leyó el diseño por su cuenta |
| 4 | Hallazgos con `ruta:línea`, regla, escenario y confirmación | ✓ | QA-01 explica el mecanismo exacto (render extra de `setBusy`) |
| 5 | La sesión principal verifica cada hallazgo | ✓ | Resolvió la duda del revisor sobre las traducciones vacías, con evidencia |
| 6 | No salen como hallazgos los problemas ya conocidos | ✓ | |
| 7 | `runtime-tester` | ✓ honesto, poco útil aquí | En Debug el usuario es fijo (`Consultant` + `GlobalAdmin`): SPEC-10 a 12 quedaron «No ejecutado». La regresión como `Consultant`, parcial. Dejó 4 `.xlsx` en Azurite y registros de Hangfire en local. Sí paró la aplicación (comprobado: nada escucha en 5204/5205; el único `dotnet` es el de C# Dev Kit), pero su informe no lo decía |
| 8 | `qa-report.md` completo y una línea en la bitácora | ✓ | La línea de la ronda 1 y la de la ronda 2 |
| 9 | `qa-review` no tocó código | ✓ | `git status`: solo los 3 documentos |
| 10 | Comprobador | ✓ | «listo para commit» con 4 hallazgos decididos |
| 11 | Bucle de QA | ✓ | Ver el detalle debajo de la tabla |
| 12 | Contexto y tiempo | 104,7k | Mismo valor en todas las sesiones según la persona (mensajes: 66k); 40944 implementación: 175k. Ronda 1: 5 min 15 s; modo `qa`: unos 15 min en tres pasadas; ronda 2: 5 min 23 s |
| 13 | ¿Encontró algo que no vio el bloque 2? | ✓ | QA-01 (fallo latente) y QA-02 (un SPEC solo con verificación manual) |

Detalle del bucle de QA (comprobación 11):
- Sin hallazgos `A corregir`, el modo `qa` no hizo nada.
- Ante QA-02 se paró y preguntó: los argumentos con nombre no son posibles (CS0853 en árboles de
  expresión de Hangfire). Propuso tres opciones.
- En las pruebas sin cambio de producción, el *Rojo* se demostró con una mutación temporal que
  luego se deshizo.
- La ronda 2 revisó solo las correcciones.

## Lo que funcionó

- **El revisor con un modelo de razonamiento y contexto limpio** encuentra cosas que la sesión que
  implementó no ve: QA-01 depende del orden de render de React.
- **Verificar antes de escribir:** cada hallazgo se contrastó con el código. La duda del revisor se
  descartó con evidencia y no se escribió como hallazgo.
- **Decisión de la persona por hallazgo**, con el cambio de opinión de QA-03 (de `Aceptado` a
  `A corregir`) registrado.
- **Modo `qa` prudente:** no hace nada si nada está `A corregir`, y se para ante una dificultad
  técnica real en lugar de improvisar.
- **Mutación como prueba de que la prueba sirve** cuando no hay código de producción nuevo.
- **Ronda 2:** el revisor encontró que la prueba nueva de SPEC-08 era casi tautológica (QA-04).

## Lo que hay que mejorar (aplicado en la v0.7.1)

1. **La bitácora se editó hacia atrás.** El modo `qa` añadió «QA-03 aceptado» al final de una
   línea anterior con `sed`. *Registro* debe ser solo de añadir líneas, nunca de editarlas:
   reforzarlo en la convención compartida.
2. **Mensaje de commit parcheado.** Se rehízo por partes tras cada hallazgo y quedó «dejó **dos**
   hallazgos bajos» cuando se corrigieron tres. Regla: tras el último hallazgo corregido, el mensaje
   se escribe de nuevo entero a partir del CHANGELOG, no se parchea.
3. **El *Resultado* de arriba de `qa-report.md` se quedó en la ronda 1** («3 bajos»). Debe reflejar
   el estado actual; las secciones de cada ronda guardan la historia.
4. **Nombre de la persona inconsistente:** «Juan Ceballos», en negrita, frente a «Juan Antonio
   Ceballos Usuga». Usar siempre el nombre de «Preparado por» de `story.md`.
5. **`runtime-tester`:**
   - El informe debe incluir siempre «Procesos detenidos» y «Datos locales creados».
   - `qa-review` no debe proponerlo cuando el cambio depende del rol y `AGENTS.md` dice que el
     usuario local es fijo.
6. **Mutación como *Rojo*:** codificar en `backend-dev` y `frontend-dev` lo que se hizo de forma
   espontánea, para las tareas que solo añaden pruebas: mutación temporal, comprobar que fallan,
   revertir, y `git diff --stat` del código de producción vacío.
7. **Bonis `AGENTS.md`:** documentar que la suplantación de Debug tiene roles fijos
   (`DebugImpersonationMiddleware.cs`). Así `runtime-tester` y `qa-review` lo saben de antemano.

## Para el desarrollador

- **QA-01 a mano antes del PR:** entra como delegado estándar, abre «Agregar proyecto» y comprueba
  que se ve tu nombre y que la petición `CreateProject` lleva `managers`. QA-01 no tiene prueba
  automática.
- **Corregir en `commit-message.md`** «dejó dos hallazgos bajos» → «dejó tres hallazgos bajos».
- ~~Comprobar que no quedó ningún proceso de `runtime-tester`~~: comprobado, no quedó ninguno.
- **Commit de seguimiento** `fix(roles): corregir hallazgos de QA` con `Ref: #40933`. Va con la
  variante B de `docs/guias/git-por-work-item.md`, en una rama nueva desde `dev`.
- Seguimiento subido: PR 14472 (`fix(roles): corregir hallazgos de QA`), mezclado en `dev`
  (`f8dac7c5`) y traído a `chore/sdd-kit-piloto`. **Bloque 3 cerrado.**
- Copiar en el `AGENTS.md` de Bonis (sección *Project context*) las notas nuevas de
  `tests/pilots/bonis/AGENTS.md`: *Runtime checks* y las pruebas y la comprobación de tipos del
  frontend.
