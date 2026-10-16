# Scripts

:::lead
Los scripts hacen la parte que no debe depender de la IA: instalar, crear la carpeta de un work
item, comprobar artefactos y commits, medir cobertura, demostrar que solo cambiaron comentarios.
Son Python sin dependencias externas, dan siempre el mismo resultado y salen con código 0 (bien) o
1 (errores).
:::

## Dónde está cada uno

| Script | Dónde | Lo ejecuta | Para qué |
| --- | --- | --- | --- |
| `install.py` | Kit: `scripts/` | Tú | Instalar o actualizar el kit (capítulo 5) |
| `validate.py` | Kit: `scripts/` | Responsable del kit | Validar el propio kit |
| `new-sdd-item.py` | Kit: `scripts/` | Tú | Crear la carpeta de un work item |
| `check-sdd-item.py` | Kit y `.agents/scripts/` | Tú y las skills | Comprobar los artefactos de un work item o un mensaje de commit |
| `check-encoding.py` | Kit y `.agents/scripts/` | Tú y `pr-check.py` | Comprobar (y reparar) UTF-8 |
| `pr-check.py` | Kit y `.agents/scripts/` | Tú, antes del PR | Las reglas obligatorias de una rama |
| `inventory.py` | `.agents/skills/project-context/scripts/` | `project-context` | Inventario del repositorio |
| `check_project.py` | `.agents/skills/project-context/scripts/` | `project-context`, `document-project`, tú | Comprobar el contexto del proyecto |
| `comment_only.py` | `.agents/skills/document-code/scripts/` | `document-code`, `document-project` | Probar que solo cambiaron comentarios |
| `doc_coverage.py` | `.agents/skills/document-project/scripts/` | `document-project` | Cobertura, áreas, bloques, plan y avisos |
| `test_cases_csv.py` | `.agents/skills/test-cases/scripts/` | `test-cases`, QA | `test-cases.md` → CSV de Azure Test Plans |

Además está el hook `sdd_guard.py` en `.agents/hooks/`, que se explica en el capítulo 12.

## new-sdd-item.py

Crea la carpeta de un work item para que prepares `story.md`.

```text
python <kit>/scripts/new-sdd-item.py <id> "<título>" [--tipo pbi|bug] [--por "<persona>"] [--target <raíz>]
```

| Opción | Por defecto | Qué hace |
| --- | --- | --- |
| `id` | — | ID del work item en Azure DevOps |
| `titulo` | — | El título tal cual, entre comillas; de él sale el nombre de la carpeta |
| `--tipo` | `pbi` | `bug` añade las secciones de reproducción e información del sistema |
| `--por` | `git config user.name` | Quién prepara `story.md` |
| `--target` | Carpeta actual | Raíz del proyecto |

:::out Salida real
Creado docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/
  story.md     ← cópialo desde Azure DevOps (instrucciones en el comentario del archivo)
  bitacora.md  ← notas de trabajo; ya tiene la primera entrada
  assets/      ← imágenes y archivos del work item, con nombre descriptivo

Siguiente:
  1. Rellena story.md y guarda las imágenes en assets/
  2. python <kit>/scripts/check-sdd-item.py docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral
  3. En una sesión nueva: /enrich-us 40399
:::

## check-sdd-item.py

Comprueba los artefactos de un work item según el paso alcanzado (sellos, anclas, secciones,
marcadores abiertos, coherencia de la WBS…), o solo un mensaje de commit.

Con ADR-0027 entiende lo que no se versiona:

- **Adjuntos que faltan.** Si `story.md` enlaza un adjunto que no está en tu equipo y git lo
  ignora, da un aviso: «bájalo del work item en Azure DevOps con ese nombre». Un enlace a un archivo
  que no existe y que git no ignora sigue siendo un error.
- **Paso 5.** Cuando la carpeta ya está en un commit con `Ref: #<id>`, comprueba ese mensaje (el
  `commit-message.md` ya no viaja con el repositorio). Antes del commit, comprueba `commit-message.md`.

```text
python .agents/scripts/check-sdd-item.py <carpeta>
python .agents/scripts/check-sdd-item.py --commit-message <archivo> --id <id>
```

:::out Carpeta recién creada, story.md sin rellenar (salida real)
Work item: 40399-seccion-de-ofertas-en-el-menu-lateral · paso alcanzado: 0 · story.md

  ✓ carpeta — docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral
  ✓ story.md — preparado por Ana Pérez
  ⚠ story.md — 14 campo(s) sin rellenar: <proyecto>, <N>, <estado>, <ruta>, <persona>, <texto literal> …
  ✗ story.md — la descripción está vacía o sin rellenar
  ✓ bitacora.md
  ⚠ pbi.md / bug.md — todavía no existe (paso 1)

  1 errores · 2 avisos
:::

:::out Un mensaje de commit con tres errores (salida real)
Mensaje de commit: msg.txt

  ✓ commit: primera línea tipo(ámbito): descripción
  ✗ commit: Ref — falta la línea «Ref: #<id>»
  ✗ commit: firma de IA — quita las líneas Co-Authored-By / Generated with: el sello SDD es la evidencia (ADR-0004)
  ✗ commit: cierre automático — no uses fix/fixes/fixed #id: Azure Repos cerraría el work item
  ✓ commit: tamaño — 105 caracteres

  3 errores · 0 avisos
:::

Qué comprueba del mensaje: primera línea `tipo(ámbito): descripción` (≤ 72 caracteres), la línea
`PBI-<id>`/`BUG-<id>` con el título, `Ref: #<id>` (opcional, con aviso, en `docs`, `chore`, `ci` y
`style`), sin `fix #id`, sin firmas de IA y como máximo 4000 caracteres.

:::tip Comprobar el commit que acabas de hacer (Windows)
```powershell
cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"
python .agents\scripts\check-sdd-item.py --commit-message $env:TEMP\msg.txt --id 40399
```
Usa `cmd /c`: el `>` de PowerShell 5.1 estropea las tildes.
:::

## pr-check.py

Las reglas obligatorias de una rama, **antes de abrir el PR** (ADR-0023). Es la red que no depende
de que la IA obedezca.

```text
python .agents/scripts/pr-check.py [--base origin/dev] [--root <raíz>]
```

| Comprobación | Error si… |
| --- | --- |
| Commits | Algún commit de la rama no sigue el formato (usa `check-sdd-item.py`) |
| Rutas protegidas | La rama cambia una ruta de `protected` de `sdd-guardrails.json` |
| Archivos de secretos | La rama añade un archivo que coincide con `secrets` |
| Borradores | La rama añade o cambia algo en `docs/sdd/_borradores/` (ADR-0027). Borrarlo está permitido |
| Archivos locales (aviso) | La rama añade a propósito un adjunto, `commit-message.md` o `test-cases.csv`, que no se versionan |
| Archivos del kit | La rama cambia archivos del kit sin un commit `chore(sdd)` |
| `AGENTS.md` | Pasa de 200 líneas |
| Secretos en el diff | El diff contiene patrones de claves, tokens o cadenas de conexión |
| Codificación | Un archivo cambiado no está en UTF-8 |

:::out Una rama con tres problemas (salida real)
pr-check · demo · feature/40399-seccion-ofertas..HEAD

  ✗ commit 1423eb02 — «arreglar cosas fix #123»: commit: primera línea (no sigue tipo(ámbito): descripción
    → «arreglar cosas fix #123»); commit: Ref (falta la línea «Ref: #<id>»); commit: cierre automático
    (no uses fix/fixes/fixed #id: Azure Repos cerraría el work item)
  · archivos — 2 cambiados o nuevos, 0 borrados
  ✗ rutas protegidas — Api/Legacy/Old.cs
  ✗ archivos de secretos — .env
  ✓ borradores — ninguno en la rama
  ✓ archivos del kit — sin cambios a mano
  ✓ AGENTS.md — 69 líneas (máximo 200)
  ✓ secretos en el diff — ninguno
  ✓ codificación UTF-8 — correcta

  3 errores · 0 avisos
:::

:::out Una rama con un borrador (salida real)
  ✗ borradores — docs/sdd/_borradores/tipos.md: crea el work item en Azure DevOps, anota su ID donde
    se citaba el borrador (bitacora.md, qa-report.md, plan.md) y borra el archivo antes del PR (ADR-0027)
:::

:::out Una rama correcta (salida real)
pr-check · demo · dev..HEAD

  ⚠ commit 66dd21f6 — «chore(sdd): configurar los guardarraíles»: commit: título del ticket; commit: Ref
  · archivos — 1 cambiados o nuevos, 0 borrados
  ✓ rutas protegidas — sin cambios
  ...
  0 errores · 1 avisos
:::

Los avisos no bloquean: un commit `chore(sdd)` sin work item no lleva `Ref:` y es lo esperado.

## check-encoding.py

```text
python .agents/scripts/check-encoding.py [--base origin/dev] [--fix]
```

Revisa que los archivos de texto cambiados frente a la base están en UTF-8. Con `--fix` convierte
los que no lo están (manteniendo el BOM si lo había). Típico en Windows con archivos guardados en
ANSI por otro editor.

:::out
1 archivo(s) de texto cambiados frente a dev

  ✓ Todos están en UTF-8
:::

## validate.py (solo el kit)

Valida el kit antes de cada commit al kit: estándar Agent Skills (nombre, descripción, tamaño del
`SKILL.md` ≤ 500 líneas), el bloque de convenciones idéntico en las 9 skills, anclas y sellos de
las plantillas, formato de los agentes, tamaño de `AGENTS.base.md`, versiones y que cada ADR esté
en el índice.

:::out
9 skills · 7 agents checked · 0 errors · 0 warnings
:::

## inventory.py

Inventario determinista para `project-context`: proyectos .NET y de pruebas, paquetes, lockfiles,
CI, contenedores y submódulos, traducciones, documentación existente, configuración de IA
existente y tabla de endpoints REST.

```text
python .agents/skills/project-context/scripts/inventory.py --out <temp>/inventario.md --endpoints <temp>/endpoints.md
```

:::out Extracto real
# Inventario de `demo`
Generado por inventory.py (fi-sdd-standard). Cada dato indica su archivo.
## CI
- Sin pipelines
## Traducciones
- Sin archivos de traducción detectados
## Configuración de IA existente
- `AGENTS.md`: 68 líneas, bloque del kit sí; secciones de contexto: ninguna
- `CLAUDE.md`: 1 líneas (solo importa `@AGENTS.md`)
- `.sdd-kit.json`: fi-sdd-standard v0.12.0
:::

## check_project.py

Comprueba el contexto del proyecto: bloque del kit, encabezados fijos de *Project context*, sello y
marca `sdd:context`, tamaño de `AGENTS.md` y de cada sección, `CLAUDE.md`, los seis `docs/`,
`[REQUIRES-VALIDATION]` abiertos, fuentes cambiadas desde la fecha del contexto,
`sdd-guardrails.json` frente a *Protected paths* y la existencia de pruebas de arquitectura.

```text
python .agents/skills/project-context/scripts/check_project.py [--root <raíz>]
```

Debe acabar en **0 errores** antes de `/document-project` y del primer work item. Los avisos se
resuelven con `/project-context check`.

## comment_only.py

Demuestra que la documentación solo cambió comentarios.

```text
python comment_only.py save    <copia> <archivo> [...]   # antes: guarda una copia (también de archivos sin seguimiento)
python comment_only.py check   <copia> <archivo> [...]   # después: compara
python comment_only.py restore <copia> <archivo> [...]   # descarta la documentación de un archivo, byte a byte
```

`check` exige que cada línea añadida, quitada o cambiada sea un comentario o esté en blanco, y que
no cambien el BOM ni los finales de línea. Código de salida 0 = solo comentarios, 1 = otra cosa
cambió, 2 = error de uso. No revisa `docs/`.

:::out Salida real: un cambio que no es comentario
✗ Api/Controllers/PingController.cs
    línea 2 (antes) cambió o se borró: public class PingController {}
    línea 3 (ahora) no es comentario: public class PingController { int x; }

1 archivo(s) con cambios que no son comentarios
:::

## doc_coverage.py

La herramienta de medición de `document-project`. Es una heurística por líneas (no el
compilador): sirve para planificar y medir antes y después.

| Modo | Qué hace |
| --- | --- |
| (sin opciones) | Cobertura del proyecto: símbolos documentados por carpeta |
| `--areas` | Propone áreas, partes y bloques (tablas y lista de archivos por área) |
| `--files <archivos>` | Símbolos sin comentario de esos archivos: línea, tipo, nombre |
| `--build-log <log>` | Cuenta los CS1591 (miembro público sin comentario) de un log de build |
| `--check-plan <plan.md>` | Comprueba el plan: cada archivo a documentar en exactamente un área, sin archivos desconocidos |
| `--warnings <log> --out avisos.md` | Avisos del build por código y archivo (sin duplicados; `NU19xx` aparte) |
| `--warnings <log> --compare avisos.md` | Compara con la línea base; sale con 1 si hay avisos nuevos |
| `--out`, `--json`, `--root` | Dónde escribir el informe, la versión JSON y la raíz |

:::out Extracto real de --areas
| ID | Área | Tipo | Archivos | Pruebas | Sin documentar | Cambios 6 m | Bloque | Nota |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A-01 | Ping | backend | 1 | 0 | 1/1 | 1 | B-01 |  |

| Bloque | Áreas | Archivos | Sin documentar |
| --- | --- | --- | --- |
| B-01 | A-01 | 1 | 1 |
:::

:::warn Builds comparables
Compara siempre builds hechos igual: `dotnet build <solución> --no-incremental`. Un build
incremental se salta proyectos y oculta sus avisos, y la comparación saldría engañosamente mejor.
:::

## test_cases_csv.py

```text
python .agents/skills/test-cases/scripts/test_cases_csv.py <test-cases.md> [--out <csv>] [--area "<Area\Path>"] [--include-blocked]
```

Convierte las secciones `### TC-NN` en el CSV que importa Azure Test Plans (columnas `ID`, `Work
Item Type`, `Title`, `Test Step`, `Step Action`, `Step Expected`, `Area Path`, `State`), en UTF-8
con BOM. Los casos `Bloqueado` quedan fuera salvo con `--include-blocked`. Ejemplo completo en el
capítulo 7.
