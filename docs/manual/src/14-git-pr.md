# Git, commit y PR

:::lead
La IA prepara el mensaje de commit y te da los comandos con rutas exactas, pero el commit, el push y
el PR los haces tú. Este capítulo recoge el formato del mensaje, el camino de un work item terminado
hasta `dev` y cómo llevar el kit de un piloto a `dev`.
:::

## El mensaje de commit

Un work item, **un commit** (ADR-0004). El mensaje sigue `.gitmessage` y se reutiliza como
descripción del PR. `wbs-execution` y `quick-fix` lo escriben completo en `commit-message.md` desde
el `CHANGELOG.md`; `qa-review` y `document-code` solo añaden una viñeta.

:::file docs/sdd/40399-…/commit-message.md
feat(menu): añadir la sección de ofertas al menú lateral

PBI-40399 — [MENÚ] Sección de ofertas en el menú lateral

**Problema**
Los comerciales no tenían acceso directo a sus ofertas: debían entrar por Clientes.

**Cambios**
- Backend (Permissions.cs): permiso ViewOffers para Comercial y Jefe de ventas.
- Frontend (SideMenu.tsx): entrada «Ofertas» bajo «Clientes», visible con ViewOffers.
- Traducciones (es.json, fr.json): clave «Offers» en todos los idiomas.
- Documentación: comentarios en 2 archivos; docs/frontend.md.

**Alcance y no regresión**
- No cambian las rutas del API ni los permisos existentes.

**Pruebas**
- PermissionsTests: 3 nuevas (Rojo → verde). dotnet test: 301/301.
- SideMenu.test.tsx: 3 casos por rol. yarn test: 51/51 · lint y tipos OK.
- Revisión de QA (qa-review, ronda 2): sin hallazgos altos ni medios.

Ref: #40399
:::

| Regla | Por qué |
| --- | --- |
| Primera línea `tipo(ámbito): descripción`, minúscula, imperativo, sin punto, ≤ 72 caracteres | Legible en `git log --oneline` y como título del PR |
| `tipo`: `feat` · `fix` · `refactor` · `perf` · `docs` · `test` · `chore` · `ci` · `style` · `revert` | Clasificar el cambio |
| Segunda línea en blanco y luego `PBI-<id> — [MÓDULO] <título>` (o `BUG-<id>`) | Enlaza con el work item a simple vista |
| Rótulos en negrita (**Problema**, **Causa**, **Cambios**, **Alcance y no regresión**, **Pruebas**), nunca `#` | Git borra las líneas que empiezan por `#` |
| **Pruebas**: solo lo que se ejecutó de verdad | Es evidencia, no una promesa |
| Última línea `Ref: #<id>` | Enlaza el work item **sin cambiar su estado** |
| Nunca `fix #id`, `fixes #id`, `fixed #id` | Azure Repos cerraría el work item |
| Sin `Co-Authored-By` ni «Generated with» | El sello SDD es la evidencia (ADR-0004) |
| Todo el mensaje < 4000 caracteres | Es la descripción del PR |

## De un work item terminado a dev

### 1 · Rama, antes de empezar

```powershell
git fetch origin
git switch -c feature/40399-seccion-ofertas origin/dev
git push -u origin feature/40399-seccion-ofertas
```

### 2 · Antes del commit

```powershell
python .agents\scripts\check-sdd-item.py docs\sdd\40399-seccion-de-ofertas-en-el-menu-lateral   # 0 errores
git status --short     # solo el código del work item y su carpeta
```

**Borradores.** Si alguna skill dejó propuestas en `docs/sdd/_borradores/`, crea ahora cada work
item en Azure DevOps y anota su ID donde se citaba el borrador: una línea en `bitacora.md` y, si
venía de QA, el estado del hallazgo en `qa-report.md` (`Work item #41100`). Después borra el
borrador (`git rm`, o bórralo sin más si nunca se versionó). Los borradores no llegan a `dev`:
`pr-check.py` da error si encuentra uno en la rama.

### 3 · Un solo commit, con rutas exactas

Copia el `git add` que te dio la skill al cerrar (o construye la lista desde `git status --short`):

```powershell
git add Api/Authorization/Permissions.cs MiProyecto.Tests/Authorization/PermissionsTests.cs `
        ClientApp/src/layout/SideMenu.tsx ClientApp/src/layout/SideMenu.test.tsx `
        ClientApp/src/i18n/es.json ClientApp/src/i18n/fr.json docs/frontend.md `
        docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
git status --short     # nada del work item en «??» ni sin preparar
git commit -F docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/commit-message.md
```

Al añadir la carpeta del work item, git salta lo que no se versiona (ADR-0027): `assets/`,
`commit-message.md` y `test-cases.csv` están en el `.gitignore`. `git commit -F` lee
`commit-message.md` de tu disco igualmente, y el mensaje queda guardado en el commit.

:::danger Nunca git add -A ni git add .
Se colarían archivos ajenos: copias locales de `.claude/`, logs, un `.env`. Y recuerda que los
archivos nuevos (`??`) hay que añadirlos con `git add`: `git commit -- <rutas>` no los incluye.
:::

### 4 · Comprobar

```powershell
git log --oneline origin/dev..HEAD                 # una sola línea
python .agents\scripts\pr-check.py                 # 0 errores
```

Si hay varios commits, júntalos antes del push: `git reset --soft origin/dev` y vuelve a hacer el
commit con `-F`. Si `dev` avanzó, `git rebase origin/dev` y vuelve a pasar las pruebas.

### 5 · Push y PR

```powershell
git push -u origin feature/40399-seccion-ofertas
Get-Content -Encoding UTF8 docs\sdd\40399-…\commit-message.md | Select-Object -Skip 2 | Set-Clipboard
```

En Azure Repos: **New pull request** de la rama a `dev`. Título: la primera línea del mensaje.
Descripción: el resto (ya está en el portapapeles). Enlaza el work item `#40399`, añade revisores y,
al aprobarse, **Complete → Squash commit** comprobando que el mensaje conserva `Ref: #40399`.

### 6 · Después del merge

```powershell
git fetch origin --prune
git switch dev; git merge --ff-only origin/dev
git branch -D feature/40399-seccion-ofertas      # -D: con squash, git no la ve como mezclada
```

El PO valida los criterios de aceptación en el entorno de `dev` (G4) y el work item avanza en
Azure DevOps a mano.

## Commits de seguimiento

| Situación | Mensaje |
| --- | --- |
| Correcciones de QA después de mezclar | `fix(<ámbito>): corregir hallazgos de QA` · solo las correcciones · `Ref: #<id>` |
| Documentación después de mezclar | `docs(<ámbito>): documentar <qué>` · `Ref: #<id>` |
| Un bloque de `/document-project` | `docs(<ámbito>): documentar <áreas>` · `Ref: #<id del PBI de documentación>` |
| Instalar o actualizar el kit | `chore(sdd): instalar fi-sdd-standard v<versión>` / `actualizar … a v<versión>` |
| Contexto del proyecto | `chore(sdd): añadir el contexto del proyecto y la documentación base` |

## Llevar el piloto a dev

Mientras se prueba, el kit puede vivir en una rama local (`chore/sdd-kit-piloto`). Para que el
equipo lo use, entra en `dev` con un PR como cualquier cambio:

```powershell
git fetch origin
git switch chore/sdd-kit-piloto
git merge origin/dev
python .agents\skills\project-context\scripts\check_project.py   # 0 errores
dotnet build <solución> --no-incremental; dotnet test <pruebas>
git switch -c chore/sdd-kit-en-dev
git push -u origin chore/sdd-kit-en-dev
python .agents\scripts\pr-check.py --base origin/dev
```

- **Entra:** `.agents/`, `.github/agents/`, `.github/prompts/`, `.claude/settings.json`,
  `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`, `sdd-guardrails.json` y `docs/`.
- **No entra:** `.claude/skills/`, `.claude/agents/` (copias locales), `.claude/settings.local.json`,
  `.github/copilot-instructions.md` y, de `docs/sdd/`, los `assets/`, `commit-message.md`,
  `test-cases.csv` y `_borradores/` (ADR-0027). Si alguno ya estaba versionado en el piloto,
  quítalo del índice antes del PR (capítulo 5, *Si el proyecto ya versionaba esos archivos*).
- **Squash**, con `chore(sdd): adoptar fi-sdd-standard v<versión> en <proyecto>`. Sin work item,
  el aviso de `pr-check.py` sobre `Ref:` es esperado.
- **Revisor:** el tech lead. Revisa a mano `sdd-guardrails.json`.

Mientras trabajas en la rama del piloto, el código de cada work item se lleva a una rama limpia
desde `dev` con *cherry-pick* para que su PR no arrastre archivos del kit (guía
`docs/guias/git-por-work-item.md`, variante B).
