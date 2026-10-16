# ADR-0001 · Registrar las decisiones del estándar con ADR

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

El estándar SDD reúne propuestas de varias personas y obliga a elegir entre opciones que
compiten (dónde se guardan los artefactos, idioma, formato de commit, herramientas). Si esas
elecciones solo quedan en conversaciones, se pierden y se vuelven a discutir.

## Decisión

Toda decisión que cambie el comportamiento del kit se registra como un ADR en `docs/adr/`,
con la plantilla `0000-plantilla.md`. Los ADR se numeran en orden y no se borran: una
decisión que cambia se sustituye por un ADR nuevo y el antiguo pasa a «Sustituida por».

## Consecuencias

- El historial explica por qué el kit es como es.
- Cada PR al kit que cambie una regla enlaza el ADR que la justifica.
- El índice de `docs/adr/README.md` se mantiene al día en el mismo PR.

## Alternativas consideradas

- Registrar las decisiones solo en el documento del brief: se pierde la relación con el código del kit.
