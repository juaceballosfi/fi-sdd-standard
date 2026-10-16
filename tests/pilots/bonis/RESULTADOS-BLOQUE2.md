# Resultados del bloque 2 de la fase 2 · `backend-dev` y `frontend-dev` · PBI 40933

**Fecha:** 2026-10-14 · **Kit:** v0.6.0 (skills v3.5) · **Quién:** Juan Ceballos
**Work item:** 40933 — [RSP] Correcciones rol delegado. Hay 4 tareas y 6 SP:
- T-01: el Excel, en un archivo de 4582 líneas.
- T-02: la pantalla «Investigadores».
- T-03: el modal «Agregar proyecto».
- T-04: la verificación final.

## Resumen

La delegación funciona:
- Cada tarea fue al agente de su capa, con un paquete cerrado.
- Hubo dos agentes en paralelo, sobre archivos distintos.
- La sesión principal verificó todo por su cuenta y fue la única que escribió en `docs/sdd/`.
- El resultado está en verde y pasó la verificación manual.

Falló una cosa: en T-01 no se escribieron las pruebas primero, porque el agente se quedó parado.

El contexto de la sesión principal no bajó: 172,8k frente a 175k en el 40944. El 40933 es más
grande y tuvo que reanudar un agente, pero la causa principal está en cómo la sesión principal
registra el avance (ver «Lo que hay que mejorar»).

## Tabla de resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos y agentes visibles | ✓ | Faltaba `git add` de los agentes nuevos; corregido en `PRUEBA-BLOQUE2.md` |
| 2 | La confirmación asigna cada tarea al agente correcto | ✓ | T-01 → `backend-dev`, T-02 y T-03 → `frontend-dev`, T-04 → la sesión principal |
| 3 | El paquete es cerrado | ✓ | SPEC literales, archivos con líneas, comandos y riesgos |
| 4 | Pruebas primero en T-01 | ✗ | El agente implementó antes de escribir las pruebas y se paró a los 600 s. Al reanudarlo, la caracterización se fijó contra `HEAD` |
| 5 | Informe del agente con el formato y menos de 80 líneas | ✓ | |
| 6 | La sesión principal verifica por su cuenta y revisa el alcance | ✓ | Ver el detalle debajo de la tabla |
| 7 | Solo la sesión principal escribe en `docs/sdd/` | ✓ | |
| 8 | Paralelo sin conflictos | ✓ | T-01 ∥ T-02 y luego T-01 ∥ T-03; nunca más de 2 agentes |
| 9 | Bucles | ✓ | Se reanudó T-01 una vez tras el bloqueo; no hizo falta ninguna ronda de verificación |
| 10 | Build, pruebas y lint en verde al final | ✓ | SPEC-10 a SPEC-12, a mano: OK |
| 11 | Contexto de la sesión principal al terminar | 172,8k | 40944: 175k. Mensajes: 132,6k |
| 12 | Tiempo | — | T-01 10 min 22 s; T-02 3 min 50 s; T-03 3 min 21 s |

Detalle de la comprobación 6:
- Build: 0 errores y 0 advertencias.
- Pruebas en Release: 1034 de 1034. La clase nueva, 25 de 25.
- Lint: 0 errores.
- Tipos: 148 errores antes y 148 después.
- `git status`: nada tocado en `core-ui`.

## Lo que funcionó

- **Bloqueo de T-01.** La sesión principal revisó lo que el agente había dejado a medias, lo
  reanudó con la lista exacta de lo que faltaba y anotó la desviación en la bitácora.
- **Verificación independiente.** La sesión principal no aceptó el informe sin más: volvió a
  ejecutar la suite completa y comprobó que las expresiones extraídas eran idénticas a `HEAD`.
- **Hallazgo falso.** Un hallazgo fuera de alcance (otros Excel sin filtro) resultó falso. Se
  corrigió con una entrada nueva en la bitácora y no se creó un borrador.
- **Mensaje de commit.** 2814 caracteres, con `Ref: #40933` y sin trailer de IA.

## Lo que hay que mejorar (v0.6.1)

1. **Muchas ediciones pequeñas de los documentos.** La sesión principal editó `05` 9 veces,
   `bitacora.md` 7 y `CHANGELOG.md` 5. Cada edición del WBS repite filas muy anchas en la
   conversación. Regla nueva: al cerrar cada tarea, una sola edición por archivo.
2. **El orden «primero las pruebas» no se puede comprobar.** `backend-dev` debe ejecutar las
   pruebas nuevas en rojo y pegar el resumen de esa ejecución en el informe antes de tocar el
   código de producción. Cuando una tarea extrae código, la caracterización va primero y en verde.
3. **No hay pauta para un agente parado.** Se añade a la tabla de bucles:
   - revisar `git diff --stat` de lo que dejó;
   - reanudarlo una sola vez con la lista de lo que falta;
   - si se vuelve a parar, decide la persona.
4. **Tareas grandes sobre archivos enormes.** T-01 tenía 3 SP sobre un archivo de 4582 líneas.
   `technical-analysis` debe dividir las tareas de más de 2 SP que extraen código y cambian
   comportamiento a la vez, por ejemplo:
   - caracterización + extracción;
   - cambio de comportamiento.
5. **El cierre sugería `git add -A`.** Habría incluido archivos ajenos al work item. El cierre
   debe listar las rutas exactas y recordar la rama `feature/<id>-…` (ADR-0006).
6. **Salidas largas de las verificaciones.** La salida del build y de las pruebas debe ir a un
   archivo, y en la conversación solo debe quedar el resumen. Esto ya lo pide `AGENTS.md`; se
   refuerza en el paso 4.3.
7. **Marcadores resueltos que siguen en `pbi.md`.** Los dos `[REQUIRES-VALIDATION]` de las
   «Notas de implementación» se cerraron en el bloque 1: el modal usa un campo oculto (04 §4.4) y
   `ManagerMaster` se resolvió en 01. `wbs-execution` no los quitó. El comprobador avisó, pero
   dijo «listo para commit». Ajustes:
   - Antes de escribir `commit-message.md`, `wbs-execution` busca en `pbi.md`/`bug.md` y en 00–06
     los marcadores ya resueltos y los cambia por la decisión.
   - El comprobador no dice «listo para commit» mientras haya marcadores abiertos en `pbi.md`.

## Para el desarrollador

- En `pbi.md`, los dos `[REQUIRES-VALIDATION]` ya resueltos se cambiaron a mano por la decisión
  antes del commit.
- El commit lleva los 5 archivos de código y toda la carpeta del 40933. Antes había una versión
  anterior de `05` y `bitacora.md` en *staged*; el `git add` de la carpeta la actualiza.
- Rama `feature/40933-correcciones-rol-delegado` desde `origin/dev`, con *cherry-pick*: PR 14468,
  mezclado en `dev` con squash (`99e5da20`). `dev` se mezcló después en `chore/sdd-kit-piloto`.
  El proceso completo está en `docs/guias/git-por-work-item.md`.
- La revisión de QA (bloque 3, v0.7.0) se prueba sobre el rango del squash: `PRUEBA-BLOQUE3.md`.
- Los 7 ajustes están en la v0.6.1 (incluida en la v0.7.0).
