# Resultados de `/project-context` en Calls4Grants · kit v0.12.0

**Fecha:** 2026-10-16 · **Rama:** `chore/sdd-kit-piloto` · **Quién:** Juan Ceballos
**Commits:** `725da8e` instalar v0.12.0 · `9198a18` ignorar `nuget.local.config` · `7441cc0` contexto
del proyecto y documentación base (21 archivos)

## Resumen

La instalación y `/project-context` terminaron: `check_project.py` con 0 errores y `AGENTS.md` con
149 líneas. La sesión aplicó lo previsto en el paso 6.4 para el kit anterior de Clavijo:

- Retiró los hooks PowerShell que cubre el kit (`format-on-edit.ps1`, `protect-core-ui.ps1`,
  `warn-controller-auth.ps1`); sus reglas pasaron a `sdd-guardrails.json`.
- Retiró el agente `qa-reviewer` antiguo y el skill `/pbi` (los sustituyen el del kit y
  `enrich-us`).
- Creó el proyecto de pruebas `FIniciativas.Calls4Grants.Tests` con las pruebas de arquitectura y
  una prueba de `TranslationService`, y lo añadió a la solución.

## Hallazgo del kit

| # | Qué | Causa | Corregido en |
| --- | --- | --- | --- |
| 1 | `pr-check.py`: `✗ secretos en el diff — .agents/scripts/pr-check.py (firma SAS)` | El patrón de firmas SAS aceptaba `SharedAccessSignature=` sin valor y se encontraba a sí mismo, porque el kit se instaló en la misma rama del PR. En las pruebas del kit no salió: el kit estaba en la rama base | v0.12.1: el patrón exige un valor y `validate.py` comprueba que ningún archivo del kit dispare la búsqueda |

Los 3 avisos de `pr-check.py` (título del ticket y `Ref:` en commits `chore`) son los esperados:
el PR del piloto a `dev` se completa con squash (`docs/guias/piloto-a-dev.md`).

## Pendiente

- 4 `[REQUIRES-VALIDATION]` legítimos en *Project context*: `dotnet test` en CI con el SDK 8,
  `.env*`, `ResponseExceptionFilter` (Razorblade, fuera del repositorio) y el nombre de las ramas
  de trabajo.
- Borradores de seguridad en `docs/sdd/_borradores/` (sin versionar): `CONSUL_TOKEN` impreso,
  SignalR a todos los clientes, autorización, certificado TLS de OneData y secretos versionados.
  Crear los work items en Azure DevOps antes del PR del piloto (ADR-0027).
- El tech lead revisa `sdd-guardrails.json` en el PR a `dev`.
