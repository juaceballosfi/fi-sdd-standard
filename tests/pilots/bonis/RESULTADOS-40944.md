# Resultados del piloto en Bonis · PBI 40944

**Fecha:** 2026-10-14 · **Kit:** v0.3.0 (skills v3.1) · **Herramienta:** Claude Code (Opus 5.5)
**Quién:** Juan Ceballos · **Work item:** 40944 — [RSP] Ubicación seguimiento del servicio
**Revisado por:** fi-sdd-standard v0.4.0, a partir de la carpeta del ítem y de los registros de las
tres sesiones

## Resumen

El flujo funcionó de principio a fin y terminó con código probado y un mensaje de commit válido.
El PBI pedía mover una entrada del menú. Durante el análisis técnico, por decisión del
desarrollador con aprobación del PO, creció a 6 SP:

- Unificar el menú lateral y el del dashboard.
- Corregir un bug: RRHH con permiso no veía su tarjeta en el dashboard.
- Extraer un hook de permisos.

`tenant-layout.tsx` pasó de 1701 a 587 líneas. Se encontró además un problema que afecta a todo
el frontend: el build no comprueba tipos. Quedó como propuesta de work item aparte.

## Tabla de resultados

| # | Comprobación | Claude Code | Notas |
| --- | --- | --- | --- |
| 1 | Instalación o actualización sin conflictos | ✓ | 32 actualizados, «Todo en orden» |
| 2 | Skills visibles | ✓ | Copilot no se probó |
| 3 | `story.md` preparado y comprobador sin errores | ✓ | Tras quitar la tilde de la carpeta y rellenar revisión y fecha |
| 4 | `enrich-us` abrió la imagen | ✓ | La describió bien en el resumen de confirmación |
| 5 | `story.md` sin cambios después de `enrich-us` | ✓ | Según el informe; confirmar con `git diff` |
| 6 | Criterios propuestos solo desde la descripción, marcados para validar | ✓ | CA-01, CA-02 y CA-05; el PO los aprobó |
| 7 | Bitácora con preguntas, respuestas y decisiones | ✓ | 10 decisiones; ver mejoras 3 y 4 |
| 8 | `pbi.md` correcto y sin decisiones perdidas | ✓ | Actualizado por `technical-analysis` con la ampliación |
| 9 | Diseño 00–06 coherente con Bonis | ✓ | Comparó entrada a entrada las dos listas antes de unificarlas |
| 10 | Pruebas primero y build/test en verde | ✓ | 15 pruebas nuevas, 9 en rojo al principio; 19/19 al final |
| 11 | Traducciones | N/A | Correcto: no hay textos nuevos |
| 12 | `commit-message.md` válido | ✓ | 0 errores, 2365 caracteres |
| 13 | Contexto por paso | ⚠ | `enrich-us` 107k · `technical-analysis` **551k** · `wbs-execution` 175k |
| 14 | Tiempo total | — | Unas 3 h 15 min, incluida la verificación manual por rol (preparación 15 min · enriquecimiento 25 min · análisis 55 min · ejecución 1 h 30 min) |

## Lo que funcionó

- **Entrada preparada por la persona (ADR-0015).** `enrich-us` leyó la imagen, detectó los huecos
  (sin criterios, origen en #40942) y propuso criterios marcados para validar, sin inventarlos.
- **Preguntas útiles.** El alcance por roles y el dashboard eran ambigüedades reales y no se
  supusieron.
- **Investigación con evidencia.** `technical-analysis` encontró el bug de `dashboard.tsx` y el
  build que no comprueba tipos. Pidió el log de CI en vez de suponer.
- **Verificación honrada.** `wbs-execution` dejó T-04 «En curso» hasta que la verificación manual
  por rol estuvo confirmada. Avisó de la rama del piloto y no hizo commit.
- **Comprobador.** Marcó la tilde de la carpeta y los campos sin rellenar antes de empezar.

## Lo que hay que mejorar (corregido en v0.4.0, skills v3.2)

1. **Contexto de `technical-analysis` (551k).** Sobre todo por el log de CI pegado en el chat
   (unas 4000 líneas) y por leer enteros archivos de 1700 líneas. Nuevas reglas:
   - Los logs se piden como archivo y se buscan; no se pegan.
   - En archivos grandes se leen solo los rangos necesarios.
   - El subagente `code-explorer` (fase 2) es el siguiente paso.
2. **Ampliación de alcance.** Un cambio de orden pasó a ser una refactorización de 6 SP dentro
   del mismo PBI. Ahora `technical-analysis` explica lo que añade y pregunta si va en este work
   item o en otro. Si entra, actualiza `pbi.md` con la línea «Actualizado con» y deja constancia
   de quién lo aprobó.
3. **Decisiones fuera de Azure DevOps.** El work item sigue diciendo solo «ponerlo encima del
   manual». Ahora cada paso que confirma decisiones termina con un bloque «Comentario para Azure
   DevOps» listo para pegar.
4. **Bitácora.** `wbs-execution` abrió una sección nueva en *Hallazgos* (luego la corrigió). Un
   hallazgo quedó contradicho («la comprobación fiable es `yarn build`») sin corregir. Ahora la
   regla dice dónde va cada cosa y cómo corregir un hallazgo.
5. **Borradores de work items.** La IA creó `docs/sdd/_borradores/` por su cuenta, con buen
   criterio. Ahora es la convención.
6. **Comprobador.** Dos falsos positivos:
   - Contaba «Secciones [ASSUMPTION-BASED]: Ninguna» como marcador sin resolver.
   - Daba «5/4 tareas» porque contaba la leyenda de estados.

   Además, sugiere el nombre correcto de la carpeta.
7. **`new-sdd-item.py` con carpeta existente.** Ahora crea solo lo que falta (por ejemplo
   `bitacora.md`) sin tocar `story.md`.

8. **Codificación.** En la PR, Azure Repos mostró `useDashboard.ts` como «utf-8 -> Windows-1252».
   El archivo era UTF-8 válido. Lo más probable es que la IA quitara el BOM al reescribirlo con un
   script. Desde la v0.4.2, `scripts/check-encoding.py` comprueba la codificación y el BOM, y
   `AGENTS.base.md` tiene una regla para conservarlos.

## Pendiente de decidir

- **Firma de IA en el commit:** decidido el 2026-10-14. No se firma; basta con el sello «Generado
  con» (ADR-0004).
- **Granularidad:** decidido el 2026-10-14. Un commit por work item (ADR-0004).
- **Prueba con Copilot.** Falta repetir los pasos con GitHub Copilot en VS Code.

## Acciones para el desarrollador

- Publicar en el work item 40944 el comentario con las decisiones y la ampliación de alcance.
- Crear en Azure DevOps el work item de la comprobación de tipos, desde
  `docs/sdd/_borradores/comprobacion-tipos-frontend.md`.
- Añadir al «Project context» del `AGENTS.md` de Bonis lo aprendido:
  - Las pruebas de frontend van en `src/tests/pages/...` y no hay `@testing-library`.
  - `yarn build` no comprueba tipos. Hasta que se corrija, hay que usar la comprobación con
    tsconfig temporal de `04-implementation-plan.md` §4.7.
- Llevar el trabajo a `feature/40944-…` desde `dev` antes de la PR. En la PR, mencionar los dos
  cambios visibles: «My Projects» en el dashboard y la tarjeta de RRHH.
