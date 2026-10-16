# ADR-0010 · Responsable del estándar y proyectos piloto

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Decisión

- Responsable del estándar: **Juan Ceballos**.
- Pilotos: **Bonis**, para el flujo completo, porque tiene pruebas en CI y pruebas de arquitectura;
  y **Calls4Grants**, que ya tiene `sdd-clavijo` y el skill i18n, y permite probar el flujo en un
  proyecto sin proyecto de pruebas.
- El kit se desarrolla en un repositorio git local. El repositorio en Azure Repos se crea cuando el
  kit esté probado y aprobado.

## Consecuencias

- Hasta que exista el repositorio en Azure Repos, la instalación en los pilotos es manual.
