# ADR-0003 · Idioma

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

Los skills SDD tienen instrucciones en inglés y producen documentos en español. Bonis escribe
comentarios y commits en español; Calls4Grants, sobre todo en inglés.

## Decisión

| Qué | Idioma |
| --- | --- |
| Documentación del flujo (artefactos en `docs/sdd/`) y guía del kit | Español |
| Comentarios de código y mensajes de commit | Español |
| Instrucciones internas de skills y agentes (`SKILL.md`, agentes, `AGENTS.base.md`) | Inglés |
| Nombres de archivo, identificadores (`CA-01`, `T-01`…) y marcadores | Sin cambios |

## Consecuencias

- `AGENTS.base.md` incluye la regla de idioma para todos los proyectos.
- En Calls4Grants, el código nuevo se comenta en español; el existente no se reescribe.

## Alternativas consideradas

- Todo en inglés (como exige LIDR SpecBoot): no encaja con el equipo ni con los commits de Bonis.
- Idioma libre por proyecto: genera la misma inconsistencia que hoy.
