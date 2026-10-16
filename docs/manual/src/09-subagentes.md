# Subagentes

:::lead
Un subagente es un asistente con un rol estrecho, permisos limitados y un modelo propio. La skill
de la sesión principal le pasa un paquete cerrado con todo lo que necesita, él hace un trabajo
acotado y devuelve un informe con un formato fijo. Tú normalmente no los invocas: los usan las
skills.
:::

## Por qué subagentes

@@figure delegacion.svg | La sesión principal decide y verifica; los subagentes hacen trabajo acotado con un paquete cerrado.

- **Contexto limpio.** La búsqueda en 40 archivos o la implementación de una tarea ocurre en el
  contexto del subagente; a la sesión principal solo llega el resumen. Las sesiones duran más y
  gastan menos.
- **El modelo adecuado.** Buscar es barato (Haiku); revisar exige razonamiento (Opus).
- **Independencia.** `qa-reviewer` recibe fuentes, no conclusiones: no hereda la opinión de quien
  implementó.
- **Permisos mínimos.** Quien busca no puede editar; quien revisa no puede tocar el código.

:::warn Los subagentes no tienen memoria
Cada llamada empieza de cero: por eso el paquete lleva todo (tarea, SPECs literales, archivos con
rangos de líneas, comandos exactos, reglas). Y su informe **no es evidencia**: la sesión principal
vuelve a ejecutar las comprobaciones.
:::

## Formato y adaptadores

Cada subagente se define una vez en el kit (`core/agents/<nombre>.md`), en formato neutral, y el
instalador genera el de cada herramienta:

```yaml
---
name: backend-dev
description: Implements exactly one backend task of an approved WBS ... Use when wbs-execution
  delegates a task whose role is Backend; not for design, analysis or open-ended changes.
permissions: [read, edit, execute]   # read | edit | execute
model_tier: standard                 # fast | standard | reasoning
sdd_steps: [3]                       # pasos del flujo donde participa
skills: []
status: stable                       # solo se instalan los stable
---
Instrucciones (en inglés). El informe que devuelve, en español.
```

| Neutral | Claude Code (`.claude/agents/*.md`) | Copilot (`.github/agents/*.agent.md`) |
| --- | --- | --- |
| `read` | `Read, Grep, Glob` | `read`, `search` |
| `edit` | `Edit, Write` | `edit` |
| `execute` | `Bash` | `execute` |
| `model_tier` | `haiku` / `sonnet` / `opus` | El modelo de la conversación |

En Claude Code los ves con `/agents`; en VS Code, en el selector de agentes. En Copilot se marcan
`user-invocable: false`: los usan las skills con `runSubagent`.

## Resumen de los siete

| Subagente | Hace | Permisos | Modelo | Lo usan |
| --- | --- | --- | --- | --- |
| `code-explorer` | Busca y mapea código para responder una pregunta | Lectura | fast (Haiku) | Casi todas las skills |
| `backend-dev` | Implementa **una** tarea de backend, pruebas primero | Lectura, edición, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix`, `project-context` |
| `frontend-dev` | Implementa **una** tarea de frontend, con traducciones | Lectura, edición, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix` |
| `qa-reviewer` | Revisa el cambio e intenta romperlo | Lectura, ejecución | reasoning (Opus) | `qa-review` |
| `runtime-tester` | Arranca la aplicación en local y comprueba pantallas o endpoints | Lectura, ejecución | standard (Sonnet) | `qa-review` (opcional) |
| `doc-writer` | Escribe comentarios y `docs/` desde un paquete de hechos | Lectura, edición | fast (Haiku) | `document-code`, `document-project`, `project-context` |
| `migration-reviewer` | Revisa migraciones de EF Core antes de cerrar una tarea | Lectura, ejecución | standard (Sonnet) | `wbs-execution`, `quick-fix`, `qa-review` |

## code-explorer

**Rol:** búsqueda de solo lectura. Responde **una** pregunta precisa (un flujo, una entidad, un
patrón, dónde se decide algo) para que la sesión principal lea la respuesta y no el repositorio.

**Cómo trabaja:** busca primero por nombre y por texto; abre un archivo solo cuando la búsqueda
muestra que responde; en archivos de más de unas 300 líneas, solo los rangos; **como máximo 15
archivos**. Nunca lee `bin/`, `obj/`, `node_modules/`, lockfiles ni código generado. Nunca abre
`.env*`; los `appsettings*.json`, solo por los nombres de sección. Si encuentra un secreto literal,
lo reporta como `ruta:línea — literal sensible` sin copiar el valor. Busca siempre las pruebas que
cubren lo que reporta. Lo que infiere sin verlo va marcado *(no verificado)*.

:::out Informe (máximo 60 líneas)
**Respuesta:** el menú lateral se construye en SideMenu.tsx a partir de una lista fija; la visibilidad
por rol la decide hasPermission() de core/permissions.ts.
**Archivos:**
- ClientApp/src/layout/SideMenu.tsx:40-96 — construye las entradas del menú
- ClientApp/src/core/permissions.ts:12-35 — hasPermission(rol, permiso)
- Api/Authorization/Permissions.cs:8-60 — catálogo de permisos del backend
**Patrones a reutilizar:** entrada de menú con permiso → «Clientes» en SideMenu.tsx:52
**Pruebas existentes:** ClientApp/src/layout/SideMenu.test.tsx · MiProyecto.Tests/Authorization/PermissionsTests.cs
**No cubierto / dudas:** cómo llegan los roles al cliente (no verificado: parece venir del token)
:::

:::tip Tú también puedes usarlo
En Claude Code puedes pedir directamente «usa code-explorer para encontrar dónde se calcula el
total de una factura y qué pruebas lo cubren». Mantiene limpia tu sesión.
:::

## backend-dev

**Rol:** implementa **exactamente una** tarea de backend de una WBS aprobada (.NET, EF Core,
servicios, controllers, jobs, autorización). No diseña.

**Paquete que recibe:** ID, título y descripción de la tarea · sus SPECs, literales · los contratos
que debe respetar · los archivos con rangos de líneas · los comandos exactos de build, test y lint ·
las convenciones de `AGENTS.md` · los riesgos.

**Cómo trabaja:**

1. **Pruebas primero, antes de tocar producción.** Escribe las pruebas de las SPECs y las ejecuta:
   deben fallar por el motivo esperado. Guarda esa línea como *Rojo*. Las pruebas de
   caracterización (fijan el comportamiento actual) deben pasar con el código de hoy.
2. Si la tarea **solo añade pruebas** de algo que ya existe, demuestra que pueden fallar con una
   **mutación temporal** del código (invertir una condición), las ejecuta, revierte y comprueba que
   el diff de producción queda vacío: *Rojo (mutación)*.
3. Implementa el cambio mínimo siguiendo los patrones del proyecto. Comentarios en español con
   `#<id>` cuando el cambio no es obvio.
4. Verifica con los comandos del paquete. **Hasta 3 intentos** con la misma comprobación; al
   tercero, devuelve un bloqueo.

**Límites:** solo los archivos del paquete y sus pruebas (otro estrictamente necesario, en *Fuera
del paquete*). Nunca `docs/sdd/`, rutas protegidas, migraciones ni contratos públicos salvo que el
paquete lo diga. Nunca commit, cambios de rama ni versiones de paquetes. Nunca secretos.

**Se para y pregunta** ante una regla o valor que el paquete no define, un diseño no
implementable, pruebas que ya fallaban, o si hace falta una migración, un cambio de contrato o un
archivo de otra capa.

:::out Informe (máximo 80 líneas)
**Estado:** ✅ Hecha
**Cambios:** Permissions.cs — nuevo permiso ViewOffers para Comercial y JefeVentas
**Archivos:** Api/Authorization/Permissions.cs · MiProyecto.Tests/Authorization/PermissionsTests.cs (nuevo) · Fuera del paquete: ninguno
**Pruebas:** 3 escritas · Rojo: dotnet test --filter PermissionsTests → 3 fallidas (ViewOffers no existe) · Verde: 3 pasan
**Validación:** dotnet build → 0 errores, 15 avisos (línea base 15) · dotnet test → 301/301
**Hallazgos:** Api/Authorization/Permissions.cs:77 — permiso Legacy sin uso
:::

## frontend-dev

**Rol:** implementa **exactamente una** tarea de frontend (React, TypeScript, componentes,
formularios, **traducciones en todos los idiomas**). Igual que `backend-dev`, con estas diferencias:

- Pruebas primero **cuando el proyecto puede probarlo** con sus herramientas. Si no (por ejemplo,
  no hay librería de pruebas de componentes), lo dice y escribe los pasos de comprobación manual.
- **Textos visibles** por el sistema de traducción, en todos los idiomas del paquete, en la misma
  tarea. Reutiliza claves; ante una casi igual (mayúsculas, espacios) pregunta. Nunca inventa una
  traducción: la deja fuera y reporta `[PENDING-TRANSLATION: <clave> → <idioma>]`. Mantiene orden,
  sangría y codificación de los archivos.
- Verifica con lint, pruebas, type check y build si se pide.
- Nunca toca submódulos compartidos ni rutas protegidas (por ejemplo `core-ui`) ni añade
  dependencias. Se para si la tarea necesita un cambio de backend.
- Su informe añade **Traducciones:** claves añadidas por idioma y pendientes.

## qa-reviewer

**Rol:** revisión independiente y adversarial de un work item implementado. **Nunca edita** nada:
devuelve hallazgos a `qa-review`, que los verifica.

**Recibe fuentes, no conclusiones:** el ID y la carpeta, los archivos a leer, `base`/`head` y el
comando para ver cada diff, los archivos con su tamaño, `AGENTS.md`, los comandos de prueba y si
puede ejecutarlos; en la ronda 2, los hallazgos a revisar y el diff de la corrección.

**Qué busca, en cada cambio:**

- **SPECs y criterios:** implementados de verdad, con sus bordes (vacío, nulo, otros roles,
  límites, primer y último elemento).
- **Contratos** de 03/04 y el contrato de errores de `AGENTS.md`.
- **Seguridad:** autorización y aislamiento de tenant en cada endpoint o rama nueva, validación de
  entrada, secretos, datos personales en logs.
- **Regresiones:** quién llama a cada método cambiado, otros roles o flujos que comparten código,
  firmas de jobs o datos serializados.
- **Pruebas:** cada SPEC con prueba o comprobación manual documentada; casos negativos; pruebas que
  fallarían sin el cambio.
- **Traducciones**, **reglas del proyecto y rutas protegidas**, y las mitigaciones de `06`.

Puede ejecutar las pruebas; nunca arranca la aplicación, instala paquetes ni ejecuta git que
cambie estado (solo `diff`, `show`, `log`, `grep`, `blame`).

**Reglas:** cada hallazgo tiene `ruta:línea`, qué está mal, la SPEC o regla que incumple, un
**escenario concreto** (entrada o estado → resultado incorrecto) y cómo lo confirmó. Si no puede
escribir el escenario, no es un hallazgo (como mucho 3 *Dudas*). Nada de formato ni estilo.

:::out Informe (extracto)
**Resultado:** 0 altos · 1 medio · 1 bajo
QA-01 · Media · ClientApp/src/layout/SideMenu.tsx:88
**Qué:** el rol JefeVentas no ve «Ofertas».
**Por qué:** SPEC-02 (CA-02: la ven Comercial y Jefe de ventas).
**Escenario:** usuario con rol JefeVentas abre el menú → no aparece la entrada.
**Confirmado con:** yarn test SideMenu → 1 fallida (prueba añadida en una copia temporal)
**Cobertura de SPECs:** SPEC-01 → PermissionsTests · SPEC-02 → SideMenu.test.tsx (sin caso JefeVentas)
**Pruebas ejecutadas:** dotnet test → 301/301 · yarn test → 48/48
**Dudas:** ninguna
:::

## runtime-tester

**Rol:** arranca la aplicación en local con los comandos documentados, comprueba las pantallas o
endpoints que cambiaron y **para lo que arrancó**. Nunca edita código, configuración, secretos ni
datos.

1. **Requisitos:** lee en `AGENTS.md` qué necesita (servicios, base de datos, usuario y roles
   locales). Si falta algo o pide credenciales, devuelve `No ejecutado (<motivo>)` y los pasos
   manuales.
2. **Arranca** en segundo plano, con la salida en un archivo; espera como máximo unos 3 minutos.
   Hasta 2 intentos.
3. **Endpoints:** los llama en local (`curl` o `Invoke-WebRequest`) y compara código de estado y
   la parte relevante del cuerpo.
4. **Pantallas:** con la herramienta de automatización del proyecto si existe (Playwright); si no,
   no finge: lista las comprobaciones manuales.
5. **Para** cada proceso que arrancó, y solo esos. Dice qué datos locales creó.

Solo URLs locales: nunca Dev, Staging ni producción. Un arranque fallido es `No ejecutado`, nunca
un aprobado.

## doc-writer

**Rol:** escribe la documentación que define el paquete, con los hechos que da. **Nunca cambia
código.**

**Reglas de escritura:**

- C#: `/// <summary>` de una o dos frases; `<remarks>` para la regla o decisión con su fuente
  (`#<id>`, `BR-XX`). `<param>` es todo o nada (documentar solo algunos da CS1573).
- TypeScript: `/** … */`, con `@param` y `@returns` solo si aportan.
- Dice para qué sirve y por qué, desde los hechos; nunca narra el código línea a línea.
- Un símbolo marcado **«desde el código»** se describe por lo que hace (propósito, parámetros,
  retorno, excepciones, efectos: escrituras, caché, llamadas externas), **nunca la intención**.
- **Nunca** cita números de línea (caducan), ni lista quién llama a un símbolo, ni copia un secreto.
  En XML, los nombres de código van en `<c>` o `<see cref>`, nunca entre comillas invertidas.
- Edita en el sitio, manteniendo codificación, BOM y finales de línea. Nada de formato, imports,
  renombrados ni reordenaciones: `comment_only.py` lo detectaría.

:::out Informe (máximo 40 líneas)
**Estado:** ✅ Hecha
**Comentarios:** Api/Controllers/OffersController.cs → 4 añadidos · 1 actualizado
**docs/:** api-reference.md → Ofertas
**Sin documentar:** GetLegacy (el código no muestra para qué se usa)
**Fuera del paquete:** ninguno
:::

## migration-reviewer

**Rol:** revisa las migraciones de Entity Framework Core de una tarea antes de cerrarla. Solo
lectura.

**Lista de comprobación:**

1. **Coincide con el modelo:** cada operación de `Up()` sale de un cambio de entidad o
   configuración de la tarea, y viceversa; el *snapshot* concuerda.
2. **`Down()` revierte `Up()`**, operación a operación, en orden inverso. Si no puede restaurar
   datos (una columna borrada), lo dice.
3. **Pérdida de datos:** `DropColumn`, `DropTable`, estrechar un tipo, un renombrado que EF generó
   como borrar + añadir.
4. **NOT NULL sin valor por defecto** en una tabla con filas.
5. **Bloqueos y tiempo:** índices en tablas grandes sin `ONLINE`, reconstruir columnas, actualizar
   todas las filas.
6. **Claves e índices:** índice único sobre datos que pueden repetirse, borrado en cascada no
   pedido, un índice que una consulta usa y desaparece.
7. **SQL a mano** (`migrationBuilder.Sql`): idempotente, en la misma transacción, sin valores de un
   entorno.
8. **Arranque:** si las migraciones se aplican al arrancar, una lenta o fallida para el despliegue.

Puede ejecutar `dotnet ef migrations script <anterior> <esta> --idempotent` para leer el SQL; nunca
`dotnet ef database update`.

:::out Informe (máximo 30 líneas)
**Estado:** ⚠️ Riesgos
alta · Migrations/20261015_AddOfferStatus.cs:18 · columna Status NOT NULL sin valor por defecto en
     Offers (tabla con datos) · añadir defaultValue: 0 o un paso de datos previo
**Comprobado:** 1–8 · dotnet ef migrations script 20260930_Init 20261015_AddOfferStatus --idempotent
:::

Un riesgo **alta** devuelve la tarea a `backend-dev` antes de marcarla hecha.
