# Prueba de `/project-context` · kit v0.9.0 · Bonis y Calls4Grants

**Objetivo:** comprobar que `/project-context` escribe un *Project context* y una documentación base
correctos, con cada dato verificado.

Son dos pruebas (ADR-0021):

| | Bonis | Calls4Grants |
| --- | --- | --- |
| Para qué | Comparar | Instalación real |
| Modo | `fresh` | `new` |
| Referencia | El `AGENTS.md` hecho a mano | — |
| Lo nuevo que se prueba | Integración con DocFX | Proyecto de pruebas, `.claude/` de Clavijo, traducciones generadas, npm |

Prepara tiempo: la skill compila y ejecuta todas las pruebas. Cuenta con 30–60 minutos por
proyecto.

---

## A · Bonis (`fresh`, comparación)

### A.1 · Actualizar el kit en el piloto

```powershell
cd ..\fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
git switch chore/sdd-kit-piloto
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git add .agents .github/agents AGENTS.md .gitignore .sdd-kit.json
git status --short
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.9.0"
```

Debe salir `creado` para `.agents/skills/project-context/` (`SKILL.md`, `scripts/` y `templates/`)
y su copia en `.claude/`. Al final, el instalador sugiere `/project-context`.

### A.2 · Rama de prueba y copia de referencia

```powershell
git switch -c chore/sdd-project-context-prueba
Copy-Item AGENTS.md $env:TEMP\AGENTS-referencia.md
Copy-Item -Recurse docs $env:TEMP\docs-referencia
```

### A.3 · Ejecutar

Cierra Claude Code y ábrelo de nuevo. En una sesión nueva:

```text
/project-context fresh
```

| Momento | Qué comprobar |
| --- | --- |
| Paso 0 | Ve la rama de prueba y el modo `fresh`. Avisa de la duración |
| Inventario | Detecta los **dos archivos de bloqueo** (`yarn.lock` y `package-lock.json`), `i18n.resources.ts` con `en`, `es` y `fr`, DocFX, el submódulo `core-ui` y `Bonis.Tests` |
| Exploración | `code-explorer` en paralelo; lee `README.md` y `docs/*.md` |
| Ejecución | Build, `dotnet test -c Release` (unas 1056 pruebas), `yarn lint` y la comprobación de tipos. Debe encontrar por sí misma que `yarn build` no comprueba tipos y dar con el tsconfig temporal, o marcarlo `[REQUIRES-VALIDATION]` |
| Preguntas | Un solo bloque: qué lockfile vale (el pipeline usa yarn), contexto de negocio, quién despliega a producción, convenciones (`B0`–`B9`, `M0`–`M14`) |
| Pruebas | No crea proyecto de pruebas (ya existe). Propone el borrador de pruebas de componentes |
| Borrador | *Project context* con los 11 encabezados fijos y unas 150 líneas en total; los seis `docs/*.md` |
| DocFX | Propone añadir los `docs/*.md` a `toc.yml` y a `docfx.json`. **Acéptalo** para probarlo |
| Comprobación | `check_project.py` con 0 errores |

```powershell
python .agents\skills\project-context\scripts\check_project.py
git status --short
git diff --stat
```

### A.4 · Comparar

```powershell
Compare-Object (Get-Content $env:TEMP\AGENTS-referencia.md) (Get-Content AGENTS.md) | Measure-Object
```

Envíame:
- el `AGENTS.md` nuevo;
- los `docs/*.md`;
- `docs/docfx/toc.yml` y `docfx.json`;
- el registro de la sesión con `/context`.

Lo comparo con la referencia: qué acierta, qué falta, qué sobra y qué se inventa. Con eso
decidimos qué pasa al piloto. **No hagas commit todavía.**

---

## B · Calls4Grants (`new`, instalación real)

> **Con el kit v0.10.0** sigue la parte 4 de [`PASOS-v0.10.0.md`](PASOS-v0.10.0.md): son estos pasos
> actualizados, con la simulación previa y las respuestas preparadas.

### B.1 · Rama del piloto e instalación

```powershell
cd <ruta de Calls4Grants>
git switch dev; git pull --ff-only
git switch -c chore/sdd-kit-piloto
python <ruta>\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
```

Lo que se espera (es lo que hay que resolver):
- `CONFLICTO .claude/agents/qa-reviewer.md`: el de Clavijo. El kit no lo toca; lo resuelve
  `/project-context` en el paso 6.4.
- `PENDIENTE CLAUDE.md no importa @AGENTS.md`: igual.
- `creado AGENTS.md`, con *Project context* vacío.

Haz commit solo de lo del kit, revisando antes `git status --short`:

```powershell
git add .agents .github AGENTS.md .gitignore .gitmessage .sdd-kit.json docs/adr docs/sdd
git status --short
git commit -m "chore(sdd): instalar fi-sdd-standard v0.9.0"
```

### B.2 · Ejecutar

Cierra Claude Code y ábrelo de nuevo, en Calls4Grants. En una sesión nueva:

```text
/project-context
```

| Momento | Qué comprobar |
| --- | --- |
| Inventario | 5 proyectos .NET (`Api`, `Core`, `Domain`, `EntityFramework`, `Logic`), **ningún proyecto de pruebas**, npm, `i18n.generated.json` marcado como «parece generado», `core-ui` en la raíz, dos pipelines, y `CLAUDE.md` y `.claude/` con contenido |
| Exploración | CQRS (Commands y Queries), autorización, `ExceptionHandlingMiddleware`, `AntiXssMiddleware`, jobs de sincronización, frontend con stores |
| Conocimiento previo | Lee `CLAUDE.md`, `README.md`, los `docs/*.md` existentes y los skills `i18n` y `pbi` |
| Ejecución | Build de la solución, pruebas (todavía no hay), lint y comprobación de tipos del frontend con npm |
| Pruebas | Propone `FIniciativas.Calls4Grants.Tests` (xUnit v3 + Moq, mismo framework, referencias a `Logic` y `Core`), lo crea con `backend-dev` con una prueba de humo real y propone el paso `dotnet test` en el pipeline |
| Preguntas | Si `i18n.generated.json` se edita a mano o lo genera el skill o un script; contexto de negocio; despliegue |
| Configuración de Clavijo | Propone: `CLAUDE.md` → `@AGENTS.md` (su contenido pasa a `AGENTS.md`), retirar el `qa-reviewer` antiguo, conservar el skill `i18n` si genera traducciones, retirar `/pbi` y mantener los hooks |
| Documentación | Corrige y completa los seis `docs/*.md` que ya existen, con los encabezados fijos |
| Comprobación | `check_project.py` con 0 errores (el proyecto de pruebas ya existe) |

Si se retiró el `qa-reviewer` antiguo, vuelve a instalar para que se cree el del kit:

```powershell
python <ruta>\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
python .agents\skills\project-context\scripts\check_project.py
```

### B.3 · Qué enviar

- El registro de la sesión con `/context`.
- `AGENTS.md`, los `docs/*.md` y el `git diff --stat`.
- La salida de `dotnet test` del proyecto nuevo.

---

## Resultados

| # | Comprobación | Bonis | Calls4Grants |
| --- | --- | --- | --- |
| 1 | El inventario detecta lo esperado (lockfiles, traducciones, pruebas, DocFX, submódulos) | | |
| 2 | Exploración en paralelo; lee el conocimiento existente | | |
| 3 | Ejecuta todo y registra duración y línea base | | |
| 4 | Comandos de *Commands* verificados (ninguno inventado) | | |
| 5 | Preguntas en un bloque, solo lo que el código no dice | | |
| 6 | Proyecto de pruebas creado y en verde (solo Calls4Grants) | — | |
| 7 | Configuración previa migrada sin perder conocimiento (solo Calls4Grants) | — | |
| 8 | *Project context* con los 11 encabezados y ≤ 160 líneas en total | | |
| 9 | Los seis `docs/*.md` con hechos y fuente; `reglas-negocio.md` sin reglas inventadas | | |
| 10 | DocFX integrado (solo Bonis) | | — |
| 11 | `check_project.py` con 0 errores | | |
| 12 | Comparación con la referencia (aciertos · faltas · invenciones) | | — |
| 13 | Contexto y tiempo | | |
