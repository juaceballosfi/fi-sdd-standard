# ADR-0028 · Alcance de project-context y borradores con prioridad

- **Estado:** Aceptada
- **Fecha:** 2026-10-17
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0021, ADR-0023, ADR-0027

## Contexto

El primer `/project-context` del piloto de Calls4Grants (v0.11.0) hubo que repetirlo desde cero
(`tests/pilots/calls4grants/RESULTADOS-PROJECT-CONTEXT.md`). La sesión no falló en el contexto: se
desvió a arreglar lo que encontraba por el camino.

- El entorno no compilaba (PAT de NuGet vencido, enlace `ClientApp/src/core` roto, Node 24 en vez de
  22) y se descubrió a mitad de la skill; la sesión intentó resolverlo.
- Se fue a migrar y depurar los hooks antiguos de PowerShell y el formateador (tiempos de espera
  en frío, el BOM de PowerShell 5.1, rutas relativas de los hooks en subagentes).
- La instalación del kit no tenía commit, así que nada se podía descartar sin miedo a perderlo.
- `appsettings.json` y `nuget.config` no estaban en los `secrets` por defecto: un subagente leyó
  `appsettings.json` entero y una sesión imprimió los PAT de `nuget.config`.
- Las preguntas llegaron una a una en lugar de en un bloque.

Los hallazgos reales (secretos versionados, controllers sin autorización, `CONSUL_TOKEN` en consola)
acabaron en borradores sin orden: no se distinguía lo urgente de lo cosmético.

## Decisión

1. **`/project-context` deja el kit a punto; no arregla el proyecto.** Termina con contexto,
   documentos base, proyecto de pruebas, guardarraíles y `check_project.py` en 0 errores. Todo lo
   demás que haya que arreglar es un borrador y la sesión sigue. Una herramienta que falla tiene un
   intento; después se anota y se deja.
2. **Compuerta del entorno al empezar.** Antes de explorar: la instalación del kit con su commit,
   el preflight de `inventory.py` (SDK, Node, gestor, enlaces, submódulos) y `dotnet restore`. Lo
   que impide compilar **para la sesión** con los pasos para la persona; la IA no toca credenciales,
   configuración global ni SDK, ni abre los archivos de credenciales para diagnosticar.
3. **Borradores con prioridad** (convención compartida de las 9 skills y plantilla
   `enrich-us/templates/borrador.md`):

   | Prioridad | Cuándo |
   | --- | --- |
   | Urgente | Un secreto o un fallo de seguridad expuesto, o bloquea el build o al equipo |
   | Alta | Comportamiento incorrecto o riesgo en producción |
   | Media | Deuda que frena el trabajo |
   | Baja | Cosmético |

   El informe final los lista de más a menos urgente; `check_project.py` avisa de los urgentes y de
   los que no tienen prioridad. Los urgentes se crean en Azure DevOps en cuanto se hace el commit.
4. **Secretos por defecto:** se añaden `**/appsettings.json`, `**/nuget.config`,
   `**/nuget.*.config` y `**/.npmrc`; `nuget.config` también a las reglas deny. `install.py` añade
   los que falten a un `sdd-guardrails.json` existente, sin quitar ninguno. `inventory.py` lista los
   secretos versionados por archivo, línea y clave, nunca el valor; cada uno es un borrador Urgente.
   Un `appsettings.json` sin secretos que los work items necesiten editar puede ir a
   `secretsAllowed` con aprobación.
5. **Hooks antiguos:** pasan siempre las rutas protegidas y los patrones; un formateador solo si se
   ejecutó y tardó menos de unos 20 s. El hook antiguo se borra cuando se ha visto al guard
   bloquear, y con aprobación. `format` acepta una lista de comandos y `formatTimeout`.

## Consecuencias

- `project-context` v3.10: alcance, compuerta del entorno, bloque de preguntas con una línea para
  rellenar, reglas de hooks, el proyecto de pruebas con el adaptador de VSTest (`dotnet test` en el
  SDK local y en el del pipeline) y cómo seguir si se para.
- `sdd_guard.py` acepta el JSON con BOM de PowerShell 5.1 y omite con aviso un formateador lento.
- `install.py` recuerda hacer commit de la instalación antes de `/project-context`.
- Leer `appsettings.json` pasa a estar bloqueado por defecto: en proyectos sin secretos en él,
  hay que pasarlo a `secretsAllowed`. Se acepta: en el piloto estaba versionado con cuatro secretos.
- Arreglar los hallazgos del proyecto lleva work items propios, fuera de la sesión del kit.

## Alternativas consideradas

- Que `/project-context` arregle lo que encuentre: alarga la sesión sin límite y mezcla en un
  mismo commit el kit y cambios del producto que nadie ha priorizado.
- Prioridad libre en cada borrador: no se puede ordenar ni comprobar con un script.
- Mantener `appsettings.json` legible: en los repositorios de FI suele llevar secretos versionados.
