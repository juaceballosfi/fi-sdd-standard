# Vía rápida y QA

:::lead
Dos caminos complementan el flujo principal. La vía rápida (`quick-fix`) lleva un bug pequeño de
`story.md` a una corrección probada en una sola sesión, con una página de diseño en lugar de siete.
El camino de QA (`enrich-us … qa` y `test-cases`) convierte los criterios de aceptación en casos de
prueba con datos reales y un CSV para Azure Test Plans.
:::

## quick-fix · la vía rápida para bugs pequeños

:::card
<dl class="kv">
<dt>Sustituye</dt><dd>Los pasos 1, 2 y 3. Los pasos 4 (QA), 5 (documentación) y 6 (PR) no cambian</dd>
<dt>Quién</dt><dd>Dev, en una rama <code>fix/&lt;id&gt;-&lt;título&gt;</code></dd>
<dt>Comando</dt><dd><code>/quick-fix &lt;id&gt;</code></dd>
<dt>Lee</dt><dd><code>story.md</code> y <code>assets/</code>, <em>Project context</em>, el código</dd>
<dt>Escribe</dt><dd><code>bug.md</code>, <code>fix-plan.md</code>, código y prueba, <code>CHANGELOG.md</code>, <code>commit-message.md</code>, <code>bitacora.md</code></dd>
<dt>Subagentes</dt><dd><code>code-explorer</code> (causa), <code>backend-dev</code> o <code>frontend-dev</code> (corrección)</dd>
<dt>Modelo</dt><dd>Sonnet (fijado en Claude Code)</dd>
</dl>
:::

### La compuerta: 8 criterios

El mismo rigor que el flujo completo (evidencia en el código, pruebas primero, verificación real),
pero solo para bugs cuya causa y corrección caben en pocos archivos. **Un solo ✗ saca el bug de la
vía rápida** (ADR-0024).

| Criterio | Se cumple cuando |
| --- | --- |
| **Causa** | Se ve en el código con `archivo:línea`. Una afirmación, no una hipótesis |
| **Tamaño** | Como máximo 3 archivos de producción, de una sola capa (backend o frontend); las pruebas aparte |
| **Datos** | Sin migración ni cambio de una entidad o su configuración |
| **Contratos** | Sin cambios de rutas, forma de peticiones o respuestas, DTO que usen otros sistemas, eventos ni horarios de jobs |
| **Seguridad** | Sin cambios de autorización, roles, tenants ni autenticación |
| **Negocio** | Sin `[PENDING-BUSINESS]`: el comportamiento esperado sale de `story.md` o es obvio por el defecto |
| **Textos** | Ningún texto visible nuevo, o todos con su traducción en todos los idiomas |
| **Dependencias** | Ningún paquete nuevo ni actualizado |

### Qué hace, paso a paso

1. **Precondiciones:** no estás en `dev` ni `main`; no hay cambios sin commit fuera de la carpeta;
   lee comandos, línea base, rutas protegidas y reglas de traducción de *Project context*. Si la
   carpeta ya tiene `03`–`05`, está en el flujo completo: te manda a `/wbs-execution`.
2. **Lee el work item**: qué falla, cómo reproducirlo, qué se esperaba, dónde se vio.
3. **Busca la causa** con una pregunta precisa a `code-explorer` y abre solo las líneas que la
   prueban.
4. **Aplica la compuerta.** Con un ✗, se para **sin escribir `bug.md` ni código** y deja lo
   encontrado en `bitacora.md` para que el flujo completo empiece desde ahí.
5. **Confirmación** en un solo bloque: causa, cambio, prueba que fallará primero, regresión.
6. **Escribe el diseño**: `bug.md` (sello `quick-fix`) y `fix-plan.md` con la compuerta y su
   evidencia, la causa, el cambio, las pruebas con el *Rojo* esperado, los riesgos y la tarea
   `T-01` aprobada.
7. **Implementa `T-01`** con el subagente de la capa: prueba → *Rojo* → corrección → verde. Una
   prueba que pasa antes de la corrección no demuestra el bug: vuelve al subagente.
8. **Verifica** build, la suite de la capa, lint y tipos, el alcance (`git status`) y cada criterio
   de `bug.md`.
9. **Cierra**: `T-01` hecha, `CHANGELOG.md`, `commit-message.md` (`fix(<ámbito>): …`,
   `BUG-<id> — …`, **Causa**, `Ref: #<id>`) y el `git add`.

### Ejemplo: un bug que pasa

:::ask
/quick-fix 41020
:::

:::out Confirmación
## Corrección rápida — 41020 El total de la factura redondea mal los céntimos
Causa: el total se redondea por línea antes de sumar · Api/Services/InvoiceService.cs:212
Cambio: Api/Services/InvoiceService.cs → redondear una vez el total (1 archivo, backend)
Prueba primero: CalculateTotal_TresLineasConMedioCentimo_RedondeaUnaVez en
                MiProyecto.Tests/Services/InvoiceServiceTests.cs — hoy falla: devuelve 10,02 y no 10,01
Regresión: InvoiceServiceTests (14 pruebas) deben seguir en verde
Compuerta: ✓ todos · Riesgos: ninguno
Implementa: backend-dev (subagente)
¿Empiezo?
:::

:::out Cierre
## 🩹 Corrección rápida — 41020 El total de la factura redondea mal los céntimos
Causa: Api/Services/InvoiceService.cs:212 · Cambio: InvoiceService.cs · Pruebas: 1 nueva (Rojo → verde) + 14 en la suite
Verificado: build sin avisos nuevos · pruebas 312/312 · lint N/A
Siguiente: /qa-review 41020 en una sesión nueva (lee fix-plan.md como diseño) · después /document-code 41020
git add Api/Services/InvoiceService.cs MiProyecto.Tests/Services/InvoiceServiceTests.cs docs/sdd/41020-el-total-de-la-factura-redondea-mal-los/
:::

### Ejemplo: un bug que no pasa

:::out
⛔ No es una corrección rápida — 41077: Datos · la causa está en la configuración de la entidad
   Invoice (Api/Data/Configurations/InvoiceConfiguration.cs:31: precisión decimal(18,2)) y
   corregirla exige una migración.
Siguiente: /enrich-us 41077 (flujo completo). Lo encontrado está en bitacora.md.
:::

:::tip No fuerces la compuerta
Que un bug no pase no es un fallo: es la vía rápida haciendo su trabajo. La causa ya encontrada
queda en la bitácora y `enrich-us` la aprovecha.
:::

## enrich-us en modo qa · clasificar los criterios

El modo QA es `enrich-us` con un paso más (ADR-0025): **cada criterio de aceptación se clasifica**
según lo seguro que es, con su fuente. Lo usa QA cuando prepara el work item o antes de
`/test-cases`.

:::ask
/enrich-us 40933 qa
:::

| Clasificación | Cuándo | Qué necesita |
| --- | --- | --- |
| **Definido** | `story.md` lo dice: la acción, los datos y el resultado esperado | La cita |
| **Deducción directa** | Se sigue sin elección posible de `story.md`, un adjunto o el código actual (una validación que ya existe, un patrón de la misma pantalla) | La fuente: `story.md` §, `assets/…` o `archivo:línea` |
| **A confirmar** | Todo lo demás: un límite, un mensaje, un rol, un caso que `story.md` no decide | Una pregunta concreta para el PO; además es un `[PENDING-BUSINESS]` |

Un criterio nunca pasa a *Definido* porque «suene razonable». La clasificación va en la sección
*Clasificación de QA* (`<!-- sdd:qa-classification -->`) de `pbi.md`/`bug.md`, y la confirmación
muestra el recuento: `Clasificación QA: 3 Definido · 1 Deducción directa · 2 A confirmar`.

:::view Sección «Clasificación de QA» resultante en pbi.md
| Criterio | Clasificación | Fuente | Pregunta para el PO |
| --- | --- | --- | --- |
| CA-01 | Definido | story.md §Criterios: «El delegado ve solo sus clientes» | — |
| CA-02 | Deducción directa | Api/Services/ClientService.cs:88 (filtro por delegación) | — |
| CA-03 | A confirmar | — | ¿Qué ve el delegado si no tiene clientes asignados? |
:::

## test-cases · casos de prueba y CSV

:::card
<dl class="kv">
<dt>Paso</dt><dd>QA, después de <code>enrich-us</code> (idealmente en modo <code>qa</code>); puede ir en paralelo a la implementación</dd>
<dt>Quién</dt><dd>QA</dd>
<dt>Comando</dt><dd><code>/test-cases &lt;id&gt;</code></dd>
<dt>Lee</dt><dd><code>pbi.md</code>/<code>bug.md</code> (criterios, clasificación, roles, campos, i18n), SPECs de <code>04</code> si existe, <code>fix-plan.md</code></dd>
<dt>Escribe</dt><dd><code>test-cases.md</code>, <code>test-cases.csv</code>, <code>bitacora.md</code>, los <code>[PENDING-BUSINESS]</code> de <code>pbi.md</code></dd>
<dt>Script</dt><dd><code>test_cases_csv.py</code></dd>
<dt>Modelo</dt><dd>Sonnet (fijado en Claude Code)</dd>
</dl>
:::

### Tipos de caso

| Tipo | Qué prueba |
| --- | --- |
| **Funcional** | El criterio tal como está escrito, con sus datos |
| **Negativo** | Cada validación y cada error que nombran el criterio o las reglas (vacío, fuera de rango, formato, no permitido), con el mensaje o código esperado |
| **Borde** | Los límites que da el work item (fechas, importes, longitudes, cantidades), a cada lado |
| **Permisos** | Un caso por rol que puede y otro por rol que no, cuando el work item nombra roles |
| **Idioma** | Un caso por idioma del proyecto, cuando el criterio muestra textos |
| **Regresión** | (bugs) Los pasos reportados con el resultado esperado, y el comportamiento vecino que no debe romperse |

Reglas que la skill no se salta:

- Los datos y los resultados esperados salen de `pbi.md`/`bug.md`. Un valor que no dan → el caso
  lleva `[PENDING-BUSINESS: <pregunta>]` y queda **Bloqueado**. Nunca inventa límites, mensajes ni
  catálogos.
- Un criterio *A confirmar* deja **todos sus casos Bloqueados** hasta que se confirme.
- Un caso prueba una sola cosa; los pasos son acciones de una persona con un resultado observable.
- Dice si es automatizable y a qué nivel (unitaria, integración, e2e), o por qué no. Con `04`,
  marca qué casos ya cubre una SPEC automatizada.

### Ejemplo

:::ask
/test-cases 40399
:::

:::out Confirmación
## Casos de prueba — 40399 Sección de ofertas en el menú lateral
Criterios: 2 (1 Definido · 0 Deducción directa · 1 A confirmar · 0 sin clasificar)
Casos: 3 · Funcional 2 · Negativo 0 · Borde 0 · Permisos 1 · Idioma 0 · Regresión 0
Bloqueados: 1 — TC-03: ¿orden ascendente o descendente? · Ya automatizados (SPECs): 1
¿Empiezo?
:::

:::file test-cases.md (un caso)
### TC-02 · No ver la sección Ofertas como consultor

- **Criterio:** CA-01 · **Tipo:** Permisos · **Prioridad:** Alta · **Estado:** Diseñado
- **Rol:** Consultor · **Idioma:** es
- **Precondiciones:** usuario con rol Consultor
- **Datos:** —
- **Automatizable:** Sí (integración)

| # | Acción | Resultado esperado |
| --- | --- | --- |
| 1 | Iniciar sesión como consultor y abrir el menú lateral | No aparece «Ofertas» |
:::

El CSV lo genera el script (salida real):

:::cmd
python .agents/skills/test-cases/scripts/test_cases_csv.py docs/sdd/40399-…/test-cases.md --area "MiProyecto\Comercial"
:::

:::out
✓ 2 casos y 3 pasos en docs/sdd/40399-seccion-de-ofertas-en-el-menu-lateral/test-cases.csv
:::

:::file test-cases.csv
ID,Work Item Type,Title,Test Step,Step Action,Step Expected,Area Path,State
,Test Case,TC-01 · Ver la sección Ofertas como comercial,,,,MiProyecto\Comercial,Design
,,,1,Iniciar sesión como comercial,Se muestra el panel principal,,
,,,2,Abrir el menú lateral,Aparece «Ofertas» debajo de «Clientes»,,
,Test Case,TC-02 · No ver la sección Ofertas como consultor,,,,MiProyecto\Comercial,Design
,,,1,Iniciar sesión como consultor y abrir el menú lateral,No aparece «Ofertas»,,
:::

El caso bloqueado (TC-03) no está en el CSV. Para incluirlo, `--include-blocked`. El archivo va en
UTF-8 con BOM para que Excel y Azure DevOps lean bien las tildes. El CSV **no se versiona**
(ADR-0027): lo que va al repositorio es `test-cases.md`, y el script vuelve a generar el CSV cuando
haga falta.

### Importarlo en Azure Test Plans

1. Revisa `test-cases.md` (QA es quien lo aprueba).
2. En Azure DevOps: **Test Plans → tu plan → suite → Test cases → Import** (o *Import test cases
   from CSV*), elige `test-cases.csv` y revisa la vista previa.
3. Si el PO responde una pregunta, vuelve a lanzar `/test-cases <id>`: actualiza el archivo
   conservando los IDs y los casos ya revisados, y desbloquea los que correspondan.

:::note Relación con qa-review
Si existe `test-cases.md`, `qa-review` comprueba que cada caso de **prioridad Alta** tiene una
prueba automatizada o una comprobación en ejecución.
:::
