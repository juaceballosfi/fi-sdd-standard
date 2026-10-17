# Decisiones del estándar (ADR)

:::lead
Cada regla del kit tiene detrás una decisión registrada en `docs/adr/` del repositorio del kit. Si
te preguntas por qué algo funciona así, el ADR lo explica: contexto, decisión, consecuencias y
alternativas descartadas.
:::

## Índice de ADR

| ADR | Decisión | Estado |
| --- | --- | --- |
| 0001 | Registrar las decisiones con ADR | Aceptada |
| 0002 | Azure DevOps es la fuente del requisito; todo el trabajo SDD en `docs/sdd/<id>-<título>/`, versionado | Sustituida en parte por 0027 |
| 0003 | Español para documentación, comentarios y commits; inglés para instrucciones internas | Aceptada |
| 0004 | Formato de commit: `.gitmessage` de Bonis | Aceptada |
| 0005 | Herramientas soportadas y rutas de cada una | Aceptada |
| 0006 | Ramas y despliegue | Aceptada |
| 0007 | `story.md` con el texto pegado es la entrada de `enrich-us` | Sustituida por 0015 |
| 0008 | MCP de Azure DevOps en solo lectura, tras una prueba | Propuesta |
| 0009 | IA dentro del pipeline con Fi Apps | Aceptada |
| 0010 | Responsable y pilotos | Aceptada |
| 0011 | Fuente única y adaptadores generados, sin enlaces simbólicos | Aceptada |
| 0012 | Reglas obligatorias en pruebas y pipeline | Aceptada |
| 0013 | Subagentes y skills de la sesión principal | Aceptada |
| 0014 | Reglas de optimización de tokens | Aceptada |
| 0015 | `story.md` lo prepara la persona, con sus adjuntos en `assets/` | Aceptada |
| 0016 | Ajustes del flujo tras el primer piloto en Bonis | Aceptada |
| 0017 | Adaptadores de agentes: `.github/agents/` versionado y `.claude/agents/` local | Aceptada |
| 0018 | `wbs-execution` delega cada tarea en el agente de su capa, con bucles limitados | Aceptada |
| 0019 | Revisión de QA independiente antes del PR, con `qa-review` | Aceptada |
| 0020 | Documentación del código con `document-code`, solo comentarios y `docs/` | Aceptada |
| 0021 | `/project-context`: contexto del proyecto, documentación base y pruebas desde el inicio | Aceptada |
| 0022 | `/document-project`: documentación inicial y completa del proyecto | Aceptada |
| 0023 | Guardarraíles: permisos `deny`, hook `sdd_guard.py`, pruebas de arquitectura y `pr-check.py`, con la matriz regla → comprobación | Aceptada |
| 0024 | Vía rápida para bugs pequeños con `quick-fix` y su compuerta | Aceptada |
| 0025 | Modo QA de `enrich-us` y skill `test-cases`, con CSV para Azure Test Plans | Aceptada |
| 0026 | El bucle de pipeline en rojo pasa a la fase 4 | Aceptada |
| 0027 | Qué se versiona en un proyecto con el kit: fuera `assets/`, `commit-message.md`, `test-cases.csv` y los borradores | Aceptada |
| 0028 | `/project-context` deja el kit a punto y no arregla el proyecto; compuerta del entorno; borradores con prioridad | Aceptada |

## Las que más afectan al día a día

| ADR | Qué significa para ti |
| --- | --- |
| 0002 | Todo el trabajo de un work item vive en `docs/sdd/<id>-<título>/`; qué se versiona, en 0027 |
| 0003 | Documentos, comentarios y commits en español |
| 0004 | Un commit por work item, `Ref: #id`, nunca `fix #id`, sin firma de IA |
| 0006 | Rama `feature/<id>-…` o `fix/<id>-…` desde `dev`, PR a `dev` con squash |
| 0013 | Las skills que piden confirmación corren en tu sesión; el trabajo acotado, en subagentes |
| 0015 | `story.md` lo preparas tú, con los adjuntos en `assets/` |
| 0018 | `wbs-execution` delega cada tarea en el subagente de su capa, con bucles limitados |
| 0019 | `qa-review` siempre en una sesión independiente, antes del PR |
| 0021 | `/project-context` antes del primer work item: contexto, `docs/` y pruebas |
| 0023 | Guardarraíles: cada regla obligatoria con su comprobación |
| 0024 | Vía rápida para bugs pequeños con su compuerta |
| 0025 | Modo QA de `enrich-us` y `test-cases` con CSV para Test Plans |
| 0027 | Qué se versiona: fuera `assets/`, `commit-message.md`, `test-cases.csv` y los borradores |
| 0028 | Lo que una skill encuentra fuera de su alcance es un borrador con prioridad (Urgente, Alta, Media, Baja); los urgentes se crean ya |

## Proponer un cambio al kit

1. Rama desde `main` en el repositorio del kit; un cambio por rama.
2. Si cambia una regla o un comportamiento, un ADR nuevo (o uno que sustituya a otro).
3. Los cambios se hacen en `core/`, nunca en las copias instaladas.
4. `python scripts/validate.py` sin errores y una entrada en `CHANGELOG.md`.
5. Commit según `.gitmessage`.
