# Guía git · de un work item terminado a `dev`

**Para:** desarrolladores que usan el flujo SDD con Azure Repos y PowerShell en Windows.
**Decisiones:**
- ADR-0004: un commit por work item, `Ref: #id` y nunca `fix #id`.
- ADR-0006: rama `feature/<id>-<título>` desde `dev`, PR a `dev` y squash merge.

**Ejemplo real:** PBI 40933, que acabó en el PR 14468, el 2026-10-14.

Todos los comandos se ejecutan **desde la raíz del repositorio**, por ejemplo `bonis_v2`, no
`bonis_v2\Bonis`. El kit está al lado, en `..\fi-sdd-standard`.

En los comandos de abajo sustituye:

| Marcador | Ejemplo |
| --- | --- |
| `<carpeta>` | `docs/sdd/40933-correcciones-rol-delegado` |
| `<id>` | `40933` |
| `<rama>` | `feature/40933-correcciones-rol-delegado` (el mismo nombre que la carpeta) |

---

## A · Flujo normal: trabajas desde el principio en la rama del work item

Este es el flujo para cuando el kit ya está en `dev`.

### A.1 · Crear la rama antes de empezar

```powershell
git fetch origin
git switch -c <rama> origin/dev
git push -u origin <rama>    # crea la rama remota; desde aquí ya sigue a la suya y no a dev
```

Si ya hiciste `git switch -c … origin/dev` sin el push, la rama sigue a `origin/dev`. El primer
`git push -u origin <rama>` lo corrige.

### A.2 · Antes del commit

```powershell
python ..\fi-sdd-standard\scripts\check-sdd-item.py <carpeta>
git status --short
```

- El comprobador debe dar 0 errores. Arregla los avisos de marcadores abiertos antes del commit.
- `git status` solo debe mostrar los archivos de código del work item y su carpeta.

### A.3 · Un solo commit, con las rutas exactas

```powershell
git add <archivo1> <archivo2> ... <carpeta>
git status --short           # todo en verde (staged) y nada en «??» que sea del work item
git commit -F <carpeta>/commit-message.md
```

- Nunca uses `git add -A` ni `git add .`, porque se colarían archivos ajenos al work item.
- Las rutas exactas salen de `git status --short` o del apartado «Archivos» del cierre de
  `wbs-execution`.
- Los archivos nuevos (`??`) hay que añadirlos con `git add`: `git commit -- <rutas>` no los
  incluye.
- De la carpeta, git no añade `assets/`, `commit-message.md` ni `test-cases.csv` (ADR-0027): están
  en `.gitignore`. `git commit -F` lee `commit-message.md` del disco igualmente.
- Si la rama tiene borradores en `docs/sdd/_borradores/`, crea antes cada work item en Azure DevOps,
  anota su ID donde se citaba el borrador y bórralo (`git rm`): `pr-check.py` da error si llegan al PR.

### A.4 · Comprobar el commit

```powershell
git log --oneline origin/dev..HEAD
cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"
python ..\fi-sdd-standard\scripts\check-sdd-item.py <carpeta> --commit-message $env:TEMP\msg.txt --id <id>
python ..\fi-sdd-standard\scripts\check-encoding.py --base origin/dev
```

- El primer comando debe mostrar **una sola línea**.
- Si muestra varias, júntalas en una con `git reset --soft origin/dev` y vuelve a hacer el commit
  con `-F`. Esto solo antes del push; después el squash del PR las junta igualmente.
- Usa `cmd /c`: el `>` de PowerShell 5.1 estropea las tildes del mensaje.

Si `dev` avanzó desde que hiciste las pruebas, vuelve a ejecutarlas sobre tu rama:

```powershell
git fetch origin
git log --oneline HEAD..origin/dev     # si sale algo, dev avanzó
git rebase origin/dev                  # antes del push; con el PR ya abierto, git merge origin/dev
dotnet test Bonis.Tests -c Release
cd Bonis\ClientApp; yarn lint; cd ..\..
```

### A.5 · Push

```powershell
git push -u origin <rama>
git status -sb      # debe decir ## <rama>...origin/<rama>
```

Escribe siempre `-u origin <rama>`, nunca un `git push` sin más.

### A.6 · PR en Azure Repos

1. Abre el enlace que muestra el push, o ve a **Repos → Pull requests → New**, de `<rama>` a
   `dev`.
2. **Título:** la primera línea del mensaje de commit.
3. **Descripción:** el resto del mensaje. Este comando lo copia al portapapeles con las tildes
   bien:
   ```powershell
   Get-Content -Encoding UTF8 <carpeta>\commit-message.md | Select-Object -Skip 2 | Set-Clipboard
   ```
4. **Work items:** enlaza el `#<id>`.
5. **Reviewers:** los del equipo.
6. Si hay `qa-report.md`, menciona su resultado en la descripción (lo añade `qa-review`).
7. Al aprobarse, **Complete → Squash commit**. Comprueba que el mensaje mantiene `Ref: #<id>`.
   Deja marcada «Delete source branch».

### A.7 · Después del merge

```powershell
git fetch origin --prune
git switch dev
git merge --ff-only origin/dev
git log --oneline -3          # arriba: «Merged PR NNNNN: <primera línea>»
git branch -D <rama>
```

- `-D` (y no `-d`) es necesario porque, con squash, git no reconoce la rama como mezclada. Es
  seguro cuando el PR está completado.
- Las líneas `- [deleted] (none) -> origin/...` de `--prune` son normales: borran las referencias
  locales a ramas que ya no existen en el remoto.

---

## B · Variante del piloto: trabajas en una rama local con el kit

Es lo que se hace mientras el kit vive en `chore/sdd-kit-piloto`, una rama solo local que irá a
`dev` con su propio PR al final. El código del work item se lleva a una rama limpia desde `dev`
con *cherry-pick*, para que el PR no arrastre archivos del kit.

### B.1 · Commit en la rama del piloto

Igual que en A.2 y A.3, en `chore/sdd-kit-piloto`. Después guarda el hash:

```powershell
$h = git rev-parse HEAD
```

### B.2 · Rama limpia desde `dev` y cherry-pick

```powershell
git fetch origin
git switch -c <rama> origin/dev
git cherry-pick $h
```

Si el *cherry-pick* da conflicto, es porque el commit tocó archivos del kit. Cancélalo con
`git cherry-pick --abort` y rehaz el commit del piloto solo con las rutas del work item.

### B.3 · Comprobaciones

Las de A.4 y, además:

```powershell
git log --oneline chore/sdd-kit-piloto..origin/dev   # si sale algo, dev cambió desde tus pruebas
git status --short                                   # «?? .claude/» es normal aquí: no lo añadas
```

En `dev` todavía no está la línea del `.gitignore` que añade el instalador para `.claude/`.

### B.4 · Push y PR

Como en A.5 y A.6.

### B.5 · Después del merge: traer `dev` al piloto

```powershell
git fetch origin --prune
git switch dev
git merge --ff-only origin/dev
git switch chore/sdd-kit-piloto
git merge --no-edit dev
git log --oneline --graph -6
```

No debería haber conflictos: el piloto ya tiene el mismo cambio que el squash.

Comprueba que el código quedó igual que en `dev`:

```powershell
git diff dev --stat -- Bonis Bonis.Tests <carpeta>   # vacío
git diff dev --stat                                   # solo archivos del kit
git status --short                                    # vacío
git branch -D <rama>
```

La rama del piloto es local: **no hagas push de ella** hasta el PR final del kit.

---

## Bloques de `/document-project`

Cada bloque es como un work item: una rama, un commit y un PR. Cambian solo los marcadores:

| Marcador | Valor |
| --- | --- |
| `<carpeta>` | `docs/sdd/_documentacion` (el plan y el `B-NN.md` del bloque) |
| `<id>` | el PBI «Documentación inicial del proyecto», si existe |
| `<rama>` | `docs/<id>-documentacion-b01` (sin work item: `docs/documentacion-b01`) |

- Un bloque nuevo empieza desde `dev` actualizado, con el bloque anterior ya mezclado.
- El mensaje sale entero de la sección *Mensaje de commit* de `B-NN.md`.
- En el piloto (variante B), los bloques necesitan que los `docs/*.md` de `/project-context` ya
  estén en `dev`; mientras no lo estén, el bloque se queda en la rama del piloto.

---

## C · Avisos que no son errores

| Mensaje | Qué significa |
| --- | --- |
| `LF will be replaced by CRLF the next time Git touches it` | Conversión de finales de línea de Windows. Inofensivo |
| `branch '<rama>' set up to track 'origin/dev'` | Normal al crear la rama desde `origin/dev`. El `push -u` lo cambia |
| `- [deleted] (none) -> origin/...` en `fetch --prune` | Limpieza de referencias locales a ramas borradas en el remoto |
| `?? .claude/` en una rama sacada de `dev` | Copias locales de Claude Code; `dev` aún no las ignora. No se añaden |
| Azure muestra `utf-8 -> Windows-1252` en un archivo | Heurística de Azure. Si `check-encoding.py` dice UTF-8, está bien |
| Tildes como `├®` o `├│` en la salida de `git diff … \| Select-String` | Es cómo la consola de PowerShell muestra UTF-8, no el archivo. Confírmalo con `check-encoding.py` |
| Tildes rotas en `msg.txt` | Se sacó con `>` de PowerShell. Usa `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"` |

## D · Lo que nunca se hace

- Push directo a `dev` o `main`: todo entra por PR.
- `git add -A` o `git add .` en un work item.
- `fix #id`, `fixes #id` o `closes #id` en el mensaje, porque Azure Repos cerraría el work item.
- Trailers de IA (`Co-Authored-By`): la evidencia es el sello «Generado con» de la carpeta.
- Dejar que la IA haga commit, push o cambie de rama: lo hace la persona (AGENTS.md).
