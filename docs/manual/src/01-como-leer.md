# Cómo usar este manual

:::lead
Este manual explica de principio a fin cómo se trabaja con **fi-sdd-standard**: qué es cada pieza,
cuándo se usa, qué le pides a la IA, qué te devuelve y qué haces tú en cada momento. Al terminarlo
deberías poder instalar el kit en un proyecto, llevar un work item de Azure DevOps hasta el PR y
saber qué hacer cuando algo se para.
:::

## Qué encontrarás

El manual va de lo general a lo concreto. Los primeros capítulos dan el mapa; los del centro son la
referencia de cada pieza, y los últimos son recetas y soluciones para el día a día.

| Parte | Capítulos | Para qué |
| --- | --- | --- |
| El mapa | 2 · Conceptos · 3 · El flujo · 4 · Herramientas | Entender qué es el kit, cómo se encadenan los pasos y dónde vive cada cosa |
| Empezar | 5 · Instalación | Instalar el kit en un proyecto existente o nuevo, y actualizarlo |
| Referencia | 6 a 13 | Cada skill, subagente, prompt, plantilla, script, guardarraíl y marcador, en detalle |
| Trabajo diario | 14 · Git y PR · 15 · Recetas · 16 · Cómo pedir | Casos completos, de principio a fin, y cómo hablarle a la IA |
| Cuando algo falla | 17 · Problemas · 18 · Referencia rápida | Errores frecuentes y una hoja de consulta |

## Por dónde empezar según tu rol

:::grid3
:::tile-accent Desarrollo
1. Capítulos 2 y 3: el flujo completo.
2. Capítulo 6: las skills del flujo, sobre todo `enrich-us`, `technical-analysis` y `wbs-execution`.
3. Capítulo 7: `quick-fix` para bugs pequeños.
4. Capítulos 14 y 15: el commit, el PR y las recetas.
:::
:::tile-accent QA
1. Capítulos 2 y 3: el flujo y dónde entra QA.
2. Capítulo 7: el modo `qa` de `enrich-us` y `test-cases`.
3. Capítulo 6: `qa-review`, la revisión independiente antes del PR.
4. Capítulo 15: las recetas de QA.
:::
:::tile-accent Tech lead
1. Capítulo 5: instalación y actualización.
2. Capítulo 8: `project-context` y `document-project`.
3. Capítulo 12: los guardarraíles y `sdd-guardrails.json`.
4. Capítulo 14: llevar el piloto a `dev`.
:::
:::

## Convenciones de este manual

Los ejemplos usan un proyecto ficticio con el work item **#40399 «Sección de ofertas en el menú
lateral»** y el bug **#41020 «El total de la factura redondea mal los céntimos»**. Las salidas de
scripts son reales: se generaron con el kit v0.12.0. Las respuestas de la IA son representativas:
siguen el formato exacto que fija cada skill, pero el texto varía de una sesión a otra.

:::ask Lo que pides
Así se ve un mensaje que tú escribes en el chat de la herramienta.
:::

:::out Lo que responde
Así se ve lo que la IA o un script te devuelve.
:::

:::cmd Comando
python .agents/scripts/pr-check.py    # así, un comando que ejecutas en la terminal
:::

:::note Nota
Información que conviene saber.
:::

:::tip Consejo
Una forma mejor de hacer algo.
:::

:::warn Atención
Algo que, si se ignora, cuesta tiempo o rehacer trabajo.
:::

:::danger Nunca
Algo que rompe una regla del equipo.
:::

Otras convenciones:

- `<id>` es el ID del work item en Azure DevOps (por ejemplo `40399`) y `<carpeta>` es su carpeta,
  `docs/sdd/<id>-<título>/`.
- `<kit>` es la ruta donde tienes el kit descargado (por ejemplo `C:\Users\tu-usuario\Documents\fi-sdd-standard`).
- Los comandos van en PowerShell (Windows) salvo que se diga otra cosa. En macOS o Linux cambia `\`
  por `/`.
- Los nombres de archivos, identificadores (`CA-01`, `SPEC-01`, `T-01`, `QA-01`) y marcadores se
  escriben siempre igual: las skills los buscan por su nombre exacto.

## Qué no es este manual

No sustituye a los archivos del kit. Las instrucciones exactas que sigue la IA están en cada
`SKILL.md`, y las decisiones del estándar en los ADR de `docs/adr/` del kit. Si algo de este manual
contradice un `SKILL.md`, manda el `SKILL.md`, y conviene avisar al responsable del kit para
corregir el manual.

El manual vive en `docs/manual/` del repositorio del kit, en PDF y en Markdown (este último, pensado
para dárselo de contexto a una IA). No se copia a los proyectos al instalar el kit.
