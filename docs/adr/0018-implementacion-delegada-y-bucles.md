# ADR-0018 · `wbs-execution` delega cada tarea en el agente de su capa, con bucles limitados

- **Estado:** Aceptada (confirmada en el bloque 2 con el PBI 40933; ajustes de la v0.6.1)
- **Fecha:** 2026-10-14
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0013, ADR-0014, ADR-0017

## Contexto

En el PBI 40944, `wbs-execution` implementó las cuatro tareas en la sesión principal y llegó a 175k
tokens: cada archivo leído, cada salida de build y cada prueba se quedaban en la conversación.
ADR-0013 ya preveía que `backend-dev` y `frontend-dev` hicieran cada tarea con un paquete cerrado;
faltaba definir cómo se reparte el trabajo, quién verifica y hasta dónde se reintenta.

## Decisión

1. **Quién implementa.** La columna **Rol** del WBS decide: `Backend` → `backend-dev`, `Frontend` →
   `frontend-dev`, y `Transversal` o QA → la sesión principal. `technical-analysis` divide en dos
   las tareas que tocan las dos capas. Sin subagentes (Visual Studio), la sesión principal
   implementa con las mismas reglas.
2. **Paquete cerrado.** La sesión principal entrega al agente todo lo que necesita:
   - la tarea y sus SPEC literales;
   - los contratos;
   - los archivos con sus líneas;
   - los comandos exactos;
   - las convenciones;
   - las traducciones;
   - los riesgos y las decisiones de la sesión.

   El agente no lee los documentos de diseño.
3. **El agente:**
   - escribe las pruebas primero;
   - toca solo los archivos del paquete (los demás los declara);
   - no edita `docs/sdd/` ni hace commit;
   - se detiene y pregunta ante cualquier decisión de negocio o de diseño;
   - responde con un informe fijo de 80 líneas como máximo.
4. **La sesión principal verifica.** Vuelve a ejecutar build, pruebas, lint y comprobación de tipos,
   y revisa con `git status` que solo cambió lo esperado. El informe del agente no cuenta como
   evidencia. Solo la sesión principal escribe en la carpeta del work item.
5. **Bucles con límite:**

   | Bucle | Límite |
   | --- | --- |
   | El agente arregla su propia comprobación fallida | 3 intentos |
   | La verificación de la sesión principal falla y vuelve al agente | 2 rondas |
   | Hace falta cambiar el diseño durante la implementación | Primero se actualizan 03/04 con aprobación |
   | El agente se detiene sin informe (v0.6.1) | 1 reanudación con «Ya hecho» y «Falta» |
   | Hallazgos de QA que vuelven a implementación (ADR-0019) | 2 rondas de QA |

   Pasado un límite, decide la persona.
6. **Paralelo opcional.** Como mucho 2 agentes a la vez, en tareas sin dependencias pendientes y con
   archivos disjuntos (traducciones incluidas), y solo si la persona lo acepta al empezar.

## Consecuencias

- El contexto de la sesión principal debería bajar: recibe informes, no el detalle de cada archivo.
- Las pruebas se ejecutan dos veces (agente y verificación). Cuesta tiempo, pero el resultado no
  depende de lo que diga el agente.
- En Claude Code, los agentes piden permiso para cada comando (`dotnet`, `yarn`) salvo que estén
  permitidos en la configuración.
- `backend-dev` y `frontend-dev` usan `sonnet` en Claude Code (ADR-0017); en Copilot, el modelo de
  la conversación.

## Alternativas consideradas

- **Que el agente marque la tarea como hecha:** dos escritores en el WBS y sin verificación
  independiente.
- **Un solo agente para todo:** pierde la ventaja de un contexto limpio por capa, y las reglas de
  cada capa (pruebas de .NET, traducciones de React) se mezclan.

## Ajustes tras la prueba (v0.6.1)

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE2.md`:

- **Pruebas primero, demostradas:** el informe del agente trae la línea *Rojo*, de la ejecución
  hecha antes de tocar el código de producción. Si falta, la sesión principal lo registra como
  desviación.
- **Una edición por archivo y tarea** en `05`, `CHANGELOG.md` y `bitacora.md`, sin repetir la tabla
  del WBS. El contexto de la sesión principal no bajó (172,8k frente a 175k) por estas ediciones.
- **Tareas grandes divididas:** las de más de 2 SP que reestructuran y cambian comportamiento se
  separan en dos.
- **Cierre:**
  - Barrido de marcadores ya resueltos antes del mensaje de commit.
  - Rutas exactas para el commit, nunca `git add -A`.
