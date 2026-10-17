# Resultados de `/project-context` en Calls4Grants

**Fecha:** 2026-10-16 · **Rama:** `chore/sdd-kit-piloto` · **Quién:** Juan Ceballos
**Intentos:** 2. El primero (v0.11.0) se descartó; el segundo (v0.12.0) terminó.
**Commits del segundo:** `725da8e` instalar v0.12.0 · `9198a18` ignorar `nuget.local.config` ·
`7441cc0` contexto del proyecto y documentación base (21 archivos)
**Fuente:** el registro completo de la sesión de apoyo que guió los dos intentos (revisado el
2026-10-17).

## Resumen

El segundo intento terminó: `check_project.py` con 0 errores y 4 avisos, `AGENTS.md` con 149
líneas, unos 24 minutos de sesión. La sesión aplicó el paso 6.4 al kit anterior de Clavijo:

- Retiró los hooks PowerShell que cubre el kit (`format-on-edit.ps1`, `protect-core-ui.ps1`,
  `warn-controller-auth.ps1`); sus reglas pasaron a `sdd-guardrails.json`.
- Retiró el agente `qa-reviewer` antiguo (pasó sus áreas frágiles a `docs/reglas-negocio.md`) y el
  skill `/pbi`; conservó `/i18n`, que no tiene equivalente en el kit.
- Creó `FIniciativas.Calls4Grants.Tests` con las pruebas de arquitectura y una prueba de
  `TranslationService`, y lo añadió a la solución.
- Corrigió la documentación que contradecía al código: MobX → `@hookstate/core`, `@inject` →
  `container.get`, el proxy `:3000 → :5001`, que no existe (lo hace `UseReactDevelopmentServer`,
  `Startup.cs:482`), y `appsettings.json`, que no se carga en Debug.

Después se probó el flujo con el PBI 40237 (multiselección de anualidades e hitos): `story.md`
correcto a la primera (`check-sdd-item.py` 0 errores) y `enrich-us` con 10 preguntas, de las que 5
se respondían desde el código. Esa prueba sigue en curso.

## Por qué hubo que repetir el primer intento

La sesión no falló en el contexto: se desvió a arreglar lo que encontraba por el camino.

| # | Qué pasó | Efecto | Qué cambia en la v0.13.0 (ADR-0028) |
| --- | --- | --- | --- |
| 1 | El entorno no compilaba: PAT de NuGet vencido (401), enlace `ClientApp/src/core` roto, Node 24 en vez de 22, `eslint`/`stylelint` rotos | Se descubrió a mitad de la skill y la sesión intentó resolverlo | Compuerta del entorno: preflight de `inventory.py` y `dotnet restore` antes de explorar; lo que bloquea para la sesión con los pasos para la persona |
| 2 | Migrar y depurar los hooks antiguos y el formateador: `TimeoutExpired` a 90 s en frío (9 s en caliente), pruebas con `$null \|`, prettier → eslint → prettier | Horas fuera del objetivo | Alcance: una herramienta tiene un intento; el formateador solo se migra si funcionó en menos de ~20 s; `format` admite varios comandos y `formatTimeout` |
| 3 | El JSON que manda Windows PowerShell 5.1 por la entrada estándar lleva BOM y el hook lo descartaba sin avisar | Las pruebas a mano del guard «no bloqueaban» | `sdd_guard.py` lee la entrada como `utf-8-sig` |
| 4 | Los hooks antiguos usaban rutas relativas y fallaban cuando un subagente trabajaba en otra carpeta | Más depuración | Ya cubierto: el hook del kit usa `${CLAUDE_PROJECT_DIR}` |
| 5 | Sin commit de la instalación antes de `/project-context`, y todo sin commit durante horas | Miedo a perder trabajo; el reinicio necesitó `switch --discard-changes`, `branch -D` y `clean -fd` | La skill se para si la instalación no tiene commit; `install.py` lo recuerda en «Siguiente» |
| 6 | Se instaló la v0.11.0 cuando ya existía la v0.12.0 | El SAS de `pr-check` y ADR-0027 llegaron después | Manual: instalar la última versión antes de empezar |
| 7 | `appsettings.json` y `nuget.config` no estaban en los `secrets` por defecto | Un subagente leyó `appsettings.json` entero; una sesión imprimió los PAT de `nuget.config` | Por defecto en `secrets` (y `nuget.config` en deny); `install.py` los añade a un `sdd-guardrails.json` existente; `inventory.py` lista los secretos versionados sin el valor |
| 8 | Las decisiones se pidieron una a una | Muchas idas y vueltas | Un solo bloque de preguntas con una línea para rellenar |
| 9 | `AGENTS.md` llegó a 189 líneas | Por encima del objetivo de 185 | Ya cubierto por el presupuesto por sección; el segundo intento quedó en 149 |

El segundo intento funcionó porque se preparó fuera de la sesión: respaldo de los borradores,
reinicio limpio desde `origin/dev`, comprobaciones previas, instalación de la v0.12.0 con su commit
y todas las respuestas del paso 5 en un bloque.

## Hallazgos del kit

| # | Qué | Causa | Corregido en |
| --- | --- | --- | --- |
| 1 | `pr-check.py`: `✗ secretos en el diff — .agents/scripts/pr-check.py (firma SAS)` | El patrón aceptaba `SharedAccessSignature=` sin valor y se encontraba a sí mismo | v0.12.1 |
| 2 | El hook ignoraba los eventos con BOM (PowerShell 5.1) | `json.loads` rechaza el BOM y el hook sale con 0 ante cualquier error | v0.13.0 |
| 3 | `format` admitía un solo comando por extensión: `eslint --fix` dejó de ejecutarse | Diseño | v0.13.0: lista de comandos |
| 4 | `dotnet test` falla con el SDK 10 local y xUnit v3 (Microsoft.Testing.Platform); funciona `dotnet run --project` | El proyecto de pruebas creado no trae el adaptador de VSTest | v0.13.0: la skill pide `Microsoft.NET.Test.Sdk` y `xunit.runner.visualstudio`. **Verificar** en Calls4Grants añadiéndolos |
| 5 | `check_project.py` listaba como pruebas de arquitectura las plantillas de `.agents/` y `.claude/` | La búsqueda no excluía las carpetas del kit | v0.13.0 |
| 6 | Restaurar con NuGet: las credenciales del `NuGet.Config` de usuario no sirven si el `nuget.config` del repositorio trae credenciales del mismo origen | Gana el archivo más cercano | Documentado (manual, capítulo 17). La solución de fondo es quitar las credenciales del `nuget.config` versionado |

## Borradores del proyecto

El piloto dejó 14 borradores en `docs/sdd/_borradores/` de Calls4Grants (3 urgentes, 5 altas,
4 medias y 2 bajas): seguridad, autorización, dependencias y herramientas del frontend. El detalle
no se publica aquí porque describe fallos sin corregir de un producto interno: está en el equipo del
responsable y pasa a Azure DevOps como work items, que es donde se siguen (ADR-0027, ADR-0028).

Una credencial quedó expuesta durante el piloto y se rotó fuera del repositorio.

## Pendiente

- 4 `[REQUIRES-VALIDATION]` legítimos en *Project context*: `dotnet test` en CI con el SDK 8,
  `.env*`, `ResponseExceptionFilter` (Razorblade, fuera del repositorio) y el nombre de las ramas
  de trabajo.
- Actualizar el kit en la rama del piloto a la v0.13.0 (`chore(sdd): actualizar fi-sdd-standard a
  v0.13.0`): `install.py` añadirá los secretos por defecto que falten.
- El tech lead revisa `sdd-guardrails.json` en el PR a `dev`.
- Terminar la prueba del PBI 40237 (G1 → G4) y registrar sus resultados.
