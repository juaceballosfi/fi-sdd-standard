# ADR-0011 · Fuente única y adaptadores generados, sin enlaces simbólicos

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0005

## Contexto

LIDR SpecBoot expone los mismos archivos a cada herramienta con enlaces simbólicos. En Windows y
en los zips esos enlaces se rompen: en el zip revisado, `AGENTS.md` y `CLAUDE.md` llegaron como
archivos de texto con una ruta dentro. El flujo SDD v2.3 ya resolvía esto con un script que genera
la copia de Claude Code.

## Decisión

- Skills, agentes, plantillas y reglas se escriben una sola vez en `core/`.
- `scripts/build-adapters.py` genera el formato de cada herramienta (ADR-0005), incluidos los
  campos propios de cada una (por ejemplo `model` y `allowed-tools` solo en la copia de Claude Code).
- No se usan enlaces simbólicos.

## Consecuencias

- Una regla se cambia en un sitio y llega a las cuatro superficies.
- `scripts/validate.py` comprueba que la fuente cumple el estándar Agent Skills y que las reglas
  comunes son idénticas.

## Alternativas consideradas

- Enlaces simbólicos: fallan en Windows sin modo desarrollador y en los zips.
- Mantener copias a mano por herramienta: divergen.
