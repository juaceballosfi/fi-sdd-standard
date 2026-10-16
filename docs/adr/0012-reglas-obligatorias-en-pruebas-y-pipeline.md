# ADR-0012 · Las reglas obligatorias se comprueban con pruebas y en el pipeline

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

Los hooks solo existen en Claude Code; Copilot y Codex no los tienen. Una instrucción en
`AGENTS.md` la puede ignorar un agente. Bonis ya tiene `ArchitectureTests.cs`, que hace fallar la
build si se rompe una regla de arquitectura.

## Decisión

- Las reglas de arquitectura se escriben como pruebas, al estilo de `ArchitectureTests.cs`.
- El resto de reglas obligatorias (no tocar `core-ui/`, traducciones completas, documentación del
  código modificado, formato de commit, marcadores SDD resueltos) se comprueba en la validación del PR.
- Los hooks de Claude Code quedan como aviso temprano, nunca como única defensa.

## Consecuencias

- Las reglas se cumplen igual con cualquier herramienta y aunque no se use IA.
