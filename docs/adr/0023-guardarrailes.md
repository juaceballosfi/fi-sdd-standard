# ADR-0023 · Guardarraíles: cada regla obligatoria con su comprobación

- **Estado:** Aceptada (pendiente de probar en Windows con Bonis y Calls4Grants)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0004, ADR-0012, ADR-0014, ADR-0021

## Contexto

Las reglas de `AGENTS.md` son instrucciones: la IA puede saltárselas. En los pilotos de Bonis pasó:
- un subagente leyó un secreto de `appsettings.Development.json`;
- la sesión principal imprimió parte de una clave al hacer grep;
- otra sesión parcheó un comentario que no le tocaba.

ADR-0012 ya decía que toda regla obligatoria se comprueba fuera de las instrucciones. Faltaban las
herramientas.

## Decisión

Cuatro capas, de la más temprana a la definitiva:

1. **Permisos `deny` de Claude Code.** `install.py` los añade a `.claude/settings.json` sin pisar los
   del proyecto:
   - no leer `.env*`, `appsettings.*.json`, `secrets.json`, `*.pfx`, `*.pem` ni `*.key`;
   - no ejecutar `git commit`, `git push`, `git reset --hard`, `git clean`, `git branch -D` ni
     borrados recursivos.

   El commit y el push los hace una persona.
2. **Hook `sdd_guard.py`** (Python, sin dependencias), instalado en `.agents/hooks/` y configurado en
   `sdd-guardrails.json`, que el proyecto versiona y completa `/project-context`:
   - *pre*: bloquea editar una ruta protegida y leer o editar un archivo de secretos, también con un
     comando de shell que lo nombre;
   - *post*: formatea el archivo con el comando del proyecto, avisa si ya no es UTF-8 y avisa de los
     patrones configurados.

   Un fallo interno del hook nunca bloquea la sesión.
3. **Pruebas de arquitectura.** Una plantilla xUnit sin paquetes extra comprueba tres reglas:
   - los controllers no inyectan el `DbContext`;
   - todo endpoint declara `[Authorize]` o `[AllowAnonymous]`;
   - la capa de datos no depende de los servicios.

   `/project-context` la crea en el proyecto de pruebas. La deuda que ya existe va a listas de
   excepciones con su motivo.
4. **`pr-check.py`** en `.agents/scripts/`. Se ejecuta antes del PR y, en la fase 4, en la validación
   del PR. Cubre así a Copilot y Codex, que no tienen hooks.

## Matriz regla → comprobación

| Regla (`AGENTS.md`) | Permiso | Hook | Prueba | `pr-check.py` | Otra |
| --- | --- | --- | --- | --- | --- |
| No leer ni imprimir secretos | ✓ lectura | ✓ lectura y shell | — | ✓ archivos y patrones en el diff | `code-explorer` |
| No editar rutas protegidas ni submódulos | — | ✓ | — | ✓ | — |
| La IA no hace commit, push ni cambia de rama | ✓ | — | — | — | — |
| Formato del commit, `Ref: #id`, nunca `fix #id`, sin firma de IA | — | — | — | ✓ | `check-sdd-item.py` |
| Archivos en UTF-8 conservando el BOM | — | ✓ aviso | — | ✓ | `check-encoding.py --fix` |
| Artefactos del work item (`docs/sdd/<id>-…`) | — | — | — | ✓ | `check-sdd-item.py` |
| Archivos del kit solo cambian con `install.py` | — | — | — | ✓ | `.sdd-kit.json` |
| `AGENTS.md` < 200 líneas | — | — | — | ✓ | `check_project.py` |
| Controllers sin `DbContext` | — | — | ✓ | — | — |
| Todo endpoint con autorización explícita | — | ✓ aviso (patrón) | ✓ | — | — |
| Capas: datos sin servicios | — | — | ✓ | — | — |
| Documentar solo cambia comentarios | — | — | — | — | `comment_only.py` |
| Patrones obligatorios del proyecto | — | ✓ aviso | si se puede | — | `qa-review` |
| Textos visibles traducidos a todos los idiomas | — | — | — | — | `qa-review` (fase 4: comprobación en el PR) |
| No inventar reglas de negocio | — | — | — | — | revisión humana y `qa-review` |

Las dos últimas filas no se pueden comprobar con un script: quedan en la revisión. Cada proyecto
añade sus reglas comprobables a `sdd-guardrails.json` y a sus pruebas.

## Consecuencias

- **Copilot no tiene hooks ni permisos equivalentes probados.** Para Copilot, `pr-check.py` es la
  defensa. En la ola 3 se mira qué ofrece VS Code (aprobación de comandos de terminal) y se
  documenta.
- **`python` debe estar en el PATH** para el hook. En Windows se ejecuta en modo exec (`command` más
  `args`), sin depender de Git Bash.
- **Los hooks PowerShell de Clavijo** que cubre el kit (rutas protegidas, formato, avisos) se
  sustituyen por la configuración de `sdd-guardrails.json` en `/project-context`.
