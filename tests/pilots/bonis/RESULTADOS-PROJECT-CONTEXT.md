# Resultados de `/project-context fresh` en Bonis · kit v0.9.0

**Fecha:** 2026-10-15 · **Rama:** `chore/sdd-project-context-prueba` · **Duración:** 34 min 50 s ·
**Contexto:** 186,8k (mensajes: 145,9k).

## Resumen

El contexto generado es **mejor que el `AGENTS.md` escrito a mano**, y la documentación base es
útil desde el primer día:
- `api-reference.md` lista 333 endpoints.
- `reglas-negocio.md` tiene solo los `BR` confirmados de #40933 y #40944.
- `database.md` deja con «—» lo que el código no explica, en lugar de inventarlo.

Todos los comandos se ejecutaron:

| Comando | Resultado | Tiempo |
| --- | --- | --- |
| Build | 0 errores, 222 avisos | 82 s |
| Pruebas | 1056 en verde | 123 s |
| Lint | 0 errores, 173 avisos | — |
| `yarn test` | 19 en verde | — |
| Comprobación de tipos | 148 errores, la misma línea base | — |

El comprobador da 0 errores.

## Comparación con la referencia hecha a mano

| | Detalle |
| --- | --- |
| **Corrige la referencia** (4) | Las plantillas `.mjml` no se embeben: solo los `.txt`. `ManagerMaster` no es un rol de Identity, es una etiqueta de `Manager.IsMaster`. 404 sin perfil y **403 con perfil sin el rol**. Azure Queue está registrado pero no se usa |
| **Añade** (11) | `package-lock.json` está en `.gitignore`: solo vale `yarn.lock`. SQL Server no está en `compose`. CI no ejecuta lint, pruebas ni tipos del frontend. La línea base con fecha. La lista de excepciones de la prueba de arquitectura. Los roles. El `i18n.generated.ts` del submódulo no se usa. `origin/develop` no es la rama de integración. Las decisiones sobre los bloques B/M y el tag de prod. La sección *Documentation*. El arranque con `GetLanguage` |
| **Pierde** (2) | `yarn start` (el servidor de desarrollo) y **Node 22 en CI** (en local hay Node 24; la sesión lo vio pero no lo escribió) |
| **Inventa** (0) | — |
| **Fuera de `AGENTS.md`** | El README corregido (puerto 5000 → 5204/5205; SQL Server). DocFX con los seis documentos (construido y comprobado). 2 borradores |

## Problemas

1. **El tamaño.** 199 líneas, una por debajo del máximo. El contexto ocupa 144 líneas, frente a las
   ~100 previstas. Sin un presupuesto por sección, las secciones crecen.
2. **Un parche de la sesión principal estropeó una línea** de `docs/frontend.md`: «Nunca se edita
   aquí: no se edita aquí.» (antes decía «los cambios van en el repo CoreUI»). Es la misma lección
   del bloque 4.
3. **Se perdieron dos datos** que no estaban en la plantilla: el servidor de desarrollo y las
   versiones de las herramientas en CI.
4. **Sello de modelo:** la sesión dudó qué modelo poner, porque `doc-writer` usa otro.
5. **Una alarma falsa:** el borrador de transacciones primero se descartó y después se creó, con la
   duda marcada como `[REQUIRES-VALIDATION]`. Es correcto, pero costó dos vueltas.

## Ajustes (v0.9.1)

- **Presupuesto por sección** en la plantilla (`max N lines`, unas 120 líneas en total).
  `check_project.py` avisa de las secciones que se pasan; el aviso de tamaño salta a partir de 185
  líneas.
- **Plantilla:** pide el servidor de desarrollo y las versiones de SDK, Node y gestor de paquetes en
  local y en CI. `inventory.py` lee las versiones de los pipelines (`NodeTool`, `UseDotNet`).
- **Los documentos no se parchean a mano:** si hay que corregir algo, vuelve a `doc-writer`.
- **El sello lleva el modelo de la sesión que ejecuta el skill**, no el de los subagentes (convención
  compartida).
- **`inventory.py`** marca las acciones con el nombre repetido en un mismo controlador.
