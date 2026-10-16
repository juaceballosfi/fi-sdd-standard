# Guía · Llevar el piloto a `dev`

El kit, el contexto del proyecto y la documentación viven en la rama local `chore/sdd-kit-piloto`.
Para que el equipo los use, entran en `dev` con un PR, como cualquier cambio.

## 1 · Qué entra

| Entra | No entra |
| --- | --- |
| `.agents/` (skills, hooks, scripts), `.github/agents/`, `.github/prompts/` | `.claude/skills/`, `.claude/agents/` (copias locales: `install.py` las genera) |
| `.claude/settings.json` (permisos y hooks del equipo) | `.claude/settings.local.json` (personal) |
| `AGENTS.md`, `CLAUDE.md`, `.gitmessage`, `.sdd-kit.json`, `sdd-guardrails.json` | — |
| `docs/` (contexto, ADR, `docs/sdd/`) y los comentarios de los bloques de `/document-project` | De `docs/sdd/`: `assets/`, `commit-message.md`, `test-cases.csv` y `_borradores/` (ADR-0027) |
| — | `.github/copilot-instructions.md` (copia de `AGENTS.md` para Visual Studio, generada por `install.py`) |

## 2 · Preparar la rama del PR

```powershell
git fetch origin
git switch chore/sdd-kit-piloto
git merge origin/dev                         # resuelve conflictos si los hay; el piloto debe estar al día
python .agents\skills\project-context\scripts\check_project.py   # 0 errores
dotnet build <solución> --no-incremental; dotnet test <pruebas>  # como en la línea base
git switch -c chore/sdd-kit-en-dev
git push -u origin chore/sdd-kit-en-dev
python .agents\scripts\pr-check.py --base origin/dev
```

Si el historial del piloto tiene commits de prueba que no deben llegar a `dev`, el PR se completa
con **squash**: un solo commit en `dev`. Como no corresponde a un work item, el mensaje no lleva
`Ref:`, y el aviso de `pr-check.py` sobre `Ref:` es esperado:

```text
chore(sdd): adoptar fi-sdd-standard v<versión> en <proyecto>
```

Si existe un work item de adopción, se enlaza y el mensaje lleva `Ref: #<id>`.

## 3 · El PR

- **Revisor:** el tech lead del proyecto.
- **Descripción:** qué cambia para el equipo (cómo se trabaja un work item, la guía rápida), qué no
  cambia (el código, salvo los comentarios de los bloques documentados) y cómo se instala en cada
  equipo (`install.py --tools copilot,claude`).
- Revisa a mano `sdd-guardrails.json`: las rutas protegidas son las del proyecto, y no hay secretos
  permitidos sin motivo.

## 4 · Después del merge

Cada desarrollador, en su copia, una vez:

```powershell
git switch dev; git pull
python <kit>\scripts\install.py --target . --tools copilot,claude   # genera las copias locales de .claude/
git config commit.template .gitmessage
```

La rama `chore/sdd-kit-piloto` se borra cuando `dev` tiene todo. Desde ese momento, el kit se
actualiza con un PR `chore(sdd): actualizar fi-sdd-standard a v<versión>`.
