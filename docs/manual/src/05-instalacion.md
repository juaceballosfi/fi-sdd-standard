# Instalación

:::lead
El kit se instala en cada repositorio con un script. En un proyecto existente, después viene
`/project-context`, que escribe el contexto real del proyecto; en uno nuevo, lo mismo cuando haya
algo de código. Este capítulo cubre los dos casos y cómo actualizar el kit más adelante.
:::

## Requisitos

| Requisito | Para qué | Cómo comprobarlo |
| --- | --- | --- |
| Python 3.10 o superior | Instalador, scripts, hook | `python --version` |
| Git | Todo el flujo | `git --version` |
| El kit descargado | La fuente de la instalación | Zip `fi-sdd-standard-v<versión>.zip` descomprimido, o un clon del repositorio del kit |
| Claude Code y/o GitHub Copilot (agente) | Ejecutar las skills | `/` en el chat muestra las skills tras instalar |
| El SDK y las herramientas del proyecto (.NET, Node…) | Que la IA pueda compilar y probar | Lo que diga el README del proyecto |

:::tip Dónde dejar el kit
Ponlo al lado de tus repositorios, por ejemplo `C:\Users\<tú>\Documents\fi-sdd-standard`, y
comprueba la versión antes de instalar:

```powershell
cd C:\Users\<tú>\Documents\fi-sdd-standard
git log --oneline -1          # v0.13.0
python scripts\validate.py    # 9 skills · 7 agents checked · 0 errors · 0 warnings
```
:::

## El instalador: install.py

```powershell
python <kit>\scripts\install.py --target <ruta-del-proyecto> --tools copilot,claude [--dry-run]
```

| Opción | Valores | Qué hace |
| --- | --- | --- |
| `--target` | Ruta del repositorio | Dónde se instala (obligatorio) |
| `--tools` | `copilot`, `claude`, `visualstudio`, separados por comas | `copilot` instala `.agents/skills/` y `.github/agents/` (versionados); `claude` genera las copias locales de `.claude/`, los permisos y los hooks; `visualstudio` genera `.github/copilot-instructions.md` desde `AGENTS.md`. Por defecto: `copilot` |
| `--dry-run` | — | Muestra lo que haría sin escribir nada. Úsalo siempre la primera vez |

**Nunca sobrescribe archivos del proyecto.** Solo crea lo que falta y actualiza lo que instaló el
propio kit (lista en `.sdd-kit.json`). Cada línea de su salida dice qué pasó:

| Estado | Significado | Qué haces |
| --- | --- | --- |
| `creado` | El archivo no existía y lo ha creado | Nada |
| `actualizado` | Era del kit y ha cambiado con la nueva versión | Revisa el diff antes del commit |
| `igual` | Ya estaba en esta versión | Nada |
| `existe` | Es un archivo de configuración del proyecto que ya existía: no se toca | Nada |
| `PENDIENTE` | Falta un paso tuyo | Lee el mensaje: casi siempre es `/project-context` |
| `REVISAR` | Hay algo que conviene mirar a mano | Lee el mensaje (por ejemplo, un `.gitignore` que ignora `.claude/settings.json`) |
| `CONFLICTO` | Hay un archivo con ese nombre que **no es del kit**: no se toca | Decide si el del proyecto se queda o se sustituye a mano |

## Proyecto existente, paso a paso

Ejemplo: un repositorio .NET + React que nunca ha usado el kit.

**1. Rama de trabajo.** La instalación es un cambio como cualquier otro:

```powershell
cd C:\repos\mi-proyecto
git switch dev; git pull
git switch -c chore/sdd-kit
```

**2. Simulación y luego instalación:**

```powershell
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude --dry-run
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
```

:::out Salida real del instalador (resumida)
fi-sdd-standard v0.13.0 · Instalación en C:\repos\mi-proyecto

  creado       .agents/skills/document-code/SKILL.md
  ...                                              (las 9 skills con plantillas y scripts)
  creado       .github/prompts/wbs-execution-sonnet.prompt.md
  creado       .claude/skills/...                  (copia local para Claude Code)
  actualizado  .gitignore (+9 líneas)
  creado       .github/agents/backend-dev.agent.md
  creado       .claude/agents/backend-dev.md
  ...                                              (los 7 subagentes, en los dos formatos)
  actualizado  .gitignore (+7 líneas)
  creado       .agents/hooks/sdd_guard.py
  creado       .agents/scripts/pr-check.py
  creado       .agents/scripts/check-sdd-item.py
  creado       .agents/scripts/check-encoding.py
  creado       sdd-guardrails.json
  PENDIENTE    sdd-guardrails.json: /project-context añade las rutas protegidas y los patrones
  creado       .claude/settings.json (+20 reglas deny, hooks del kit)
  creado       .gitmessage
  creado       AGENTS.md
  PENDIENTE    AGENTS.md: ejecuta /project-context para escribir «Project context»
  creado       CLAUDE.md
  creado       docs/adr/0000-plantilla.md
  creado       docs/sdd/
  actualizado  .gitignore (+5 líneas)                (lo que no se versiona, ADR-0027)
  creado       .sdd-kit.json

  PENDIENTE: 2 · actualizado: 2 · creado: 105

  Siguiente: revisa los PENDIENTE / REVISAR de arriba  ·  git config commit.template .gitmessage
             ·  haz commit de la instalación antes de seguir: git add .agents … · git commit -m "chore(sdd): …"
             ·  /project-context en una sesión nueva (contexto del proyecto, documentación base y pruebas)
:::

Si el proyecto ya tenía un `AGENTS.md` o un `CLAUDE.md` propios, el instalador no los pisa:

- `AGENTS.md` sin las marcas del kit → `PENDIENTE AGENTS.md sin marcas del kit`. `/project-context`
  usa su contenido como fuente y reconstruye el archivo con las marcas.
- `CLAUDE.md` con contenido propio → `PENDIENTE CLAUDE.md no importa @AGENTS.md`. `/project-context`
  propone pasar ese conocimiento a `AGENTS.md` o a `docs/` y dejar `CLAUDE.md` en `@AGENTS.md`.
- Un `.gitignore` que ignora `.claude/` entero → `REVISAR`: añade `!.claude/settings.json` al
  final, porque los permisos y hooks del equipo se versionan.

**3. Plantilla de commit** (una vez por equipo y repositorio):

```powershell
git config commit.template .gitmessage
```

**4. Primer commit, con rutas exactas:**

```powershell
git status --short
git add .agents .github/agents .github/prompts .claude/settings.json AGENTS.md CLAUDE.md `
        .gitignore .gitmessage .sdd-kit.json sdd-guardrails.json docs/adr docs/sdd
git status --short          # no debe quedar nada del kit fuera, salvo .claude/skills y .claude/agents
git commit -m "chore(sdd): instalar fi-sdd-standard v0.13.0"
```

Este commit va **antes** de `/project-context`, que se para si no está hecho. Si la sesión del
contexto sale mal, se descarta sin perder la instalación.

:::note Lo que no entra en el commit
El instalador añade al `.gitignore` lo que no se versiona (ADR-0027): de cada work item, `assets/`,
`commit-message.md` y `test-cases.csv`; y `.claude/settings.local.json` y
`.github/copilot-instructions.md`. Además, `.claude/skills/` y `.claude/agents/` son copias locales:
y cada persona las genera en su equipo con `install.py`.
:::

**5. Contexto del proyecto.** Cierra y vuelve a abrir la herramienta (para que cargue las skills, los
agentes y los hooks) y, en una **sesión nueva**:

:::ask
/project-context
:::

La skill comprueba primero el entorno (SDK, Node, `dotnet restore`, enlaces y submódulos) y se para
con los pasos exactos si algo impide compilar. Después inventaría el repositorio, ejecuta build,
pruebas, lint y type check para verificar los comandos y registrar la línea base, te hace las preguntas que el código no responde y te enseña un
borrador. Al aprobarlo escribe *Project context*, los seis `docs/*.md` base, el proyecto de
pruebas si no había, las pruebas de arquitectura y `sdd-guardrails.json`. Lo que encuentre que haya
que arreglar en el proyecto lo deja como borrador con prioridad, sin arreglarlo. Detalle en el
capítulo 8.

Al terminar, comprueba:

```powershell
python .agents\skills\project-context\scripts\check_project.py     # 0 errores
```

y haz el commit que te propone: `chore(sdd): añadir el contexto del proyecto y la documentación base`.

**6. (Opcional) Documentación completa.** `/document-project` crea un plan por áreas y documenta
el proyecto por bloques, un PR por bloque. Detalle en el capítulo 8.

**7. Llevarlo a `dev`.** PR de `chore/sdd-kit` a `dev` con el tech lead como revisor (capítulo 14).
Después del merge, cada desarrollador, en su copia:

```powershell
git switch dev; git pull
python <kit>\scripts\install.py --target . --tools copilot,claude   # genera sus copias de .claude/
git config commit.template .gitmessage
```

## Proyecto nuevo

En un repositorio vacío o recién creado la instalación es la misma; lo único que cambia es el
contexto, que todavía no tiene de dónde salir.

```powershell
mkdir C:\repos\nuevo; cd C:\repos\nuevo
git init -b dev
python <kit>\scripts\install.py --target . --tools copilot,claude
git config commit.template .gitmessage
git add .agents .github .claude/settings.json AGENTS.md CLAUDE.md .gitignore .gitmessage .sdd-kit.json sdd-guardrails.json docs
git commit -m "chore(sdd): instalar fi-sdd-standard v0.13.0"
```

Este commit va **antes** de `/project-context`, que se para si no está hecho. Si la sesión del
contexto sale mal, se descarta sin perder la instalación.

`check_project.py` dará errores de `docs/` y del contexto: es lo esperado mientras no haya código.

:::out check_project.py en un repositorio recién instalado
Contexto del proyecto: nuevo

  ✓ AGENTS.md — bloque del kit
  ✗ Project context — faltan los encabezados fijos: What this is, Commands, Local run, ...
  ⚠ Project context — sin el sello «Generado con: project-context» (¿escrito a mano?)
  ✓ AGENTS.md — 69 líneas
  ⚠ Project context — sin la marca sdd:context (fecha y fuentes): no se pueden detectar cambios
  ✓ CLAUDE.md — importa @AGENTS.md
  ✗ docs/architecture.md — no existe
  ...
  7 errores · 2 avisos
:::

Orden recomendado en un proyecto nuevo:

1. Crea el esqueleto de la solución (proyectos, capas, proyecto de pruebas) como de costumbre, o
   con un primer work item cuyo `story.md` describa la estructura deseada.
2. En cuanto haya algo que compilar, `/project-context` en `new`: registra los comandos, crea lo que
   falte del proyecto de pruebas y las pruebas de arquitectura **desde el primer día**, y deja
   `docs/` con sus encabezados fijos.
3. Rellena `sdd-guardrails.json` (rutas protegidas, formateadores, patrones) con la propuesta de
   `/project-context`.
4. Cada work item siguiente sigue el flujo normal. `document-code` mantiene `docs/` al día work
   item a work item, así que `/document-project` no hace falta.

## Actualizar el kit

Cuando sale una versión nueva:

```powershell
cd <kit>; git pull        # o descomprime el zip nuevo en lugar del anterior
python scripts\validate.py
cd <proyecto>
git switch -c chore/sdd-kit-v0.13.0 origin/dev
python <kit>\scripts\install.py --target . --tools copilot,claude
git status --short
git diff --stat
```

- Los archivos del kit salen como `actualizado`; los tuyos, nunca.
- El bloque del kit de `AGENTS.md` se reemplaza; *Project context* no se toca.
- `.claude/settings.json` se fusiona: se sustituyen los hooks del kit y se añaden las reglas `deny`
  que falten, sin borrar las tuyas.
- Lee el `CHANGELOG.md` del kit: algunas versiones piden un paso (por ejemplo,
  `/project-context check` para rellenar una clave nueva de `sdd-guardrails.json`).

Commit con un mensaje fijo y rutas exactas:

```powershell
git add .agents .github/agents .github/prompts .claude/settings.json AGENTS.md .gitignore .sdd-kit.json sdd-guardrails.json
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.13.0"
```

:::warn Por qué el prefijo chore(sdd)
`pr-check.py` da error si una rama cambia archivos del kit sin un commit `chore(sdd)`: así nadie
modifica una skill instalada a mano por accidente.
:::

## Qué se versiona y qué no

El criterio (ADR-0027): se versiona lo que un paso posterior o una persona necesita desde otra
máquina, o lo que es una decisión o una evidencia que no se puede reproducir. No se versiona lo que
duplica algo ya guardado (git, el PR, Azure DevOps), lo que un script regenera igual ni lo personal.

| Se versiona | No se versiona (`.gitignore`) |
| --- | --- |
| `.agents/` (skills, hook, scripts): Copilot lo lee de ahí y todo el equipo usa la misma versión | `.claude/skills/`, `.claude/agents/`: copias que genera `install.py` |
| `.github/agents/`, `.github/prompts/` | `.github/copilot-instructions.md`: copia de `AGENTS.md` para Visual Studio, la genera `install.py --tools visualstudio` |
| `.claude/settings.json` (permisos y hooks del equipo) | `.claude/settings.local.json` (personal) |
| `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`, `sdd-guardrails.json` | — |
| `docs/`: contexto, ADR y `docs/sdd/` | De cada work item: `assets/`, `commit-message.md`, `test-cases.csv` |
| `docs/sdd/_documentacion/` mientras dure el plan | `docs/sdd/_borradores/`: no llega a `dev` (`pr-check.py` lo bloquea) |

:::tip Un adjunto que es la especificación
Si un mockup aprobado es la única especificación posible y quieres que viaje con el código,
añádelo a propósito: `git add -f docs/sdd/<carpeta>/assets/<archivo>`. `pr-check.py` lo deja
pasar con un aviso.
:::

### Si el proyecto ya versionaba esos archivos

En un proyecto que usaba el kit antes de la v0.12.0, `install.py` avisa con `REVISAR` de los que
ya estaban en git (por ejemplo, `commit-message.md` de work items antiguos). No borra nada. Para
dejar de versionarlos sin borrarlos de tu disco:

```powershell
git rm -r --cached --ignore-unmatch "docs/sdd/*/commit-message.md" "docs/sdd/*/test-cases.csv" "docs/sdd/*/assets/*"
git commit -m "chore(sdd): dejar de versionar los archivos locales del flujo (ADR-0027)"
```

Lo que ya estaba en el historial sigue ahí; a partir de este commit no se vuelve a subir.

### El manual

El manual (PDF y Markdown) vive en `docs/manual/` del repositorio del kit, con sus fuentes. No se
instala en los proyectos: se consulta en el kit, y el Markdown se puede dar de contexto a una IA.
