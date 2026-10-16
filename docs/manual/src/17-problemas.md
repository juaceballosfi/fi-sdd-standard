# Solución de problemas

:::lead
Los problemas más frecuentes de los pilotos, con su causa y su arreglo. Casi todos son del entorno
(Windows, codificación, git) y no del flujo.
:::

## Instalación y carga

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `/` no muestra las skills | La herramienta se abrió antes de instalar | Cierra y vuelve a abrir. En Claude Code, comprueba `.claude/skills/`; en VS Code, `.agents/skills/` |
| Faltan los subagentes en Claude Code | Solo se instaló `--tools copilot` | `install.py --tools copilot,claude` |
| `CONFLICTO … ya existe y no es del kit` | Un archivo del proyecto se llama como uno del kit | Decide cuál se queda; el instalador no lo toca |
| `UnicodeDecodeError` al instalar | Cachés de Python (`__pycache__`, `.pyc`) en una versión antigua del kit | Usa la v0.11.0 o posterior, o borra las carpetas `__pycache__` del kit |
| VS Code carga las reglas dos veces | Lee `AGENTS.md` y `.github/copilot-instructions.md` | En `.vscode/settings.json`: `"github.copilot.chat.codeGeneration.useInstructionFiles": false` |
| `REVISAR .gitignore ignora .claude/settings.json` | El proyecto ignora `.claude/` entero | Añade `!.claude/settings.json` al final de `.gitignore` |
| La IA responde en inglés | Sesión anterior a la regla de idioma, o `AGENTS.md` sin el bloque del kit | Reinstala; la regla está en el bloque del kit. Puedes pedir «responde en español» |

## Skills

| Síntoma | Causa | Solución |
| --- | --- | --- |
| La skill pide el ID aunque lo escribiste | Copilot no sustituye `$ARGUMENTS` y el ID iba en otro mensaje | Escribe `/skill <id>` en una sola línea |
| *Varias carpetas coinciden* | Hay dos carpetas con el mismo ID (por ejemplo, una antigua `docs/<sprint>/<item>`) | Responde cuál; las antiguas no se mueven |
| `technical-analysis` se para por pendientes | `pbi.md` tiene `[PENDING-BUSINESS]` | Resuélvelos (recomendado) o responde B |
| `wbs-execution` no avanza: *la base no está limpia* | Build o pruebas fallan al reanudar | A) arreglar primero · B) revisar a mano lo que quedó |
| *⛔ qa-review must run in a new session* | Lanzaste `qa-review` donde implementaste | Abre una sesión nueva |
| `document-project` se para: *uncommitted changes* | El árbol no está limpio | Commit o descarta lo anterior: un bloque empieza limpio |
| `comment_only.py`: *no es comentario* | `doc-writer` cambió algo más (un `using`, un espacio, el formato) | La skill lo devuelve a `doc-writer`; no lo parchees a mano. Para descartar: `comment_only.py restore` |
| La IA usa un *worktree* | Se le ocurrió para comparar builds | No hace falta: `doc_coverage.py --warnings --compare avisos.md`. Pídele que no use worktrees |

## Git

| Síntoma | Causa | Solución |
| --- | --- | --- |
| `nothing added to commit` | Faltó el `git add`, o los archivos nuevos (`??`) no se añadieron | `git add <rutas exactas>` y `git status --short` antes del commit |
| `git add` de la carpeta no añade `assets/` ni `commit-message.md` | Es intencionado: están en `.gitignore` (ADR-0027) | Nada. `git commit -F` lee `commit-message.md` del disco igualmente |
| `pr-check.py`: *borradores* | La rama tiene un archivo en `docs/sdd/_borradores/` | Crea el work item en Azure DevOps, anota su ID donde se citaba el borrador y bórralo |
| `check-sdd-item.py`: *… no está en este equipo* | Retomas un work item en otro equipo y los adjuntos no se versionan | Bájalos del work item en Azure DevOps a `assets/` con los nombres que enlaza `story.md` |
| `install.py`: *REVISAR … archivos versionados que ya no se versionan* | El proyecto subía esos archivos antes de la v0.12.0 | `git rm -r --cached` de esas rutas (capítulo 5) y un commit `chore(sdd)` |
| `?? .agents/scripts/__pycache__/` | `pr-check.py` de la v0.11.0 dejaba cachés de Python | Bórrala; desde la v0.12.0 no se crea y está en `.gitignore` |
| `Already up to date` al hacer merge de `dev` | No hiciste `git fetch` antes | `git fetch origin` y luego `git merge origin/dev` |
| Varios commits en la rama | Commits intermedios | Antes del push: `git reset --soft origin/dev` y un commit con `-F` |
| El work item se cerró solo al mezclar | Un `fix #id` en el mensaje | Reábrelo a mano; usa siempre `Ref: #id`. `pr-check.py` lo detecta antes |
| `warning: LF will be replaced by CRLF` | Finales de línea en Windows | Inofensivo. No cambies `core.autocrlf` por esto |
| `git branch -d` no borra la rama tras el PR | El squash cambia los commits | `git branch -D <rama>` (seguro con el PR completado) |
| `pr-check.py`: *archivos del kit cambiados a mano* | Editaste una skill instalada, o actualizaste el kit sin `chore(sdd)` | Revierte el cambio y hazlo en el kit, o haz la actualización con su commit `chore(sdd)` |

## Codificación y consola en Windows

| Síntoma | Causa | Solución |
| --- | --- | --- |
| Tildes rotas (`Ã©`, `├®`) al ver un archivo en PowerShell | PowerShell 5.1 lee UTF-8 sin BOM como ANSI | `Get-Content -Encoding UTF8 <archivo>`. El archivo está bien |
| `├®` en la salida de un script | Solo es la consola | Nada; o `chcp 65001` antes de ejecutar |
| Tildes rotas en un mensaje guardado con `>` | El `>` de PowerShell 5.1 escribe en UTF-16/ANSI | `cmd /c "git log -1 --format=%B > %TEMP%\msg.txt"` |
| Un archivo dejó de ser UTF-8 | Otro editor lo guardó en ANSI | `python .agents\scripts\check-encoding.py --fix` |

## Hooks y permisos (Claude Code)

| Síntoma | Causa | Solución |
| --- | --- | --- |
| El hook no bloquea nada | La herramienta no se reinició, `python` no está en el PATH o `.claude/settings.json` no se cargó | Reinicia; pruébalo a mano como en el capítulo 12 (*Probarlo a mano*) y comprueba que `$LASTEXITCODE` es 2 |
| Bloquea un archivo que necesitas leer | Coincide con `secrets` | Si de verdad no tiene secretos (una plantilla), añádelo a `secretsAllowed` con motivo en el PR |
| Aviso de patrón que no aplica | El patrón es demasiado amplio | Ajusta el `glob` o la expresión en `sdd-guardrails.json` |
| El formateador falla en cada edición | Comando de `format` no instalado | Quítalo de `format` o instala la herramienta (`dotnet tool restore`) |
| Te pide permiso para `git commit` y lo deniega | Es intencionado: está en `deny` | Haz el commit tú en la terminal |

## Builds y avisos

| Síntoma | Causa | Solución |
| --- | --- | --- |
| El número de avisos no cuadra (226 frente a 222) | MSBuild cuenta dos veces algunos `NU1902/NU1903`, o el build fue incremental | Compara con `doc_coverage.py --warnings … --compare`: quita duplicados y aparta los `NU19xx` |
| «0 avisos nuevos» sospechoso | Build incremental: se saltó proyectos | `dotnet build <solución> --no-incremental` |
| Avisos `NU19xx` cambian sin tocar nada | Dependen de la base de avisos de seguridad de NuGet, no del código | Se listan aparte y no cuentan como nuevos |
| CS1570–CS1587 tras documentar | Un comentario XML mal formado | La skill lo devuelve a `doc-writer` |

:::note Cuando nada de esto encaja
Guarda la salida en un archivo, anota la versión del kit (`.sdd-kit.json`), la herramienta y el
modelo, y avisa al responsable del kit. Si la skill se equivocó, el arreglo va al kit para todos,
nunca a la copia instalada.
:::
