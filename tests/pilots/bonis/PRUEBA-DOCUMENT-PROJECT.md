# Prueba de `/document-project` en Bonis · kit v0.10.0

**Objetivo:** comprobar que el plan sale bien partido y que un bloque documenta sin inventar, sin
cambiar código y sin avisos nuevos. Se prueban dos sesiones: el plan y el bloque B-01.

**Qué decide la prueba:**
- si las áreas y el orden que propone `doc_coverage.py` sirven o hay que ajustar el script;
- si un bloque cabe en una sesión (contexto y tiempo);
- si los comentarios «desde el código» son correctos o inventan intención;
- si el bloque se puede revisar como un PR normal.

## 0 · Preparación (5 min)

Desde `C:\Users\JuanCEBALLOS\Documents`, con el zip descomprimido en `fi-sdd-standard`:

```powershell
cd fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
git switch chore/sdd-kit-piloto
git status --short                     # debe estar limpio
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git status --short
```

Esperado: `validate.py` → `7 skills · 7 agents checked · 0 errors`. El instalador crea
`.agents/skills/document-project/` y actualiza los demás `SKILL.md`, `AGENTS.md` (una línea del
bloque del kit), `.github/agents/doc-writer.agent.md` y `.sdd-kit.json`. Al final sugiere
`/document-project`.

```powershell
git add .agents .github/agents AGENTS.md .sdd-kit.json
git status --short                     # solo esos archivos
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.10.0"
python .agents\skills\project-context\scripts\check_project.py     # 0 errores, 1 aviso (prod tag)
git switch -c chore/sdd-document-project-prueba
```

La prueba va en su propia rama, que sale del piloto. Si sale bien, se trae al piloto (paso 5).

**Antes de la sesión, mira los números** (tarda segundos y no escribe nada en el repositorio):

```powershell
python .agents\skills\document-project\scripts\doc_coverage.py --areas --out $env:TEMP\cobertura.md
Select-String -Path $env:TEMP\cobertura.md -Pattern '^\| A-' | Measure-Object   # nº de áreas propuestas
```

Anota la cobertura que da (código y pruebas) y el número de áreas.

**Work item (opcional, recomendado):** un PBI en Azure DevOps «Documentación inicial del proyecto».
Su ID se usa en los commits (`Ref: #<ID>`). Sin él, la prueba sirve igual.

## 1 · Sesión 1 — el plan (Claude Code, sesión nueva, Sonnet)

```text
/document-project
```

Si pregunta, responde: el ID del PBI (o «ninguno»), sí a ejecutar build, lint y tipos para la línea
base, y **no** a empezar B-01 en esta sesión.

Comprueba en la conversación y en `docs/sdd/_documentacion/plan.md`:

| # | Qué mirar | Esperado |
| --- | --- | --- |
| 1 | Precondiciones | Comprueba `check_project.py` y lee *Project context* |
| 2 | Línea base | Build 0 errores / ~222 avisos; CS1591 si Bonis genera el XML; lint ~173; tipos ~148; DocFX si está instalado |
| 3 | Áreas | Una por controlador o grupo de controladores; ninguna de más de ~15 archivos sin justificar |
| 4 | Transversales primero | `CustomBaseController`, autorización (`AuthorizeRoles…`), excepciones y `GlobalExceptionHandler`, servicios compartidos, `ApplicationDbContext` y entidades |
| 5 | Fuera del plan | Migraciones, código generado, submódulos y rutas protegidas |
| 6 | Bloques | 3 a 5 áreas, ≤ ~40 archivos cada uno |
| 7 | `docs/` por área | Cada área dice qué sección de `api-reference.md`, `database.md` o `frontend.md` completa |
| 8 | Nada escrito sin aprobación | `plan.md` aparece solo después de tu «sí» |
| 9 | Plan comprobado | `doc_coverage.py --check-plan` con 0 errores (desde v0.10.1) |

Al terminar: `/context` y el tiempo. **No hagas commit:** el plan va en el commit de B-01.

## 2 · Sesión 2 — el bloque B-01 (sesión nueva, Sonnet)

`/model sonnet` y después:

```text
/document-project
```

Debe tomar B-01 (el primer bloque transversal). En la confirmación, añade:

```text
No toques el comentario M8 de GetLanguage en CustomBaseController.cs: está en el borrador
centralizar-idioma y lo cambiará ese work item.
```

Es también una prueba: la sesión debería haber encontrado el borrador y no duplicar el hallazgo.

Comprueba:

| # | Qué mirar | Esperado |
| --- | --- | --- |
| 1 | Hechos por área | `doc_coverage.py --files` y una pregunta de `code-explorer` por área |
| 2 | Paquetes | `doc-writer` con ≤ 15 archivos por paquete, como mucho 2 a la vez, archivos disjuntos |
| 3 | `comment_only.py check` | «Solo cambiaron comentarios» |
| 4 | Build | Sin avisos nuevos; CS1591 baja; ningún CS1570–CS1587 |
| 5 | Revisión de afirmaciones | La sesión lee el diff de comentarios y devuelve lo que no tiene base |
| 6 | Hallazgos | En *Hallazgos* de `plan.md`; los conocidos citan su borrador |
| 7 | Registro | `B-01.md` con validación, *Sin documentar* y el mensaje de commit entero |
| 8 | Comentario M8 | Igual que antes |

Al terminar: `/context` y el tiempo.

## 3 · Tu revisión (la parte que más importa)

```powershell
git status --short
git diff --stat
git diff -U0 -- '*.cs' '*.ts' '*.tsx' > $env:TEMP\comentarios.diff
python .agents\skills\document-project\scripts\doc_coverage.py --out $env:TEMP\cobertura-despues.md
```

Lee 20 comentarios al azar del diff, con el código al lado, y clasifícalos:

| Clase | Qué es |
| --- | --- |
| Correcto | Dice lo que hace el código, sin más |
| Impreciso | Cierto pero vago, o le falta un caso (una excepción, un 403) |
| Inventa | Atribuye una intención, una regla de negocio o un comportamiento que el código no tiene |

Un solo «Inventa» en autorización o en una regla de negocio es un fallo de la prueba, aunque el
resto esté bien. Mira también:
- `docs/api-reference.md`: los endpoints de B-01 tienen propósito, roles, respuesta y errores;
- la compilación de DocFX, si la usas: `docfx build` con la ruta que dice *Documentation* en
  `AGENTS.md`.

## 4 · Commit del bloque (en la rama de prueba)

Con las rutas exactas que da el informe final, nunca `git add -A`:

```powershell
git add <archivos del informe> docs/sdd/_documentacion/
git status --short
```

El mensaje está en la sección *Mensaje de commit* de `docs/sdd/_documentacion/B-01.md`. Cópialo a un
archivo y úsalo entero:

```powershell
git commit -F $env:TEMP\b01-msg.txt
cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"; (Get-Content $env:TEMP\msg.txt -Raw).Length   # < 4000
```

## 5 · Llevarlo al piloto

Si la prueba sale bien:

```powershell
git switch chore/sdd-kit-piloto
git merge --ff-only chore/sdd-document-project-prueba
git branch -d chore/sdd-document-project-prueba
```

Los bloques no van todavía a `dev` por PR: los `docs/*.md` de `/project-context` solo están en el
piloto, y un cherry-pick a `dev` chocaría. Irán con el PR del piloto, o bloque a bloque cuando el
contexto del proyecto esté en `dev` (ver la guía git, «Bloques de `/document-project`»).

## 6 · Qué mandarme

1. El log de las dos sesiones (o lo que veas raro) y los dos `/context` con su tiempo.
2. `plan.md` y `B-01.md`.
3. `cobertura.md` (antes) y `cobertura-despues.md`.
4. `comentarios.diff` y tu clasificación de los 20 comentarios.
5. La salida de `git diff --stat`.

## Resultados (se rellena después)

| Medida | Plan | B-01 |
| --- | --- | --- |
| Tiempo | | |
| Contexto (`/context`) | | |
| Áreas / bloques | | — |
| Símbolos documentados (antes → después) | — | |
| CS1591 (antes → después) | — | |
| Avisos de build nuevos | — | |
| Comentarios devueltos a `doc-writer` | — | |
| Muestra de 20: correcto / impreciso / inventa | — | |
| Hallazgos nuevos / ya conocidos | — | |
