# ADR-0025 · QA en el flujo: modo QA de `enrich-us` y `test-cases`

- **Estado:** Aceptada (pendiente de validar con Brenna el formato de los casos)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0015, ADR-0019

## Contexto

El brief pide dos piezas para QA: el modo QA de Brenna en `enrich-us`, con la clasificación
Definido / Deducción directa / A confirmar, y un skill `test-cases`. `qa-review` (ADR-0019) revisa
el código, pero no diseña los casos de prueba que ejecuta QA.

## Decisión

1. **`/enrich-us <ID> qa`:** el mismo enriquecimiento, más la clasificación de cada criterio de
   aceptación con su fuente, en la sección *Clasificación de QA* (`<!-- sdd:qa-classification -->`)
   de `pbi.md`/`bug.md`:
   - **Definido:** `story.md` lo dice;
   - **Deducción directa:** se sigue sin elección de `story.md`, de un adjunto o del código actual;
   - **A confirmar:** el resto, con su pregunta, y además es `[PENDING-BUSINESS]`.
2. **Skill `test-cases` v3.8:** casos funcionales, negativos, de borde, de permisos, de idioma y de
   regresión por criterio. Los datos salen del work item. Un criterio *A confirmar* deja sus casos
   `Bloqueado`, nunca inventados. Escribe `test-cases.md` y el CSV que importa Azure Test Plans
   (`test_cases_csv.py`, sin IA).
3. **`qa-review`** comprueba que los casos de prioridad alta tienen una prueba automatizada o una
   comprobación en ejecución.

## Consecuencias

- QA prepara el work item con el mismo `story.md` y puede empezar los casos antes del código.
- El formato del CSV hay que probarlo con una importación real en Test Plans (ola 2), y el de los
  casos validarlo con Brenna. Si su formato es otro, se cambia la plantilla, no la regla de no
  inventar.
