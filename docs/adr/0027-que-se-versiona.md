# ADR-0027 · Qué se versiona en un proyecto con el kit

- **Estado:** Aceptada
- **Fecha:** 2026-10-16
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0002 (sustituida en parte), ADR-0015, ADR-0017, ADR-0023

## Contexto

ADR-0002 decidió versionar entera la carpeta de cada work item. Tras los pilotos se ve que parte de
lo que entra en el repositorio no aporta después del merge o ya está guardado en otro sitio:

- `commit-message.md` es idéntico al mensaje del commit y a la descripción del PR.
- `test-cases.csv` lo regenera `test_cases_csv.py` desde `test-cases.md`, byte a byte.
- `assets/` copia los adjuntos del work item, que ya están en Azure DevOps. Son binarios (cientos
  de KB por work item, cientos de MB al año) y las capturas pueden llevar datos que no deben
  quedar en el historial de git.
- Los borradores de `docs/sdd/_borradores/` son temporales: si llegan a `dev`, o nadie crea el
  work item, o queda una copia desactualizada del que se creó.
- `.github/copilot-instructions.md` es una copia de `AGENTS.md` solo para Visual Studio: versionada,
  se desincroniza.

Lo que genera la IA no se puede regenerar igual: volver a lanzar una skill da otro resultado y
cuesta contexto. Por eso no basta con «se puede generar» para dejar algo fuera.

## Decisión

Se versiona lo que **un paso posterior o una persona necesita desde otra máquina** o lo que **es una
decisión o una evidencia que no se puede reproducir**. No se versiona lo que duplica algo ya
guardado (git, el PR, Azure DevOps), lo que un script regenera idéntico ni lo personal.

**Carpeta del work item (`docs/sdd/<id>-<título>/`):**

| Se versiona | No se versiona (`.gitignore`) |
| --- | --- |
| `story.md`, `bitacora.md` | `assets/`: los adjuntos se bajan de Azure DevOps |
| `pbi.md` / `bug.md` | `commit-message.md`: queda en el commit y en el PR |
| `00`–`06` o `fix-plan.md` | `test-cases.csv`: se regenera con `test_cases_csv.py` |
| `CHANGELOG.md`, `qa-report.md`, `test-cases.md` | |

Un adjunto que **es** la especificación (un mockup aprobado sin otra descripción posible) puede
versionarse a propósito con `git add -f`.

**Carpetas compartidas:**
- `docs/sdd/_borradores/` no llega a `dev`: antes del PR se crea el work item en Azure DevOps, se
  anota su ID donde se citaba el borrador (`bitacora.md`, `qa-report.md`, `plan.md`) y se borra el
  archivo. `pr-check.py` da error si la rama añade o cambia un borrador.
- `docs/sdd/_documentacion/` se versiona mientras dure el plan de `/document-project`.

**Archivos del kit en el proyecto:** se versionan `.agents/`, `.github/agents/`, `.github/prompts/`,
`.claude/settings.json`, `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`,
`sdd-guardrails.json` y `docs/`. No se versionan `.claude/skills/`, `.claude/agents/`,
`.claude/settings.local.json` ni `.github/copilot-instructions.md`, que genera `install.py` en cada
equipo.

**El manual del kit** (`docs/manual/`: fuentes, PDF y Markdown) vive solo en el repositorio del kit
y no se instala en los proyectos.

## Consecuencias

- `install.py` añade al `.gitignore` del proyecto: `docs/sdd/*/assets/`,
  `docs/sdd/*/commit-message.md`, `docs/sdd/*/test-cases.csv`, `.claude/settings.local.json` y
  `.github/copilot-instructions.md`. Un `copilot-instructions.md` ya versionado no se borra: se
  avisa para quitarlo del índice con `git rm --cached`.
- `check-sdd-item.py`: un enlace de `story.md` a un adjunto que falta es aviso, no error, si la ruta
  está ignorada por git (un clon limpio o el pipeline no tienen los adjuntos). El paso «listo para
  commit» se reconoce también por el último commit que toca la carpeta con `Ref: #<id>`.
- `pr-check.py`: error si la rama añade o modifica algo en `docs/sdd/_borradores/`; borrarlo está
  permitido.
- Las skills dejan de citar `commit-message.md` en los archivos del commit; `test-cases` dice que el
  CSV es local; `enrich-us` dice que en otra máquina los adjuntos se bajan del work item.
- Quien retome un work item en otra máquina descarga los adjuntos de Azure DevOps a `assets/` con
  los mismos nombres que enlaza `story.md`.
- Hay un paso más antes del PR cuando la rama tiene borradores.

## Alternativas consideradas

- Mantener ADR-0002 sin cambios: el repositorio crece con binarios y duplicados.
- Versionar solo `pbi.md`, `CHANGELOG.md`, `bitacora.md` y `qa-report.md`: `wbs-execution`,
  `qa-review` y `document-code` necesitan `00`–`06` en sesiones posteriores, también desde otra
  máquina.
- Ignorar `_borradores/` en `.gitignore`: el borrador solo existiría en la máquina de quien lo
  generó y nadie más lo vería en la rama.
- Un aviso (no un error) para los borradores: se ignora fácilmente y acabarían en `dev` igual.
