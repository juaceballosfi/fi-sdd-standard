# Prueba del bloque 3 de la fase 2 · `qa-review`, `qa-reviewer` y `runtime-tester` · kit v0.7.0

**Objetivo:** comprobar que `qa-review` hace una revisión independiente:
- en una sesión nueva;
- con un revisor que lee el diseño por su cuenta;
- con cada hallazgo verificado antes de escribirse;
- con la decisión de la persona sobre cada hallazgo alto o medio.

También se prueba el bucle de QA si hay algo que corregir.

**Work item:** 40933, ya mezclado en `dev` (PR 14468). Se revisa el rango del squash:
- `base` = `9e07c66d` (PR 14465, el commit anterior).
- `head` = `99e5da20` (PR 14468).

En `chore/sdd-kit-piloto` el código de Bonis es idéntico a `99e5da20`: lo comprobaste con
`git diff dev --stat -- Bonis Bonis.Tests`. Así el revisor puede ejecutar las pruebas.

**Dónde:** rama `chore/sdd-kit-piloto` de Bonis, en PowerShell, desde la raíz (`bonis_v2`), con el
kit en `..\fi-sdd-standard`.

## 1 · Instalar

```powershell
cd ..\fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git status --short
```

Lo que debe mostrar el instalador:

| Acción | Archivos |
| --- | --- |
| `creado` | `.agents/skills/qa-review/` (SKILL.md y `templates/qa-report.md`) y su copia en `.claude/skills/qa-review/` |
| `creado` | `.github/agents/qa-reviewer.agent.md`, `.github/agents/runtime-tester.agent.md` y sus copias en `.claude/agents/` |
| `actualizado` | Los tres skills (v3.6), `backend-dev`, `frontend-dev`, `AGENTS.md` (solo el bloque del kit) y `.sdd-kit.json` |
| `.gitignore` | `+1 líneas` (skill) y `+2 líneas` (agentes) |

Si `AGENTS.md` sale como `PENDIENTE` (sin las marcas del kit), copia a mano la regla nueva de la
sección *SDD flow*: «`qa-review` runs in a new session, never in the one that implemented the change».

Commit solo con los archivos del kit. Las carpetas nuevas se añaden con `git add`:

```powershell
git add .agents .github/agents AGENTS.md .gitignore .sdd-kit.json
git status --short       # nada del kit en «??» ni en « M»; .claude/ no aparece (está ignorado)
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.7.0"
```

Cierra Claude Code y ábrelo de nuevo. Pregunta «¿Qué subagentes tienes disponibles?». Deben salir:
`code-explorer`, `backend-dev`, `frontend-dev`, `qa-reviewer` y `runtime-tester`.

## 2 · Ejecutar la revisión

En una **sesión nueva**, no en la que hizo `wbs-execution`:

```text
/qa-review 40933 base:9e07c66d head:99e5da20
```

| Momento | Qué comprobar |
| --- | --- |
| Paso 0 | Comprueba que el código de `head` es el del árbol de trabajo y que, por tanto, se pueden ejecutar las pruebas. El alcance son los 5 archivos de código (1 nuevo); `docs/sdd/` queda fuera del código revisado |
| Confirmación | Ronda 1 · revisor `qa-reviewer` · propone o no `runtime-tester`, con el motivo |
| `runtime-tester` | Si te lo propone, **acéptalo**. Aprueba solo `docker-compose up -d`, `dotnet run`, `curl` / `Invoke-WebRequest` y parar procesos. Rechaza cualquier cambio de configuración. Es válido que devuelva «No ejecutado (motivo)»: en Debug el usuario y los roles son fijos y quizá no pueda simular un delegado |
| Paquete del revisor | Le da fuentes (carpeta, rango, comandos, `AGENTS.md`), no conclusiones: ni los informes de los agentes de implementación ni opiniones |
| Informe del revisor | Cada hallazgo trae `ruta:línea`, la regla o el SPEC, un escenario y cómo se confirmó. Trae la cobertura de SPEC-01 a SPEC-12 |
| Verificación | La sesión principal abre las líneas de cada hallazgo y confirma, ajusta o descarta con motivo. Nada se borra |
| Ya conocidos | El aviso `unicode-bom` y el TS2345 de `add.tsx`/`identification.tsx` ya estaban antes y están en el CHANGELOG: **no deberían salir como hallazgos** |
| `qa-report.md` | Tiene el sello, el alcance, la tabla de hallazgos, «Qué se revisó» y la tabla de ejecución. En `bitacora.md`, una sola línea |
| Decisiones | Te pregunta por cada hallazgo alto o medio: A corregir · Aceptado · Borrador |
| Al terminar | Añade una línea de QA en **Pruebas** de `commit-message.md` y da las rutas exactas para el commit |

Después:

```powershell
python ..\fi-sdd-standard\scripts\check-sdd-item.py docs\sdd\40933-correcciones-rol-delegado
git status --short
```

- El comprobador debe dar «listo para commit» solo si no queda ningún hallazgo alto o medio sin
  decidir.
- `git status` **solo** debe mostrar cambios en `qa-report.md` (nuevo), `bitacora.md` y
  `commit-message.md`. Nada de código: `qa-review` no edita.
- Si arrancó la aplicación: nada en `appsettings*` y ningún proceso `dotnet` o `node` que siga
  abierto.

## 3 · Bucle de QA (solo si hay hallazgos «A corregir»)

1. **Sesión nueva:** `/wbs-execution 40933 qa`. Comprueba que:
   - corrige cada hallazgo con el agente de su capa y primero escribe la prueba que lo reproduce;
   - verifica como en el bloque 2;
   - marca `Corregido (fecha)` en `qa-report.md`;
   - deja el mensaje de commit preparado como commit de seguimiento, porque el 40933 ya está en
     `dev`.
2. **Otra sesión nueva:** `/qa-review 40933 base:HEAD`. Así revisa solo las correcciones, que
   todavía no tienen commit. Debe ser la ronda 2: `Corregido (verificado …)` o vuelve a `Abierto`.
3. **Subir el seguimiento:** se hace como en `docs/guias/git-por-work-item.md`, variante B:
   - commit en el piloto;
   - rama `feature/40933-correcciones-qa` desde `origin/dev`;
   - *cherry-pick* y PR.

Si no hay nada que corregir, haz el commit del informe en la rama del piloto. Llegará a `dev` con
el PR del kit:

```powershell
git add docs/sdd/40933-correcciones-rol-delegado/qa-report.md docs/sdd/40933-correcciones-rol-delegado/bitacora.md docs/sdd/40933-correcciones-rol-delegado/commit-message.md
git commit -m "docs(sdd): añadir la revisión de QA del 40933" -m "Ref: #40933"
```

## 4 · Resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos y 5 agentes visibles | | |
| 2 | Alcance correcto: 5 archivos y pruebas ejecutables | | |
| 3 | Paquete con fuentes, sin conclusiones | | |
| 4 | Hallazgos con `ruta:línea`, regla, escenario y confirmación | | |
| 5 | La sesión principal verifica cada hallazgo (y descarta con motivo) | | |
| 6 | No salen como hallazgos los problemas ya conocidos | | |
| 7 | `runtime-tester`: lo que probó, o «No ejecutado» con el motivo; procesos parados | | |
| 8 | `qa-report.md` completo y una línea en la bitácora | | |
| 9 | `qa-review` no tocó código (`git status`) | | |
| 10 | Comprobador: estado correcto según las decisiones | | |
| 11 | Bucle de QA (si lo hubo): modo `qa` y ronda 2 | | |
| 12 | Contexto de la sesión al terminar (`/context`) y tiempo | | |
| 13 | ¿Encontró algo que no vio la verificación del bloque 2? | | |

## 5 · Qué enviar

- El registro de la sesión de `qa-review`, con `/context` al final. Si hubo bucle, también los de
  las otras sesiones.
- `qa-report.md` y `git status --short` al terminar.
- La tabla de resultados.
