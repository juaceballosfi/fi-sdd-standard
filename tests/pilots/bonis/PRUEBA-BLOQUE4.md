# Prueba del bloque 4 de la fase 2 · `document-code` y `doc-writer` · kit v0.8.0

**Objetivo:** comprobar que `document-code`:
- decide bien qué documentar y con qué fuente;
- hace que `doc-writer` escriba solo comentarios y secciones de `docs/`;
- demuestra con el script que no cambió nada más;
- deja la documentación registrada en la carpeta del work item.

**Work item:** 40933, ya en `dev` (PR 14468 y 14472). Se documenta desde `base` = `9e07c66d`, el
commit anterior al 40933, hasta el árbol de trabajo. En `chore/sdd-kit-piloto` el código de Bonis es
igual al de `dev`. El resultado será un commit de seguimiento `docs(…)`.

**Dónde:** rama `chore/sdd-kit-piloto` de Bonis, en PowerShell, desde la raíz (`bonis_v2`).

## 1 · Instalar

```powershell
cd ..\fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git status --short
```

Lo que debe mostrar el instalador:

| Acción | Archivos |
| --- | --- |
| `creado` | `.agents/skills/document-code/` (`SKILL.md` y `scripts/comment_only.py`) y su copia en `.claude/skills/` |
| `creado` | `.github/agents/doc-writer.agent.md` y `.claude/agents/doc-writer.md` |
| `actualizado` | Los otros cuatro skills (v3.7), `backend-dev`, `frontend-dev`, `AGENTS.md` (solo el bloque del kit) y `.sdd-kit.json` |
| `.gitignore` | `+1 líneas` (skill) y `+1 líneas` (agente) |

**`AGENTS.md` de Bonis:** sustitúyelo por la versión completa del kit, que ya trae las notas nuevas
(*Runtime checks* en *Debug vs Release*; pruebas del frontend y comprobación de tipos en *Tests*):

```powershell
Copy-Item ..\fi-sdd-standard\tests\pilots\bonis\AGENTS.md .\AGENTS.md
git diff --stat AGENTS.md
```

`runtime-tester`, `frontend-dev` y `qa-review` las leen de ahí.

```powershell
git add .agents .github/agents AGENTS.md .gitignore .sdd-kit.json
git status --short
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.8.0"
```

Cierra Claude Code y ábrelo de nuevo. «¿Qué subagentes tienes disponibles?» debe mostrar 6:
`code-explorer`, `backend-dev`, `frontend-dev`, `qa-reviewer`, `runtime-tester` y `doc-writer`.

## 2 · Ejecutar

En una sesión nueva:

```text
/document-code 40933 base:9e07c66d
```

| Momento | Qué comprobar |
| --- | --- |
| Paso 0 | Toma los archivos del item del `CHANGELOG.md` y deja fuera los del kit. Son 6: el servicio, `identification.tsx`, `add.tsx` y tres clases de prueba, una de ellas la de `Enqueue`. Ve que `qa-report.md` no tiene nada alto ni medio sin decidir |
| Inventario | Lo delega en `code-explorer` (6 archivos) y trae una muestra de estilo del proyecto |
| Confirmación | Cada símbolo con su fuente (`BR-XX`, `SPEC-XX`, 03 §…) |
| Lo esperable | `IsDelegate` y el parámetro `isDelegate` de los jobs (por qué se calcula en la petición y no en el job); `ConfigureAllHeaders`, `PopulateAllTrackingRow` y `StyleHeaderRow`; el campo oculto `managers` de `add.tsx` (por qué existe); el resumen de las dos clases de prueba nuevas con sus SPEC; las reglas de delegado en `docs/reglas-negocio.md`. Ninguna ADR |
| Lo que no debería salir | Comentarios en código que el 40933 no tocó, comentarios que repiten el nombre, y cambios en la API (no la hay) |
| Snapshot | Ejecuta `comment_only.py save` **antes** de llamar a `doc-writer` |
| Verificación | `comment_only.py check` → «Solo cambiaron comentarios»; build sin avisos nuevos (CS1570–CS1587); lint |
| Registro | Una entrada «Documentación» en el `CHANGELOG.md` del item, una línea en la bitácora y `commit-message.md` reescrito entero como `docs(…)`, porque el item ya está en `dev` |

Si quieres comprobarlo tú también:

```powershell
git diff -U0 -- Bonis Bonis.Tests | Select-String '^[+-][^+-]'
```

Todas las líneas que salgan deben ser comentarios (`///`, `//`, `/** … */`, `*`).

```powershell
python ..\fi-sdd-standard\scripts\check-sdd-item.py docs\sdd\40933-correcciones-rol-delegado
git status --short
```

En la salida del comprobador debe salir `✓ documentación`.

## 3 · Subir

Los archivos `docs/*.md` del proyecto (`reglas-negocio.md` y los demás) los creó el instalador en
la rama del piloto. Puede que **no existan en `dev`**. Compruébalo:

```powershell
git ls-tree --name-only origin/dev docs/
```

- **Si están en `dev`:** un solo commit, como en la guía (variante B), en una rama
  `feature/40933-documentacion`.
- **Si no están:** dos commits en el piloto.
  1. Los comentarios del código y la carpeta del item, con
     `git commit -F docs/sdd/40933-correcciones-rol-delegado/commit-message.md`. Este es el que va
     por *cherry-pick* a `feature/40933-documentacion` y al PR.
  2. Los `docs/*.md`, con `git commit -m "docs(sdd): documentar las reglas del 40933 en docs/" -m "Ref: #40933"`.
     Se queda en el piloto y llega a `dev` con el PR del kit.

  Si el *cherry-pick* del primero da conflicto en `docs/`, cancélalo con `git cherry-pick --abort`:
  ese commit llevaba un `docs/*.md` por error.

## 4 · Resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación y 6 agentes visibles | | |
| 2 | Archivos del item tomados del CHANGELOG, sin los del kit | | |
| 3 | Inventario con fuente para cada símbolo; nada inventado | | |
| 4 | Confirmación antes de escribir | | |
| 5 | Snapshot antes y `check` después: solo comentarios | | |
| 6 | Build sin avisos nuevos y lint | | |
| 7 | Calidad: español, el porqué y no el qué, `#40933` y `BR-XX`, estilo del proyecto | | |
| 8 | `docs/`: hechos con fuente; si la plantilla está vacía, solo la sección del item | | |
| 9 | CHANGELOG, bitácora (una línea) y mensaje entero | | |
| 10 | Comprobador con `✓ documentación` | | |
| 11 | Contexto (`/context` al final) y tiempo | | |
| 12 | ¿Aprobarías estos comentarios en una revisión de PR? | | |

## 5 · Qué enviar

- El registro de la sesión, con `/context` al final.
- `git diff` de los archivos de código, o un zip con ellos.
- La carpeta del 40933 en un zip y los `docs/*.md` que cambiaron.
- La tabla de resultados.
