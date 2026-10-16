# Pasos · kit v0.10.0: instalar, probar `/document-project` y `/project-context` en Calls4Grants

**Fecha:** 2026-10-15 · **Kit:** `fi-sdd-standard-v0.10.0.zip`

Todo se ejecuta en PowerShell desde `C:\Users\JuanCEBALLOS\Documents`, salvo que se diga otra cosa.
Las rutas de abajo suponen esta estructura; cambia `calls4grants` por el nombre real de la carpeta:

```text
Documents\
  fi-sdd-standard\     ← el kit (se sustituye por la v0.10.0)
  bonis_v2\
  calls4grants\
```

| Parte | Repositorio | Rama | Tiempo |
| --- | --- | --- | --- |
| 1 · Instalar el kit | — | — | 5 min |
| 2 · Commit de la versión | Bonis | `chore/sdd-kit-piloto` | 5 min |
| 3 · `/document-project` | Bonis | `chore/sdd-document-project-prueba` | 2 sesiones, 1–2 h |
| 4 · `/project-context` | Calls4Grants | `chore/sdd-kit-piloto` (nueva) | 1 sesión, 30–60 min |

Las partes 3 y 4 son repositorios distintos: puedes lanzar la 4 en otra ventana mientras esperas la 3.

**Reglas de siempre:** `git add` con rutas exactas (nunca `-A` ni `.`), revisa `git status --short`
antes de cada commit, y nada va a `dev` en esta prueba: todo se queda en local.

---

## 1 · Instalar el kit v0.10.0

```powershell
cd C:\Users\JuanCEBALLOS\Documents
Rename-Item fi-sdd-standard fi-sdd-standard-v0.9.3            # copia de seguridad de la versión anterior
Expand-Archive $env:USERPROFILE\Downloads\fi-sdd-standard-v0.10.0.zip -DestinationPath .
Get-Content fi-sdd-standard\VERSION
cd fi-sdd-standard; python scripts\validate.py; cd ..
```

Esperado:

```text
0.10.0
7 skills · 7 agents checked · 0 errors · 0 warnings
```

Si todo va bien, al final de la prueba puedes borrar `fi-sdd-standard-v0.9.3`.

---

## 2 · Bonis: actualizar el kit y hacer el commit de la versión

### 2.1 · Partir de un árbol limpio

```powershell
cd bonis_v2
git switch chore/sdd-kit-piloto
git status --short
```

No debe salir nada. Si sale algo, para y revísalo antes de seguir.

### 2.2 · Instalar

```powershell
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
```

Esperado (además de las líneas `igual`):

| Línea | Por qué |
| --- | --- |
| `creado .agents/skills/document-project/…` y `.claude/skills/document-project/…` | El skill nuevo, con `scripts/` y `templates/` |
| `actualizado .agents/skills/*/SKILL.md` (los 6 de antes) | La convención compartida nombra el skill nuevo |
| `actualizado AGENTS.md` | Una línea del bloque del kit (los skills que corren en la sesión principal) |
| `actualizado .github/agents/doc-writer.agent.md` y `.claude/agents/doc-writer.md` | `doc-writer` acepta símbolos «desde el código» |
| `actualizado .gitignore` | La copia local de Claude Code del skill nuevo |
| `actualizado .sdd-kit.json` | La versión |
| `Siguiente: /document-project …` | Ya hay contexto del proyecto y todavía no hay plan |

### 2.3 · Revisar y hacer el commit

```powershell
git status --short
```

Solo deben aparecer `.agents/`, `.github/agents/doc-writer.agent.md`, `AGENTS.md`, `.gitignore` y
`.sdd-kit.json`. `.claude/` no aparece porque está en `.gitignore`.

```powershell
git add .agents .github/agents AGENTS.md .gitignore .sdd-kit.json
git status --short
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.10.0"
git log --oneline -3
```

### 2.4 · Comprobar

```powershell
python .agents\skills\project-context\scripts\check_project.py
```

Esperado: `0 errores · 1 avisos` (el del tag `prod`, que sigue pendiente). `AGENTS.md` sigue en
184 líneas: el cambio fue dentro de una línea.

---

## 3 · Bonis: probar `/document-project`

La guía completa, con lo que hay que comprobar en cada momento, está en
`tests/pilots/bonis/PRUEBA-DOCUMENT-PROJECT.md`. Aquí van los pasos en orden.

### 3.1 · Rama de prueba

```powershell
git switch -c chore/sdd-document-project-prueba
```

### 3.2 · Ver los números antes de la sesión

El script no usa IA y no escribe nada en el repositorio. Tarda unos segundos:

```powershell
python .agents\skills\document-project\scripts\doc_coverage.py --areas --out $env:TEMP\cobertura.md
Select-String -Path $env:TEMP\cobertura.md -Pattern '^\| A-' | Measure-Object
Select-String -Path $env:TEMP\cobertura.md -Pattern 'dividir' | Measure-Object
```

Anota:
- las dos líneas de cobertura que imprime (código y pruebas);
- el número de áreas propuestas (`Count` del primer `Measure-Object`);
- cuántas están marcadas «dividir» (el segundo).

Abre `cobertura.md` y mira por encima la tabla *Áreas propuestas*. Si algo se ve muy raro (por
ejemplo, un área con 200 archivos), mándamelo antes de seguir: es más barato ajustar el script que
una sesión.

### 3.3 · Work item (opcional, recomendado)

Crea en Azure DevOps un PBI «Documentación inicial del proyecto» y anota su ID. Los commits de los
bloques lo citarán con `Ref: #<ID>`. Sin él, la prueba sirve igual.

### 3.4 · Sesión 1 — el plan

Cierra Claude Code y ábrelo de nuevo en `bonis_v2` (para que cargue el skill nuevo). En una sesión
nueva (Sonnet basta desde la v0.10.1):

```text
/document-project
```

Cuando pregunte:
- **Work item:** el ID del paso 3.3, o «ninguno».
- **Build, lint y tipos para la línea base:** sí.
- **Aprobación del plan:** revisa la tabla de áreas y bloques antes de decir que sí. Lo transversal
  del backend debe ir primero (`CustomBaseController`, autorización, excepciones, servicios
  compartidos, `ApplicationDbContext` y entidades). Migraciones, `core-ui` y `docs/modernizacion/`
  deben quedar fuera.
- **¿Empezar B-01 ahora?:** **no**. Se hace en otra sesión.

Al terminar, escribe `/context` y anota el tiempo. Comprueba:

```powershell
git status --short          # solo docs/sdd/_documentacion/plan.md (y quizá algún _borradores/)
```

**No hagas commit:** el plan va en el commit de B-01.

### 3.5 · Sesión 2 — el bloque B-01

Sesión nueva. Cambia de modelo y lanza el bloque:

```text
/model sonnet
/document-project
```

En la confirmación del bloque, antes de decir que sí, añade:

```text
No toques el comentario M8 de GetLanguage en CustomBaseController.cs: está en el borrador
centralizar-idioma y lo cambiará ese work item. Añadir un /// <summary> a GetLanguage sí está bien.
```

Al terminar: `/context` y el tiempo. El informe final da la línea `git add` con las rutas exactas:
cópiala, pero no la ejecutes todavía.

### 3.6 · Tu revisión

```powershell
git status --short
git diff --stat
git diff -U0 -- '*.cs' '*.ts' '*.tsx' > $env:TEMP\comentarios.diff
python .agents\skills\document-project\scripts\doc_coverage.py --out $env:TEMP\cobertura-despues.md
dotnet build Bonis.sln --no-incremental *> $env:TEMP\build-b01.txt
python .agents\skills\document-project\scripts\doc_coverage.py --warnings $env:TEMP\build-b01.txt --compare docs\sdd\_documentacion\avisos.md   # desde v0.10.2
```

1. `git diff --stat`: solo archivos de código del bloque, `docs/*.md` y `docs/sdd/`. Ningún
   `.csproj`, `.json` ni archivo fuera del bloque.
2. El build: el mismo número de avisos que la línea base de `plan.md`, o menos.
3. Abre `comentarios.diff` y lee **20 comentarios al azar** con el código al lado. Clasifícalos:
   correcto · impreciso · inventa (atribuye una intención, una regla o un comportamiento que el
   código no tiene). Un solo «inventa» en autorización o en reglas de negocio es un fallo.
4. `docs/api-reference.md`: los endpoints del bloque tienen propósito, roles, respuesta y errores.
5. DocFX, si lo usas: compila con la ruta de *Documentation* en `AGENTS.md`, sin avisos nuevos.
6. `git diff -- Bonis/Controllers/CustomBaseController.cs`: el comentario M8 sigue igual.

### 3.7 · Commit del bloque (en la rama de prueba)

El mensaje está en la sección *Mensaje de commit* de `docs/sdd/_documentacion/B-01.md`. Copia el
texto que está dentro del bloque ```` ```text ```` (sin las comillas) a `$env:TEMP\b01-msg.txt`.

```powershell
git add <rutas exactas del informe final> docs/sdd/_documentacion/
git status --short
git commit -F $env:TEMP\b01-msg.txt
cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"; (Get-Content $env:TEMP\msg.txt -Raw).Length
```

La longitud debe ser menor que 4000.

### 3.8 · Llevarlo al piloto

Solo si la revisión 3.6 salió bien:

```powershell
git switch chore/sdd-kit-piloto
git merge --ff-only chore/sdd-document-project-prueba
git branch -d chore/sdd-document-project-prueba
git log --oneline -4
```

Si la revisión sale mal, no lo mezcles: mándame el material y ajustamos el skill.

### 3.9 · Qué mandarme

1. El log de las dos sesiones y los dos `/context` con su tiempo.
2. `plan.md` y `B-01.md`.
3. `cobertura.md` y `cobertura-despues.md` (están en `%TEMP%`).
4. `comentarios.diff` y tu clasificación de los 20 comentarios.
5. La salida de `git diff --stat` (de antes del commit) o `git show --stat HEAD`.

---

## 4 · Calls4Grants: probar `/project-context` (instalación real)

Es la parte B de `tests/pilots/PRUEBA-PROJECT-CONTEXT.md`, ahora con la v0.10.0 y lo aprendido en
Bonis: presupuesto por sección, aviso a partir de 185 líneas y el modo `check`.

### 4.1 · Antes de empezar

En `calls4grants`:

```powershell
cd C:\Users\JuanCEBALLOS\Documents\calls4grants
git status --short                 # debe estar limpio
git fetch origin
git switch dev; git pull --ff-only
dotnet --version                   # compáralo con global.json, si existe
node --version; npm --version
git ls-files .claude CLAUDE.md     # qué parte de la configuración de Clavijo está versionada
```

Anota la salida del último comando: sirve para saber qué se podrá retirar con `git rm` en el paso
4.5.

### 4.2 · Rama del piloto y simulación

```powershell
git switch -c chore/sdd-kit-piloto
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude --dry-run
```

La simulación no escribe nada. Lo esperado:

| Línea | Qué significa | Quién lo resuelve |
| --- | --- | --- |
| `CONFLICTO .claude/agents/qa-reviewer.md` | Es el agente de Clavijo; el kit no lo toca | `/project-context`, paso 6.4 |
| `PENDIENTE CLAUDE.md no importa @AGENTS.md` | `CLAUDE.md` tiene su propio contenido | `/project-context`, paso 6.4 |
| `creado AGENTS.md` y `PENDIENTE … Project context` | Bloque del kit, contexto vacío | `/project-context` |
| `creado .agents/skills/…` (7 skills) y `.github/agents/…` | El kit | — |
| `actualizado .gitignore` | Copias locales de Claude Code | — |

Si sale algún otro `CONFLICTO`, mándamelo antes de seguir.

### 4.3 · Instalar y hacer el commit del kit

```powershell
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git config commit.template .gitmessage
git status --short
```

Deben salir `.agents/`, `.github/agents/`, `.github/prompts/`, `.gitignore`, `.gitmessage`,
`.sdd-kit.json`, `AGENTS.md`, `docs/adr/` y `docs/sdd/`. Nada más.

```powershell
git add .agents .github/agents .github/prompts AGENTS.md .gitignore .gitmessage .sdd-kit.json docs/adr docs/sdd
git status --short
git commit -m "chore(sdd): instalar fi-sdd-standard v0.10.0"
python .agents\skills\project-context\scripts\check_project.py
```

`check_project.py` dará errores (todavía no hay contexto ni proyecto de pruebas): es lo esperado. Los
resuelve el paso siguiente.

### 4.4 · Sesión de `/project-context`

Cierra Claude Code y ábrelo en `calls4grants`. En una sesión nueva (el skill pide Opus solo):

```text
/project-context
```

Respuestas preparadas para el bloque de preguntas (cámbialas si no son ciertas):

| Pregunta probable | Respuesta |
| --- | --- |
| Qué es el producto y quién lo usa | Un párrafo tuyo: qué hace Calls4Grants y para quién |
| Quién despliega a producción y cómo | Lo que sepas; si no, «no lo sé»: quedará `[REQUIRES-VALIDATION]` |
| `i18n.generated.json`: ¿a mano o generado? | Quién lo genera (el skill `i18n` de Clavijo o un script) y si se edita a mano |
| Archivo de bloqueo válido | El que use el pipeline (`npm`) |
| Idioma de los comentarios | Código existente en inglés; **código nuevo en español** (decisión 2 del brief) |
| Proyecto de pruebas | Sí: `<prefijo>.Tests` con xUnit v3 + Moq, con una prueba de humo real |
| Añadir `dotnet test` al pipeline | Que te enseñe el cambio; acéptalo si solo añade el paso de pruebas |
| `CLAUDE.md` → `@AGENTS.md` | Sí, después de pasar su conocimiento a `AGENTS.md` o `docs/` |
| `qa-reviewer` de Clavijo | Retirarlo (lo sustituye el del kit) |
| Skill `i18n` | Conservarlo si genera traducciones; citarlo en *Internationalization* |
| Skill `/pbi` | Retirarlo (lo sustituye `enrich-us`) |
| Hooks | Conservarlos hasta la fase 3 |

Lo que hay que comprobar durante la sesión:

| Momento | Esperado |
| --- | --- |
| Inventario | 5 proyectos .NET (`Api`, `Core`, `Domain`, `EntityFramework`, `Logic`), ningún proyecto de pruebas, npm, `i18n.generated.json` marcado como generado, `core-ui`, dos pipelines, `CLAUDE.md` y `.claude/` con contenido |
| Exploración | `code-explorer` en paralelo: CQRS, autorización, middlewares, jobs, stores del frontend |
| Conocimiento previo | Lee `CLAUDE.md`, `README.md`, los `docs/*.md` y los skills `i18n` y `pbi` |
| Ejecución | Build, lint y tipos del frontend; las pruebas, después de crear el proyecto |
| Proyecto de pruebas | Lo crea `backend-dev`; la sesión ejecuta `dotnet test` y sale en verde |
| Borrador | *Project context* con los 11 encabezados, cada sección dentro de su presupuesto, `AGENTS.md` por debajo de 185 líneas |
| Documentación | Corrige y completa los seis `docs/*.md` existentes (los escribe `doc-writer`) |
| Comprobación | `check_project.py` con 0 errores |

Al terminar: `/context` y el tiempo.

### 4.5 · Después de la sesión

Si la sesión retiró el `qa-reviewer` de Clavijo, vuelve a instalar para que se cree el del kit:

```powershell
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
python .agents\skills\project-context\scripts\check_project.py
```

Si quedan avisos, en una sesión nueva:

```text
/project-context check
```

Comprueba tú:

```powershell
dotnet test <ruta del proyecto de pruebas nuevo> > $env:TEMP\c4g-test.txt; Select-String -Path $env:TEMP\c4g-test.txt -Pattern 'Passed!|Failed!|Superado|Con errores'
(Get-Content AGENTS.md).Count
Get-Content CLAUDE.md
git status --short
git diff --stat
```

Esperado: pruebas en verde, `AGENTS.md` con menos de 185 líneas, `CLAUDE.md` con solo `@AGENTS.md`.

### 4.6 · Commit del contexto (en el piloto de Calls4Grants, solo local)

Con las rutas exactas de la línea `git add` del informe final. Los archivos retirados (agente,
skill `/pbi`) ya salen como `D` en `git status` si la sesión usó `git rm`; si salen como ` D`, añádelos
con su ruta.

```powershell
git add <rutas exactas del informe>
git status --short
git commit -m "chore(sdd): añadir el contexto del proyecto y la documentación base"
python .agents\skills\project-context\scripts\check_project.py
```

### 4.7 · Qué mandarme

1. El log de la sesión, `/context` y el tiempo.
2. La salida de la simulación del paso 4.2 y la del instalador.
3. `AGENTS.md`, `CLAUDE.md` y los seis `docs/*.md`.
4. `git show --stat HEAD` y la salida de `dotnet test`.
5. La salida final de `check_project.py`.

---

## Resumen de commits que quedan en local

| Repositorio | Rama | Commits |
| --- | --- | --- |
| Bonis | `chore/sdd-kit-piloto` | `chore(sdd): actualizar fi-sdd-standard a v0.10.0` · el de B-01 (si sale bien) |
| Calls4Grants | `chore/sdd-kit-piloto` | `chore(sdd): instalar fi-sdd-standard v0.10.0` · `chore(sdd): añadir el contexto del proyecto y la documentación base` |

Nada se sube a `origin` en esta prueba.
