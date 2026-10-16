# ADR-0026 · El bucle de pipeline en rojo pasa a la fase 4

- **Estado:** Aceptada
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0012, ADR-0023

## Contexto

La fase 2 lista cuatro bucles: por tarea, de hallazgos de QA, de pipeline en rojo y «un cambio
después de implementar actualiza primero 03 y 04». Los tres primeros funcionan en la sesión. El de
pipeline en rojo necesita leer el resultado del pipeline de Azure DevOps (el MCP o la API) y las
plantillas de CI de la fase 4, que todavía no existen.

## Decisión

- El bucle de pipeline en rojo se implementa en la **fase 4**, con las plantillas de CI y la
  validación del PR.
- Hasta entonces, `pr-check.py` (ADR-0023) ejecuta en local las mismas reglas que el PR, y un
  pipeline en rojo se corrige con `/wbs-execution <ID> qa` o `/quick-fix`, a partir del log que pega
  la persona.

## Consecuencias

- La fase 2 se cierra sin ese bucle.
- La fase 4 lo diseña: leer el log, llevarlo a un hallazgo y corregirlo, con un límite de 2 rondas.
