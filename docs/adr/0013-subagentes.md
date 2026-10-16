# ADR-0013 · Subagentes y skills de la sesión principal

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

Un subagente trabaja de una vez en su propio contexto y devuelve un resultado, sin diálogo. Por
eso `wbs-execution` dejó de ser subagente en la v2.0: el flujo necesita confirmaciones.

## Decisión

- `enrich-us`, `technical-analysis` y `wbs-execution` se ejecutan en la sesión principal.
- Siete subagentes para trabajo acotado, definidos en `core/agents/` con formato neutral:

| Subagente | Paso | Permisos | Modelo |
| --- | --- | --- | --- |
| `code-explorer` | 1, 2, 3 | Solo lectura | Rápido |
| `backend-dev` | 3 | Leer, editar, build y pruebas | Estándar |
| `frontend-dev` | 3 | Leer, editar, lint y pruebas del frontend | Estándar |
| `migration-reviewer` | 2, 3 | Solo lectura y script SQL | Estándar |
| `qa-reviewer` | 4 | Solo lectura y ejecutar pruebas | Razonamiento |
| `runtime-tester` | 4 | Ejecutar y leer | Estándar |
| `doc-writer` | 5 | Editar comentarios y `docs/` | Rápido |

- `wbs-execution` entrega cada tarea a `backend-dev` o `frontend-dev` con un paquete cerrado; si el
  subagente necesita una decisión, se detiene y devuelve la pregunta.

## Consecuencias

- En Visual Studio, sin subagentes documentados, la persona elige el agente en cada paso.
