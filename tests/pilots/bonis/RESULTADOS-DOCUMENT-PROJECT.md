# Resultados de `/document-project` en Bonis

## Sesión 1 · el plan · kit v0.10.0

**Fecha:** 2026-10-15 · **Rama:** `chore/sdd-document-project-prueba` · **Modelo:** Sonnet (la guía
pedía Opus) · **Tiempo:** 3 min 45 s + 39 s · **Contexto:** 44,2k → 94,4k (mensajes: 53k).

### Lo que salió bien

- **Precondiciones:** rama, árbol limpio, kit y `check_project.py` comprobados antes de empezar.
- **Línea base ejecutada:** build 0 errores y 222 avisos, lint 0 errores y 173 avisos. Coinciden
  con `AGENTS.md`.
- **Dice lo que no midió:**
  - los tipos (148) vienen de `AGENTS.md`;
  - DocFX no se midió;
  - CS1591 no sirve porque Bonis no genera el XML.
- **Preguntas en un bloque**, y nada se escribió sin aprobación.
- **Fuera del plan:** `core-ui`, migraciones, código generado y `docs/modernizacion/`.
- **Coste bajo:** unos 50k de contexto para un repositorio de 1101 archivos de código.

### Problemas

| # | Problema | Causa | Ajuste (v0.10.1) |
| --- | --- | --- | --- |
| 1 | Las áreas grandes se partieron a mano por orden alfabético. `Bonis/Data` quedó en 7 trozos de 14 archivos: las entidades en unos bloques y sus `Configurations` en otros, y `ApplicationDbContext` en medio | El skill pedía partir «por subdominio», sin herramienta | El script parte las áreas sin separar una entidad de su configuración, una interfaz de su clase ni las partes de una clase parcial, y propone los bloques |
| 2 | `MaximumBaseController` salió como controlador base | El script lo detectaba por el nombre (`*Base*Controller`) | Es base solo si es abstracto o si otro controlador hereda de él |
| 3 | `AuthorizeRolesAttribute` acabó en el área de `GeneralNotice` y `DebugImpersonationMiddleware` en la de `Home` | Un tipo usado por un solo controlador se iba con él, aunque fuera infraestructura; el atributo se usa como `[AuthorizeRoles]` | La infraestructura (`Authorization`, `Middlewares`, `Startup`…) no se mueve a un controlador; `XAttribute` se busca también como `X` |
| 4 | Dijo «56 áreas marcadas dividir»: eran 25 | Una cifra estimada | Toda cifra sale de un script o un comando |
| 5 | «No leí el plan.md generado y no comprobé que los bloques respeten los límites» | No había forma de comprobarlo | `doc_coverage.py --check-plan`: cada archivo en un área y solo en una, y los límites |
| 6 | 75 pruebas sin área | Solo se asociaban por nombre exacto | También por prefijo (`MaximumBaseControllerAuthorizationTests`) |
| 7 | Las áreas partidas no tienen cifra de «Sin documentar» («parte de 7») | Se partieron después del script | El script da la cifra de cada parte |

### Decisión

El plan no se commitea. Se borra y se repite la sesión 1 con la v0.10.1 (Sonnet basta: el script
hace la parte mecánica), y después la sesión 2 con B-01.

## Sesión 1 (repetición) · kit v0.10.1

**Modelo:** Opus (cambiado con `/model` al empezar). **Tiempo:** 4 min 43 s + 19 s + 57 s ≈ 6 min.
**Contexto:** 44,2k → 124k (mensajes: 83,1k), frente a 94k de la primera vez con Sonnet.
**Propuesta:** 177 áreas en 45 bloques, del script; 5 áreas completas fuera.

- **Cómo trabajó:**
  - lanzó build, lint, tipos, CS1591 y DocFX en segundo plano, mientras revisaba las áreas
    sospechosas: la raíz, los controladores base, `MigrateNewId`, `Startup`, `Pages`,
    `Constants`, las pruebas sin área y las áreas completas;
  - escribió `plan.md` con un generador a partir del JSON del script más sus cambios, en vez de a
    mano.

- **Corrige los problemas de la primera vez:**
  - `Data` partida por entidad y configuración;
  - `MaximumBaseController` ya no cuenta como base;
  - la infraestructura queda en sus áreas;
  - B-01 = raíz, autorización, configuración, excepciones y middlewares; B-02 = startup y el
    controlador base.
- **Línea base completa y medida:**
  - build 222 avisos, lint 173, tipos 148, DocFX 0 errores y 8 avisos;
  - **CS1591: 4274 avisos en 465 archivos.** Bonis lo suprime con `NoWarn`; la sesión lo contó por
    su cuenta con `-p:NoWarn=`.
- **Cambios a la propuesta, con motivo:** solo pruebas sin área reasignadas, y un área nueva
  «Soporte de pruebas» en B-11.
- **A mejorar:**
  - respondió en inglés;
  - el comando de CS1591 tiene que quedar en el plan para que cada bloque mida igual (v0.10.2).
- **Tamaño del trabajo:** 45 bloques son 45 sesiones y 45 PR. Tras B-01 y un bloque de frontend se
  revisan los límites: las páginas del frontend tienen pocos símbolos por archivo.

**Plan escrito:** `--check-plan` con 0 errores y 9 avisos:
- 4 áreas de una sola clase o clase parcial por encima del límite (`ApplicationDbContext` 72,
  `ScannedDocumentsJobs` 81, `TrackingService` 89, `ImportExportResourceService` 70);
- 5 áreas completas sin bloque, a propósito.

La sección *Cómo se mide la línea base* deja el comando de cada cifra. Para CS1591, el script
deduplica mejor que un filtro a mano (4274 frente a 4343). Detalles para la v0.10.2:
- los comandos usan `.claude/skills/` en vez de `.agents/skills/`;
- las partes de `Data` salen en dos pasadas alfabéticas.

## Sesión 2 · B-01 · kit v0.10.1

**Modelo:** Sonnet. **Tiempo:** 54 min 34 s en total. Unos 35 min fueron la espera de la
confirmación; el trabajo fueron unos 20 min. **Contexto:** 44,2k → 172,3k (mensajes: 130,9k).
**Agentes:**
- 3 `code-explorer` en paralelo, de unos 3,5 min cada uno;
- 4 paquetes de `doc-writer`, de 1,5 a 2,5 min, dos a la vez.

### Resultado

| Medida | Antes | Después |
| --- | --- | --- |
| Símbolos documentados (proyecto) | 929/5810 (15 %) | 1034/5810 (17 %) |
| Clases de prueba con resumen | 11 | 13 |
| CS1591 | 4274 | 4170 (−104, cuadra con los símbolos) |
| Build | 222 avisos | 226 (ver abajo) |
| DocFX | 8 avisos | 8 |
| `comment_only.py` | — | solo comentarios, 22 archivos, CRLF y BOM conservados |

- 8 comentarios existentes corregidos porque contradecían el código. Un ejemplo: «default 300»
  cuando la propiedad vale 0 y el 300 lo pone el consumidor.
- `docs/`: `backend.md` (+37), `api-reference.md` (convenciones) y `architecture.md`.
- **Hallazgos reales:**
  - la clave HMAC de la cookie del dashboard de Hangfire está en el código (borrador creado);
  - un valor de `OneDataApiPat` está en `appsettings.Development.json`;
  - hay pocas pruebas de autorización y middlewares.

### Revisión de los comentarios (diff completo)

- **Correctos:** la mayoría. Excepciones con su código HTTP, middlewares, `AzureClientFactory`,
  `TenantMiddleware`, `AccessTokenFromQueryString` y `DebugImpersonation` dicen lo que hace el
  código, sin intención inventada.
- **Imprecisos o frágiles:**
  - números de línea en comentarios y en `docs/` (`Program.cs (línea 47)`,
    `BonisServiceCollectionExtensions.cs:244-281`): se quedan viejos con el siguiente cambio;
  - listas de «Consumo:» en `AppOptions`;
  - «Indicador de lista blanca» (vago);
  - «Existe, pero no se usa en este archivo» para `SymmetricKey`.
- **A verificar antes del commit:** el 404 de `[AuthorizeRoles]`. Los comentarios y `docs/` pasan
  de «sin perfil para el tenant → 404» a «solo si el tenant no existe (`BuildUserProfile` devuelve
  null); sin roles en un tenant existente → 403». Esto contradice *Project context* de `AGENTS.md`
  y depende de `UserProfileWorker.BuildUserProfile`, que está fuera del bloque. Si es cierto,
  `AGENTS.md` también debe cambiar.

### Problemas del kit

| # | Problema | Ajuste (v0.10.2) |
| --- | --- | --- |
| 1 | `comment_only.py` falló en la consola de Windows al imprimir ✓ | Fuerza UTF-8 |
| 2 | 3 falsos negativos de `doc_coverage.py`: un `//` entre el `///` y la declaración | Se salta los `//` |
| 3 | Números de línea y listas de consumidores en los comentarios | Regla en `doc-writer` |
| 4 | La sesión parcheó un `//` de `AppOptions.cs` con Edit (lo reconoció) | La regla dice «ni siquiera un `//`» |
| 5 | 226 frente a 222 avisos sin explicar. Probable causa: `NU1902`/`NU1903` de `System.Security.Cryptography.Pkcs` 9.0.11, que dependen de la base de vulnerabilidades | Comparar con un build de `HEAD` en un worktree temporal, por código |
| 6 | Un subagente vio un secreto en `appsettings.Development.json`; la sesión imprimió parte de la clave HMAC al hacer grep | `code-explorer`: `appsettings*` solo por secciones, y un literal sensible se informa como `ruta:línea`. Los permisos `deny` de la fase 3 son la defensa real |
| 7 | Respondió en inglés al empezar | Regla de idioma en `AGENTS.base.md` |

### Revisión antes del commit (misma sesión, 8 min 24 s)

- **El 404 está verificado.** `BuildUserProfile` solo devuelve null cuando
  `ITenantService.GetTenant` devuelve null; la condición no mira al usuario. Los comentarios eran
  correctos. *Project context* de `AGENTS.md` («no profile for that tenant → 404») queda
  desactualizado.
- **Números de línea:** `doc-writer` los quitó de 28 textos del bloque y las listas «Consumo:»
  desaparecieron; `comment_only.py` volvió a pasar. Siguen los números anteriores al bloque en
  `docs/` (de `/project-context`).
- **Los 226 avisos:**
  - `doc_coverage.py --warnings` sobre los logs reales da 222 avisos de código más 2 de NuGet,
    que MSBuild cuenta dos veces;
  - el build incremental del usuario dio 15, porque no recompila las pruebas;
  - no hay avisos nuevos;
  - vulnerabilidades reales: `System.Security.Cryptography.Pkcs` 9.0.11 y 10.0.11, y
    `System.Security.Cryptography.Xml` 10.0.11 (gravedad alta).
- **Worktree:** la sesión avisó de que contradecía una memoria del usuario («no worktrees»). La
  v0.10.2 ya no usa worktrees: compara con `avisos.md`.
