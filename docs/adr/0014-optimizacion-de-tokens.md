# ADR-0014 · Reglas de optimización de tokens

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Decisión

1. `AGENTS.md` por debajo de 200 líneas; el detalle en `docs/`, que se abre solo cuando hace falta.
2. Skills con carga progresiva: plantillas en archivos aparte y `SKILL.md` por debajo de 500 líneas.
3. La exploración del código la hace `code-explorer`; a la sesión principal vuelve solo el mapa.
4. Una sesión por paso: cada skill lee los artefactos del anterior.
5. Cada tarea del WBS en un subagente, con contexto aislado.
6. Modelo según el paso: razonamiento solo para enriquecer, diseñar y revisar.
7. Lo determinista (formatear, validar, compilar, probar) lo hacen scripts, hooks y el pipeline.
8. No se leen `bin/`, `obj/`, `node_modules/` ni archivos generados; los archivos grandes, por búsqueda.
9. Respuestas cortas con formato fijo, sin repetir código ni logs.
10. Subagentes solo cuando la lectura sería grande o la tarea es independiente.

## Consecuencias

- En el piloto se anota el consumo de cada paso por work item para comprobar que las reglas funcionan.

## Tabla de modelos (revisión mensual)

| Nivel | Claude Code | Uso |
| --- | --- | --- |
| Razonamiento | `opus` | `enrich-us`, `technical-analysis`, `project-context`, `qa-reviewer` |
| Estándar | `sonnet` | `wbs-execution`, `document-project`, `backend-dev`, `frontend-dev`, `runtime-tester` |
| Rápido | `haiku` | `code-explorer`, `doc-writer` |

**Modelo por defecto del sello** (cuando la sesión no puede saber qué modelo la ejecuta):
`claude-opus-5-5`. Revisado el 2026-10-15.
