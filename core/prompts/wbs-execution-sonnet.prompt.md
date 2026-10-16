---
agent: agent
description: 'Paso 3 del flujo SDD con el modelo fijado en Sonnet: implementa tarea por tarea el WBS aprobado de un work item'
model: Claude Sonnet 5 (copilot)
tools: ['search', 'read', 'edit', 'execute', 'todo']
---

# Ejecución WBS con Sonnet — work item ${input:item:ID del work item (ej: 40399)}

**Work item:** ${input:item}

Ejecuta la skill `wbs-execution` para este work item, siguiendo **exactamente** las instrucciones de
[wbs-execution/SKILL.md](../skills/wbs-execution/SKILL.md). Toma el ID de este prompt, no del
placeholder de argumentos de la skill. Las plantillas que cita están en
[wbs-execution/templates/](../skills/wbs-execution/templates/changelog.md).

Este prompt solo fija el modelo (Sonnet, para ciclos rápidos de implementación y verificación) y
las herramientas. Todas las reglas del flujo viven en el `SKILL.md`: si cambias el proceso, cámbialo
allí, no aquí.
