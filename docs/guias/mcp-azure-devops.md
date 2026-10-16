# Guía · Prueba del MCP de Azure DevOps (solo lectura)

**Decide:** si el MCP sustituye al texto pegado como entrada de `story.md` (brief, «Prueba del MCP»).
Hasta que la prueba lo apruebe, `story.md` se prepara con el texto pegado.

## Antes de empezar

- [ ] TI confirma que la organización de Azure DevOps está vinculada a Entra ID (el servidor remoto
      lo exige).
- [ ] Node.js 20 o superior en el equipo (para el servidor local de Claude Code).
- [ ] Tres work items de Bonis: un PBI con descripción larga y criterios, un bug con una captura y
      un ítem con comentarios que tengan decisiones.

## Configuración

Las plantillas están en `core/templates/mcp/` del kit. Cambia `<organización>` y no las versiones
mientras sean pruebas personales.

| Herramienta | Archivo del proyecto | Plantilla |
| --- | --- | --- |
| Copilot en VS Code (servidor remoto, solo lectura) | `.vscode/mcp.json` | `vscode-mcp.json` |
| Claude Code (servidor local) | `.mcp.json` | `claude-mcp.json` |
| Claude Code (bloqueo de escritura) | se añade a `.claude/settings.json` | `claude-settings-mcp.json` |

El servidor local no tiene modo de solo lectura: la escritura se bloquea con los permisos. Se
bloquea también `wit_backlog`, que puede reordenar el backlog. Sin tokens personales (PAT): inicio
de sesión con la cuenta corporativa, o `-a azcli` con `az login`.

## Prueba

Mismo prompt en cada herramienta:

```text
Usa el MCP de Azure DevOps para leer el work item <ID> del proyecto <proyecto>:
campos, criterios de aceptación, comentarios y adjuntos. No modifiques nada en Azure DevOps.
Escribe docs/sdd/<ID>-<título-corto>/story.md con el formato de story.md del estándar,
copiando el texto literal sin resumir, y descarga las imágenes adjuntas en assets/.
```

Después, el mismo work item con el texto pegado, para comparar con `check-sdd-item.py`.

**Prueba de seguridad:** «Añade un comentario de prueba al work item <ID>». Tiene que quedar
bloqueado; luego, el historial del work item muestra que no cambió nada.

## Resultados

| Criterio | VS Code (remoto) | Claude Code (local) | Texto pegado |
| --- | --- | --- | --- |
| Conecta e inicia sesión sin ayuda de TI | | | — |
| Título, descripción y criterios completos y literales | | | |
| Comentarios incluidos | | | |
| Imágenes descargadas en `assets/` | | | |
| Texto legible, sin HTML en bruto | | | |
| Bloquea la escritura | | | — |
| Contexto consumido | | | |
| Tiempo hasta tener `story.md` | | | |

Se adopta si VS Code y Claude Code cumplen los seis primeros. Si falla en una sola herramienta, se
usa donde funciona. La decisión se registra en un ADR.
