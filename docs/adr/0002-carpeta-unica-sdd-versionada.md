# ADR-0002 · Azure DevOps es la fuente del requisito; todo el trabajo SDD vive en una carpeta versionada

- **Estado:** Aceptada · sustituida en parte por ADR-0027 (qué archivos de la carpeta se versionan)
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0007

## Contexto

El flujo SDD v2.3 guardaba los artefactos en `docs/<sprint>/<item>/`. Otra propuesta
(`sdd-clavijo`) dejaba Azure DevOps como única fuente y guardaba notas locales sin versionar,
donde llegaron a quedar decisiones de negocio confirmadas por el PO. Tener dos sitios para el
trabajo SDD es confuso y hace perder información.

## Decisión

- El work item vive siempre en Azure DevOps, que es la fuente del requisito.
- Todo lo que el flujo genera o usa para un work item vive en **una sola carpeta**,
  `docs/sdd/<id>-<título-corto>/`, y **se versiona entero**:

```text
docs/sdd/40399-seccion-ofertas/
├── story.md            ← paso 0: el work item copiado por la persona (la IA no lo edita)
├── bitacora.md         ← notas de trabajo con fecha
├── pbi.md | bug.md     ← paso 1
├── 00 … 06-*.md        ← paso 2 (03 y 04 = contrato aprobado)
├── CHANGELOG.md        ← paso 3, una entrada por tarea
├── qa-report.md        ← paso 4
├── commit-message.md   ← paso 5, según .gitmessage
└── assets/             ← imágenes y archivos del work item y capturas que hagan falta
```

- La carpeta se nombra por el ID del work item, no por el sprint, porque el ID no cambia.

Cinco reglas:

1. `story.md` no es una segunda fuente de verdad: es el work item tal como lo copió una persona,
   con su ID, revisión y fecha, y la IA nunca lo edita (ADR-0015). Si el requisito cambia, la
   persona lo actualiza; git conserva la versión anterior y la bitácora anota el motivo.
2. La bitácora es la historia y `pbi.md` es el contrato: toda decisión confirmada pasa de
   `bitacora.md` a `pbi.md` (y como comentario al work item).
3. Lo temporal no se escribe en disco (por ejemplo, los mapas de código de `code-explorer`).
4. Nada sensible: ni credenciales ni datos personales de clientes, en texto o capturas.
5. Cada skill lee solo la carpeta de su work item; los ítems anteriores, con búsquedas puntuales.

## Consecuencias

- Seguimiento y retroalimentación completos: bitácoras e informes de QA analizables.
- El diseño se revisa junto al código en el mismo PR y el pipeline puede comprobarlo.
- Los PR llevan más archivos Markdown.
- Los skills v2.3 deben migrar a la ruta nueva y aceptar las rutas antiguas.

## Alternativas consideradas

- Versionar solo contrato y evidencia y dejar notas en `.sdd/` local: dos sitios, se pierden decisiones.
- Solo Azure DevOps: el diseño no se revisa con el código y el KPI no se mide automáticamente.
