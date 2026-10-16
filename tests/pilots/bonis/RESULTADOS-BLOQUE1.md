# Resultados del bloque 1 de la fase 2 · `code-explorer` · PBI 40933

**Fecha:** 2026-10-14 · **Kit:** v0.5.1 (skills v3.3) · **Quién:** Juan Ceballos
**Work item:** 40933 — [RSP] Correcciones rol delegado. Son tres cambios: la selección en
«Investigadores», el campo Delegado en «Agregar proyecto» y las columnas del Excel del seguimiento
mensual.

## Resumen

`code-explorer` funciona en las dos herramientas y los skills le delegan la exploración. El diseño
es de mejor calidad que el del 40944. El contexto de `technical-analysis` bajó de 551k a 202k
tokens (un 63 % menos), pero no llegó al objetivo de 150k: esos 202k incluyen dos rondas extra de
validaciones y aprobaciones. El bloque 1 se da por cerrado con los ajustes de la v0.5.2.

## Tabla de resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos | ✓ | |
| 2 | `code-explorer` visible en Claude Code | ✓ | Comprobado preguntando en una sesión nueva (ya no existe `/agents`) |
| 3 | `code-explorer` usable como subagente en VS Code | ✓ | Copilot lo listó y lo usó |
| 4 | Duplicados en VS Code | ✓ Ninguno | En la lista de subagentes aparece una sola vez. Falta mirar el selector de agentes |
| 5 | Prueba directa con el formato esperado | ✓ | En Claude Code faltó «Pruebas existentes»; corregido en la v0.5.1 |
| 6 | `enrich-us` delega la exploración | ✓ | Tres preguntas en paralelo, una por cambio |
| 7 | `technical-analysis` delega la exploración | ✓ | Tres preguntas en paralelo; la sesión principal verificó después varias líneas |
| 8 | Contexto de `enrich-us` | 105k | 40944: 107k, con un PBI más sencillo. `/context` indica 71,6k en lecturas de archivos en la sesión principal |
| 9 | Contexto de `technical-analysis` | 202k | 40944: 551k. Incluye cerrar 5 `[REQUIRES-VALIDATION]` (con Context7) y las aprobaciones |
| 10 | Calidad del diseño 00–06 | ✓ Alta | Ver «Lo que funcionó» |

**Tiempo:** `enrich-us` tardó unos 20 minutos y `technical-analysis` unos 75, incluidas las
decisiones.

## Lo que funcionó

- La exploración en paralelo dio a cada cambio su causa con archivo y línea:
  - `rowSelection` sin condición de rol.
  - `Form.Item name` que pisa el valor mostrado.
  - Un `isManager` que deja fuera a ManagerMaster.
- Las preguntas fueron de negocio y concretas:
  - Solo delegados, o todos los que no son Consultant.
  - Si también aplica al export «Todos».
  - Qué pasa con las columnas no listadas.
  - «Fecha recuperación» en Horas y Ausencias.
- Riesgos que una lectura rápida no habría visto:
  - `StyleHeaderRow` desplazado al quitar la última columna.
  - El proyecto se crearía sin delegado si se quita `name`.
  - La firma de los jobs de Hangfire.
  - Que no hay pruebas de las columnas del Excel, por lo que primero se fija el comportamiento
    actual con pruebas.
- Los `[REQUIRES-VALIDATION]` se cerraron con evidencia (documentación de AntD con Context7,
  patrones del repositorio, código del backend), no por suposición.
- El bloque «Comentario para Azure DevOps» salió al final de cada paso.
- El WBS separa las capas: T-01 backend, T-02 y T-03 frontend, que se pueden hacer en paralelo.
  Encaja con el bloque 2.

## Lo que hay que mejorar (v0.5.2, skills v3.4)

1. **La sesión principal vuelve a verificar lo que devuelve `code-explorer`.** Lee rangos de
   código después de cada informe, y por eso salen 71,6k en lecturas de archivos en `enrich-us`.
   Ahora `technical-analysis` solo verifica las líneas que serán causa raíz o contrato en 03/04, y
   como mucho unas 20 líneas por comprobación.
2. **Marcadores resueltos que siguen en `pbi.md`.** `technical-analysis` cerró en 01 dos
   `[REQUIRES-VALIDATION]` de `pbi.md`, pero los dejó en `pbi.md`. La nueva convención compartida
   *Resolved markers* obliga a quitarlos en todos los archivos de la carpeta. El comprobador avisa
   de los `[REQUIRES-VALIDATION]` abiertos en `pbi.md`/`bug.md` y en 00–06.
3. **Ediciones con scripts de Python sobre heredocs de bash en Windows.** Funcionan, pero fallaron
   una vez (`SyntaxWarning` por `\S`) y la IA pasó a escribir scripts en su scratchpad. Se sigue
   observando: es una decisión de la herramienta, no del skill.

## Para el desarrollador

- En `pbi.md` quedan dos `[REQUIRES-VALIDATION]` ya resueltos, en las «Notas de implementación».
  Los quitará `wbs-execution` con la regla nueva, o se pueden quitar a mano.
- `story.md` dice «revisión 4»; el *History* mostraba 3 cambios.
- Pegar en el work item 40933 los dos comentarios para Azure DevOps.
