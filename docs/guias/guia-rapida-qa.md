# Guía rápida · QA con fi-sdd-standard

## Preparar el work item (antes del desarrollo)

1. Crea la carpeta y copia el work item de Azure DevOps en `story.md`, con sus capturas en
   `assets/`:
   ```powershell
   python <kit>\scripts\new-sdd-item.py <id> "<título>"
   ```
2. `/enrich-us <id> qa`: además del `pbi.md`, clasifica cada criterio de aceptación.

   | Clasificación | Significa | Qué haces |
   | --- | --- | --- |
   | **Definido** | `story.md` lo dice | Nada |
   | **Deducción directa** | Se sigue sin elección de `story.md`, un adjunto o el código | Revisa la fuente que cita |
   | **A confirmar** | No está decidido | Lleva la pregunta al PO; se queda como `[PENDING-BUSINESS]` |

3. `/test-cases <id>`: casos funcionales, negativos, de borde, de permisos, de idioma y de
   regresión, con datos del work item.
   - Escribe `test-cases.md` y `test-cases.csv`.
   - Los casos de un criterio *A confirmar* quedan `Bloqueado` y no van al CSV.
4. Revisa `test-cases.md`. Después, importa el CSV en Azure Test Plans: *Test Plans → tu plan →
   suite → Import*, el archivo `test-cases.csv`.

## Durante la revisión

- `qa-report.md`, que deja `/qa-review`, dice qué se revisó y cada hallazgo con su estado. Los
  casos de prioridad alta de `test-cases.md` deben tener una prueba automatizada o una
  comprobación en ejecución.
- Una respuesta del PO que cambia un criterio se anota en `bitacora.md` y en `pbi.md`. Después,
  `/test-cases <id>` actualiza los casos y conserva sus ID.

## Lo que QA no tiene que hacer

- **Editar `story.md` a mano después de la IA:** `story.md` es tuyo y la IA nunca lo toca.
- **Inventar datos:** si un caso necesita un valor que el work item no da, se pregunta.
