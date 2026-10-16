# Hooks (ADR-0023)

Un solo hook de Claude Code en Python, sin dependencias: `sdd_guard.py`. `install.py` lo copia a
`.agents/hooks/` (se versiona) y lo registra en `.claude/settings.json` junto con los permisos
`deny`. Sustituye a los hooks PowerShell de `sdd-clavijo`.

| Modo | Evento | Herramientas | Qué hace |
| --- | --- | --- | --- |
| `pre` | PreToolUse | Read, Edit, Write, MultiEdit, NotebookEdit, Bash, PowerShell | Bloquea editar una ruta `protected` y leer o editar un archivo de `secrets`, también desde un comando de shell |
| `post` | PostToolUse | Edit, Write, MultiEdit | Ejecuta el formateador de `format` para la extensión, avisa si el archivo ya no es UTF-8 y avisa de los `patterns` |

La configuración está en `sdd-guardrails.json`, en la raíz del proyecto (plantilla en
`core/templates/`). Salida: 0 = sin decisión · 2 = bloqueado (pre) o aviso que el agente lee (post).
Un error interno sale con 0: el hook nunca bloquea por un fallo propio.

Es un aviso temprano. Las reglas obligatorias también se comprueban con pruebas o con
`pr-check.py` (ADR-0012).

Para probarlo a mano:

```powershell
'{"tool_name":"Read","tool_input":{"file_path":"Bonis/appsettings.Development.json"}}' | python .agents/hooks/sdd_guard.py pre
echo $LASTEXITCODE   # 2
```
