# Guardarraíles

:::lead
Las reglas de `AGENTS.md` dicen a la IA qué no debe hacer, pero una instrucción se puede olvidar.
Los guardarraíles (ADR-0023) hacen que cada regla obligatoria tenga, además, **una comprobación que
no depende de que la IA obedezca**: un permiso que lo impide, un hook que lo bloquea, una prueba
que falla o un script que lo detecta antes del PR.
:::

## Las cinco capas

@@figure guardarrailes.svg | Cinco capas, de la más temprana (antes de actuar) a la última (antes del PR).

| Capa | Pieza | Qué hace | En qué herramienta |
| --- | --- | --- | --- |
| 1 | Permisos `deny` en `.claude/settings.json` | Impide leer secretos y ejecutar `git commit`, `git push`, `git reset --hard`, `git clean`, `git branch -D`, `rm -rf` | Claude Code |
| 2 | Hook `sdd_guard.py pre` | Bloquea leer o editar secretos y editar rutas protegidas, también desde comandos de shell | Claude Code |
| 3 | Hook `sdd_guard.py post` | Tras cada edición: formatea, avisa si el archivo dejó de estar en UTF-8 y avisa de patrones obligatorios | Claude Code |
| 4 | `ArchitectureTests.cs` | Pruebas que fallan si se rompe una regla de arquitectura | Todas (`dotnet test`, y el pipeline) |
| 5 | `pr-check.py` | Commits, rutas protegidas, secretos, archivos del kit, tamaño de `AGENTS.md`, UTF-8 | Todas (y el pipeline en la fase 4) |

:::note En Copilot no hay hooks
Copilot no ejecuta hooks ni respeta `.claude/settings.json`. Ahí las capas 4 y 5 son las que
garantizan las reglas: por eso `pr-check.py` es obligatorio antes de cada PR, uses la herramienta
que uses.
:::

## Permisos deny

El instalador añade 23 reglas a `permissions.deny` de `.claude/settings.json`, sin tocar las que ya
tuvieras:

```json
"deny": [
  "Read(./.env)", "Read(./.env.*)", "Read(./**/.env)", "Read(./**/.env.*)",
  "Read(./**/appsettings.*.json)", "Read(./**/secrets.json)",
  "Read(./**/*.pfx)", "Read(./**/*.pem)", "Read(./**/*.key)",
  "Read(./**/nuget.config)", "Read(./**/NuGet.Config)", "Read(./**/nuget.*.config)",
  "Bash(git commit *)", "Bash(git push *)", "Bash(git push)", "Bash(git reset --hard *)",
  "Bash(git clean *)", "Bash(git branch -D *)", "Bash(rm -rf *)",
  "PowerShell(git commit *)", "PowerShell(git push *)", "PowerShell(git reset --hard *)",
  "PowerShell(Remove-Item * -Recurse *)"
]
```

:::note appsettings.json y nuget.config (ADR-0028)
`nuget.config` se bloquea siempre: sus credenciales no le sirven a la IA para nada. `appsettings.json`
no está en las reglas deny, pero sí en los `secrets` por defecto del hook, porque en el piloto de
Calls4Grants guardaba cuatro secretos versionados y un subagente lo leyó entero. El hook respeta
`secretsAllowed`: si `inventory.py` muestra que el `appsettings.json` de tu proyecto no tiene
secretos y los work items necesitan editarlo, `/project-context` te propone pasarlo ahí. La
estructura (sus secciones) la da `inventory.py` sin leer los valores.
:::

## El hook sdd_guard.py

Un solo script de Python, sin dependencias, en `.agents/hooks/sdd_guard.py` (versionado). El
instalador lo registra en `.claude/settings.json`:

```json
"hooks": {
  "PreToolUse":  [{ "matcher": "Read|Edit|Write|MultiEdit|NotebookEdit|Bash|PowerShell",
                    "hooks": [{ "type": "command", "command": "python",
                                "args": ["${CLAUDE_PROJECT_DIR}/.agents/hooks/sdd_guard.py", "pre"],
                                "timeout": 30 }] }],
  "PostToolUse": [{ "matcher": "Edit|Write|MultiEdit",
                    "hooks": [{ "type": "command", "command": "python",
                                "args": ["${CLAUDE_PROJECT_DIR}/.agents/hooks/sdd_guard.py", "post"],
                                "timeout": 120 }] }]
}
```

| Modo | Evento | Bloquea o avisa | Código de salida |
| --- | --- | --- | --- |
| `pre` | Antes de Read, Edit, Write, MultiEdit, NotebookEdit, Bash, PowerShell | **Bloquea** editar una ruta `protected` y leer o editar un archivo de `secrets`, también si el comando de shell lo nombra | 2 = bloqueado · 0 = sigue |
| `post` | Después de Edit, Write, MultiEdit | Ejecuta el formateador de `format`; **avisa** si el archivo ya no es UTF-8 y de cada `pattern` incumplido. El agente lee el aviso y corrige | 2 = aviso para el agente · 0 = nada |

Si el propio hook falla (un error interno), sale con 0: **nunca bloquea por un fallo propio**. Desde
la v0.13.0 acepta el JSON con BOM que manda Windows PowerShell 5.1 por la entrada estándar; antes lo
descartaba sin avisar y no bloqueaba nada.

### Lo que verás

Salidas reales del hook con la configuración de ejemplo:

:::out Leer un archivo de entorno
fi-sdd-standard · bloqueado: «Api/appsettings.Development.json» puede contener secretos
(patrón «**/appsettings.*.json»); pide a una persona el dato que necesitas (sdd-guardrails.json, ADR-0023)
:::

:::out Un cat .env desde el shell
fi-sdd-standard · bloqueado: el comando usa «.env», que puede contener secretos (patrón «.env»)
(sdd-guardrails.json, ADR-0023)
:::

:::out Editar una ruta protegida
fi-sdd-standard · bloqueado: «Api/Legacy/Old.cs» es una ruta protegida (patrón «Api/Legacy/**»);
el cambio va en su origen (sdd-guardrails.json, ADR-0023)
:::

:::out Aviso de patrón tras escribir un controller sin autorización
fi-sdd-standard · Api/Controllers/PingController.cs:
  - Todo controller declara su autorización ([Authorize] o [AllowAnonymous])
:::

### Probarlo a mano

```powershell
'{"tool_name":"Read","tool_input":{"file_path":"Api/appsettings.Development.json"}}' | python .agents\hooks\sdd_guard.py pre
$LASTEXITCODE     # 2 = bloqueado
'{"tool_name":"Read","tool_input":{"file_path":"Api/appsettings.json"}}' | python .agents\hooks\sdd_guard.py pre
$LASTEXITCODE     # 0 = permitido
```

## sdd-guardrails.json

La configuración del hook y de `pr-check.py`, en la raíz del proyecto, versionada. La crea
`install.py` y la completa `/project-context`. Las rutas y globs son relativas a la raíz, con la
sintaxis de `.gitignore` (`**` para cualquier profundidad).

| Clave | Tipo | Para qué | La usa |
| --- | --- | --- | --- |
| `protected` | Lista de globs | Rutas que la IA nunca edita: librerías compartidas, submódulos, código generado, documentación de otro equipo | Hook `pre`, `pr-check.py` |
| `secrets` | Lista de globs | Archivos que nadie lee ni sube | Hook `pre`, `pr-check.py` |
| `secretsAllowed` | Lista de globs | Excepciones a `secrets` (por ejemplo, una plantilla `.env.example` sin valores). Cada una, justificada en el PR | Hook, `pr-check.py` |
| `format` | Extensión → comando, o lista de comandos | Formateador tras cada edición; `{file}` es el archivo. Con una lista, los ejecuta en orden (por ejemplo `eslint --fix` y después `prettier`) | Hook `post` |
| `formatTimeout` | Segundos (60 por defecto) | Tiempo máximo de cada comando de `format`. Si se pasa, se omite con un aviso: es habitual en el primer arranque en frío | Hook `post` |
| `patterns` | Lista de `{glob, require/forbid, message}` | Reglas que una expresión regular puede comprobar | Hook `post` |

:::file sdd-guardrails.json (ejemplo completo)
{
  "protected": [
    "ClientApp/src/core-ui/**",
    "docs/modernizacion/**"
  ],
  "secrets": [".env", ".env.*", "**/appsettings.json", "**/appsettings.*.json", "**/secrets.json",
              "**/nuget.config", "**/nuget.*.config", "**/.npmrc", "**/*.pfx", "**/*.pem", "**/*.key"],
  "secretsAllowed": [".env.example"],
  "format": {
    ".cs":  ["dotnet", "csharpier", "format", "{file}"],
    ".tsx": [["npx", "eslint", "--fix", "{file}"], ["npx", "prettier", "--write", "{file}"]]
  },
  "formatTimeout": 60,
  "patterns": [
    {
      "glob": "**/Controllers/*Controller.cs",
      "require": "\\[(Authorize|AuthorizeRoles|AllowAnonymous)",
      "message": "Todo controller declara su autorización ([Authorize] o [AllowAnonymous])"
    },
    {
      "glob": "ClientApp/src/**/*.tsx",
      "forbid": "console\\.log\\(",
      "message": "Sin console.log en componentes: usa el logger del proyecto"
    }
  ]
}
:::

:::warn Revísalo a mano en el PR
- Las rutas protegidas deben ser las del proyecto (*Protected paths* de `AGENTS.md`):
  `check_project.py` avisa si no coinciden.
- Nada en `secretsAllowed` sin un motivo.
- Un formateador solo si se ejecutó y funciona (lo verifica `/project-context`): un comando
  que falla en cada edición es ruido.
- Al actualizar el kit, `install.py` añade los `secrets` por defecto que falten (nunca quita
  ninguno) y lo dice en su informe.
:::

## Pruebas de arquitectura

`/project-context` copia `ArchitectureTests.cs` al proyecto de pruebas
(`<Tests>/Architecture/`) y `backend-dev` rellena sus marcadores. Son pruebas xUnit por reflexión:
corren con el resto de la suite y en el pipeline.

| Prueba | Regla | Falla si… |
| --- | --- | --- |
| `Los_controllers_no_dependen_del_DbContext` | Los controllers usan servicios, nunca el `DbContext` | Un controller lo recibe en el constructor |
| `Todo_endpoint_declara_su_autorizacion` | Autorización explícita | Un controller sin atributo tiene una acción pública sin `[Authorize]`, `[AllowAnonymous]` ni requisito de autorización |
| `La_capa_de_datos_no_depende_de_los_servicios` | Dirección de dependencias | Un tipo de la capa de datos usa un tipo de la capa de servicios |

Los cuatro marcadores que se adaptan:

```csharp
//   {{TestNamespace}}     espacio de nombres del proyecto de pruebas (p. ej. MiProyecto.Tests)
//   {{AppMarkerType}}     un tipo público de la aplicación (p. ej. Program)
//   {{DataNamespace}}     capa de datos (p. ej. MiProyecto.Data)
//   {{ServicesNamespace}} capa de servicios (p. ej. MiProyecto.Services)
```

**Las reglas no se relajan.** Lo que ya las incumple va a una lista de excepciones con su motivo:

```csharp
// Controllers que todavía usan el DbContext directamente (deuda). Nombre de la clase y motivo.
private static readonly HashSet<string> DbContextExceptions = [
    "ReportsController", // consultas de solo lectura heredadas; work item #40712 para moverlas
];
```

Una excepción nueva la decide el tech lead; la lista solo debería encoger con el tiempo.

```powershell
dotnet test MiProyecto.Tests --filter "FullyQualifiedName~Architecture"
```

## La matriz: cada regla con su comprobación

| Regla de `AGENTS.md` | Permiso | Hook | Prueba | `pr-check.py` | Otra |
| --- | --- | --- | --- | --- | --- |
| No leer ni imprimir secretos | ✓ lectura | ✓ lectura y shell | — | ✓ archivos y patrones en el diff | `code-explorer` |
| No editar rutas protegidas ni submódulos | — | ✓ | — | ✓ | — |
| La IA no hace commit, push ni cambia de rama | ✓ | — | — | — | — |
| Formato del commit, `Ref: #id`, sin `fix #id`, sin firma de IA | — | — | — | ✓ | `check-sdd-item.py` |
| UTF-8 conservando el BOM | — | ✓ aviso | — | ✓ | `check-encoding.py --fix` |
| Artefactos del work item | — | — | — | ✓ | `check-sdd-item.py` |
| Archivos del kit solo cambian con `install.py` | — | — | — | ✓ | `.sdd-kit.json` |
| Los borradores no llegan a `dev`; adjuntos, `commit-message.md` y CSV fuera del repositorio | — | — | — | ✓ | `.gitignore` de `install.py` (ADR-0027) |
| `AGENTS.md` < 200 líneas | — | — | — | ✓ | `check_project.py` |
| Controllers sin `DbContext` | — | — | ✓ | — | — |
| Todo endpoint con autorización explícita | — | ✓ aviso | ✓ | — | — |
| Capas: datos sin servicios | — | — | ✓ | — | — |
| Documentar solo cambia comentarios | — | — | — | — | `comment_only.py` |
| Patrones obligatorios del proyecto | — | ✓ aviso | si se puede | — | `qa-review` |
| Textos visibles en todos los idiomas | — | — | — | — | `qa-review` (fase 4: en el PR) |
| No inventar reglas de negocio | — | — | — | — | Revisión humana y `qa-review` |
