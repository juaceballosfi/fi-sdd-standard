# Recetas

:::lead
Casos completos, de principio a fin, con lo que pides y lo que haces en cada momento. Úsalos como
lista de comprobación las primeras veces.
:::

## Un PBI de principio a fin

| # | Sesión | Tú haces o pides | Resultado | Tiempo orientativo |
| --- | --- | --- | --- | --- |
| 1 | — | Rama `feature/40399-…` desde `dev`; `new-sdd-item.py 40399 "<título>"`; copias el work item y las imágenes; `check-sdd-item.py` | `story.md` listo | 10 min |
| 2 | Nueva (Opus) | `/enrich-us 40399` · respondes o pasas las preguntas al PO · «sí» | `pbi.md` (G1) | 15–30 min |
| 3 | Nueva (Opus) | `/technical-analysis 40399` · «sí» · lees 03 y 04 · «Aprueba 03 y 04» | `00`–`06` (G2) | 20–40 min |
| 4 | Nueva (Sonnet) | `/wbs-execution 40399` · «sí» a cada tarea · resuelves bloqueos | Código, pruebas, `CHANGELOG.md`, `commit-message.md` | Según la WBS |
| 5 | **Nueva** (Opus) | `/qa-review 40399` · decides cada hallazgo | `qa-report.md` (G3) | 15–30 min |
| 6 | La de 4 u otra | Si hay «A corregir»: `/wbs-execution 40399 qa` | Correcciones | — |
| 7 | **Nueva** | `/qa-review 40399` (ronda 2) | Correcciones verificadas | 10 min |
| 8 | Nueva | `/document-code 40399` | Comentarios y `docs/` | 10–20 min |
| 9 | — | `git add <rutas>` · `git commit -F …/commit-message.md` · `pr-check.py` · push · PR | PR a `dev` (G4) | 10 min |

:::tip El work item es lo que se recuerda, no la conversación
Cada paso empieza en una sesión nueva porque todo lo necesario está en la carpeta. Si cierras el
portátil a mitad, mañana basta con lanzar el mismo comando: la skill retoma desde los documentos.
:::

## Un bug pequeño por la vía rápida

1. Rama `fix/41020-…` desde `dev` y la carpeta con `--tipo bug`:
   ```powershell
   git switch -c fix/41020-redondeo-total origin/dev
   python <kit>\scripts\new-sdd-item.py 41020 "El total de la factura redondea mal los céntimos" --tipo bug
   ```
2. Copia en `story.md` la descripción, los **pasos para reproducir** y la información del sistema,
   y guarda las capturas en `assets/`.
3. Sesión nueva: `/quick-fix 41020`. Revisa la causa (`archivo:línea`) y la compuerta, y responde
   «sí».
4. Comprueba en el cierre la línea *Rojo → verde* de la prueba nueva.
5. Sesión **nueva**: `/qa-review 41020` (lee `fix-plan.md` como diseño y comprueba que el cambio no
   salió de la compuerta).
6. `/document-code 41020`, commit con el `git add` de la skill, `pr-check.py` y PR.

## Un bug que no pasa la compuerta

`/quick-fix` responde `⛔ No es una corrección rápida — <criterio> · <evidencia>`. No es un
error: es la señal de que el bug necesita diseño.

1. Lee el motivo: suele ser una migración, un DTO compartido, un cambio de permisos o más de tres
   archivos.
2. Sigue el flujo completo en una sesión nueva: `/enrich-us 41077`. La causa ya encontrada está en
   `bitacora.md` y `enrich-us` la aprovecha.
3. Si crees que la compuerta se equivoca (por ejemplo, contó un archivo de pruebas como de
   producción), díselo con la evidencia; la IA revisa ese criterio, pero no lo fuerza.

## QA prepara los casos antes de implementar

1. QA (o el dev) lanza `/enrich-us 40933 qa`: cada criterio sale clasificado *Definido*,
   *Deducción directa* o *A confirmar*, con su fuente y, si hace falta, una pregunta para el PO.
2. Las preguntas *A confirmar* van al PO. Mientras tanto, `/test-cases 40933` ya genera los casos:
   los de criterios confirmados en `Diseñado`, los demás `Bloqueado`.
3. QA revisa `test-cases.md` e importa `test-cases.csv` en Azure Test Plans.
4. Cuando el PO responde, se resuelve el marcador (capítulo 13) y se vuelve a lanzar
   `/test-cases 40933`: actualiza conservando IDs y desbloquea los casos.
5. En el paso 4, `qa-review` comprueba que cada caso de prioridad Alta tiene una prueba automática o
   una comprobación en ejecución.

## Hallazgos de QA: dos rondas

1. `/qa-review <id>` en sesión nueva → `qa-report.md` con hallazgos `Abierto`.
2. Decides cada Alta y Media: «QA-01 A, QA-02 B asumido por Ana Pérez, QA-03 C».
   - A → `A corregir` · B → `Aceptado (riesgo asumido por …)` · C → `Borrador (_borradores/…)`;
     antes del PR, crea ese work item en Azure DevOps, pon su ID en el estado y borra el borrador.
3. `/wbs-execution <id> qa` (sesión de implementación o nueva, **nunca** la de QA): cada hallazgo
   es una pequeña tarea con su prueba primero; pone `Corregido (<fecha>)` y reescribe
   `commit-message.md`.
4. `/qa-review <id>` en otra sesión nueva: **ronda 2**, solo las correcciones. Pone
   `Corregido (verificado <fecha>)` o los devuelve a `Abierto`.
5. Lo que siga abierto tras la ronda 2 lo decides tú: no hay ronda 3.

## Hace falta cambiar el diseño a mitad de la implementación

`wbs-execution` se para con un bloque *⚠️ Desviación de diseño*: qué sección de `03` no se puede
implementar, por qué, el ajuste mínimo y su impacto.

1. Si apruebas: «Apruebo el ajuste; actualiza 03 §3.4 y 04 §4.4, versión 1.1, aprobado por Ana
   Pérez».
2. La IA actualiza **primero** `03`/`04` (nueva versión y quién aprobó), lo registra en la bitácora
   y sigue con la tarea.
3. Si el ajuste cambia el alcance o un criterio, también pasa a `pbi.md` y genera un *Comentario
   para Azure DevOps* para el PO.

:::warn Lo que no debes hacer
Pedirle que «lo haga como crea mejor» sin actualizar el diseño: `qa-review` revisa contra `03` y
`04`, y encontraría el código fuera de contrato.
:::

## Retomar el trabajo otro día

- **A mitad de la WBS:** sesión nueva, `/wbs-execution <id>`. Lee la columna *Estado* de `05`,
  lista lo hecho y lo pendiente, **ejecuta build y pruebas antes de seguir** y, si la base no está
  limpia, te ofrece arreglar primero o revisar a mano lo que quedó a medias.
- **Empezar en una tarea concreta:** `/wbs-execution <id> from:T-04` (solo si sus dependencias están
  hechas).
- **Un subagente se quedó parado** (sin informe): la sesión mira `git status` y `git diff --stat`,
  anota en la bitácora lo hecho y lo que falta, y lo reanuda **una vez** con `Ya hecho / Falta`. Si
  se vuelve a parar, eliges: A) la sesión termina la tarea, B) se divide.

## El PO cambia el work item a mitad

1. Actualiza `story.md` con el texto nuevo de Azure DevOps (sube la revisión en la cabecera) y anota
   el motivo en `bitacora.md`.
2. Antes de implementar: vuelve a lanzar `/enrich-us <id>` y elige sobrescribir `pbi.md`; luego
   `/technical-analysis <id>` (los documentos anteriores quedan en git).
3. Ya implementando: trátalo como un cambio de diseño (receta anterior). Si el cambio es grande,
   valora un work item nuevo en `_borradores/`.

## Un work item sin criterios de aceptación

`story.md` dirá «Sin criterios de aceptación en el work item». `enrich-us` solo redacta criterios
que **reformulan** lo que ya dicen la descripción y los adjuntos (por ejemplo, el orden del menú
que muestra un mockup), marcados `Propuesto desde la descripción — validar con PO`. Todo lo demás
(otros roles, casos límite, qué pasa sin permiso) son preguntas. Lleva esas preguntas al PO y, a
ser posible, que añada los criterios en Azure DevOps.

## Documentar un proyecto heredado

1. Kit instalado y `/project-context` hecho; `check_project.py` en 0 errores.
2. Pide al PO un PBI «Documentación inicial del proyecto» para enlazar los commits.
3. Rama `docs/document-project-plan`, sesión nueva: `/document-project`. Revisa la propuesta de
   áreas y bloques, aprueba, y haz el commit del plan con el primer bloque o aparte.
4. Por cada bloque: rama `docs/document-project-b01`, **sesión nueva**, `/document-project`, revisa
   el diff de comentarios (solo cambian comentarios), commit con el mensaje de `B-01.md`, PR.
5. Entre bloques, `/document-project status` muestra el avance, los hallazgos y los archivos que
   cambiaron después de documentarse.

## Usar el kit en un proyecto que ya tenía su propia IA

Proyectos con un `CLAUDE.md` largo, skills propias o hooks en PowerShell:

1. `install.py` no toca nada de eso y marca `PENDIENTE`.
2. `/project-context` lo lee como fuente de conocimiento y propone, una línea por elemento:
   - el conocimiento de `CLAUDE.md` → a *Project context* o `docs/`, y `CLAUDE.md` → `@AGENTS.md`;
   - skills que el flujo sustituye (por ejemplo `/pbi` → `enrich-us`) → eliminar;
   - skills sin equivalente (por ejemplo, una que genera traducciones) → se mantienen y se citan en
     *Internationalization*;
   - hooks que el kit cubre (rutas protegidas, formato, patrones) → sus reglas a
     `sdd-guardrails.json` y se quitan de `.claude/settings.json`; los demás se mantienen.
3. Apruebas cada propuesta por separado.
