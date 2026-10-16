# Guía rápida · Desarrollo con fi-sdd-standard

Una página para trabajar un work item. El detalle está en cada skill y en la guía git.

## Una vez por repositorio (tech lead)

```powershell
python <kit>\scripts\install.py --target . --tools copilot,claude
git config commit.template .gitmessage
```

Después, en una sesión nueva: `/project-context`. Opcional: `/document-project`, por bloques.

## Cada work item

| Paso | Qué haces tú | Comando | Sale |
| --- | --- | --- | --- |
| 0 | Rama `feature/<id>-<título>` desde `dev`; copias el work item de Azure DevOps | `python <kit>\scripts\new-sdd-item.py <id> "<título>"` | `docs/sdd/<id>-<título>/story.md` y `assets/` (local) |
| 1 | Respondes las preguntas (o las pasas al PO) | `/enrich-us <id>` | `pbi.md` o `bug.md` |
| 2 | Apruebas la propuesta (03) y el plan (04) | `/technical-analysis <id>` | `00`–`06` |
| 3 | Confirmas el inicio; resuelves bloqueos | `/wbs-execution <id>` | Código, pruebas, `CHANGELOG.md`, `commit-message.md` |
| 4 | **Sesión nueva.** Decides cada hallazgo | `/qa-review <id>` · correcciones: `/wbs-execution <id> qa` | `qa-report.md` |
| 5 | Revisas | `/document-code <id>` | Comentarios y `docs/` |
| 6 | Commit, comprobación y PR a `dev` | `git add <rutas exactas>` · `git commit -F docs/sdd/<carpeta>/commit-message.md` · `python .agents\scripts\pr-check.py` | PR enlazado al work item |

**Bug pequeño:** `/quick-fix <id>` sustituye a los pasos 1–3 si pasa la compuerta: la causa se ve en
el código, como máximo 3 archivos de una capa, sin migración, sin cambios de contrato ni de permisos.
Si no la pasa, te lo dice y sigues por el paso 1. Los pasos 4–6 no cambian.

## Lo que la IA no hace (y lo que la frena)

- No hace commit, push ni cambia de rama: lo haces tú. Los permisos de `.claude/settings.json` lo
  bloquean.
- No lee secretos (`.env*`, `appsettings.*.json`, certificados). Si necesita un valor, te lo pide.
- No edita rutas protegidas (`sdd-guardrails.json`). El hook la para.
- No inventa reglas, criterios ni traducciones: los marca `[PENDING-BUSINESS]` o
  `[PENDING-TRANSLATION]`.

## Antes del PR

- Los borradores de `docs/sdd/_borradores/` no van en el PR: crea cada work item en Azure DevOps,
  anota su ID donde se citaba y borra el borrador.
- No se versionan (ADR-0027): `assets/` (los adjuntos están en Azure DevOps), `commit-message.md`
  (queda en el commit) ni `test-cases.csv` (se regenera). Ya están en `.gitignore`.

```powershell
python .agents\scripts\pr-check.py            # reglas obligatorias de la rama, contra origin/dev
python .agents\scripts\check-sdd-item.py docs\sdd\<carpeta>
```

Los dos en 0 errores. Mensaje de commit: nunca `fix #id`, siempre `Ref: #id`, sin `Co-Authored-By`.
Más detalle en `docs/guias/git-por-work-item.md` del kit.
