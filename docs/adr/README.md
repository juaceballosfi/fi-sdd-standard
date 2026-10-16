# Decisiones de arquitectura (ADR)

Cada decisión que cambia el comportamiento del kit se registra aquí (ADR-0001). Para una nueva,
copia `0000-plantilla.md` con el siguiente número y añádela a este índice en el mismo PR.

| ADR | Decisión | Estado |
| --- | --- | --- |
| [0001](0001-registrar-decisiones-con-adr.md) | Registrar las decisiones con ADR | Aceptada |
| [0002](0002-carpeta-unica-sdd-versionada.md) | Azure DevOps es la fuente del requisito; todo el trabajo SDD en `docs/sdd/<id>-<título>/`, versionado | Sustituida en parte por 0027 |
| [0003](0003-idioma.md) | Español para documentación, comentarios y commits; inglés para instrucciones internas | Aceptada |
| [0004](0004-formato-de-commit.md) | Formato de commit: `.gitmessage` de Bonis | Aceptada |
| [0005](0005-herramientas-y-adaptadores.md) | Herramientas soportadas y rutas de cada una | Aceptada |
| [0006](0006-ramas-y-despliegue.md) | Ramas y despliegue | Aceptada |
| [0007](0007-story-md-entrada-de-enrich-us.md) | `story.md` con el texto pegado es la entrada de `enrich-us` | Sustituida por 0015 |
| [0008](0008-mcp-de-azure-devops.md) | MCP de Azure DevOps en solo lectura, tras una prueba | Propuesta |
| [0009](0009-ia-en-el-pipeline-con-fi-apps.md) | IA dentro del pipeline con Fi Apps | Aceptada |
| [0010](0010-responsable-y-pilotos.md) | Responsable y pilotos | Aceptada |
| [0011](0011-fuente-unica-y-adaptadores.md) | Fuente única y adaptadores generados, sin enlaces simbólicos | Aceptada |
| [0012](0012-reglas-obligatorias-en-pruebas-y-pipeline.md) | Reglas obligatorias en pruebas y pipeline | Aceptada |
| [0013](0013-subagentes.md) | Subagentes y skills de la sesión principal | Aceptada |
| [0014](0014-optimizacion-de-tokens.md) | Reglas de optimización de tokens | Aceptada |
| [0015](0015-story-md-lo-prepara-la-persona.md) | `story.md` lo prepara la persona, con sus adjuntos en `assets/` | Aceptada |
| [0016](0016-ajustes-tras-el-piloto-de-bonis.md) | Ajustes del flujo tras el primer piloto en Bonis | Aceptada |
| [0017](0017-adaptadores-de-agentes.md) | Adaptadores de agentes: `.github/agents/` versionado y `.claude/agents/` local | Aceptada |
| [0018](0018-implementacion-delegada-y-bucles.md) | `wbs-execution` delega cada tarea en el agente de su capa, con bucles limitados | Aceptada |
| [0019](0019-revision-de-qa-independiente.md) | Revisión de QA independiente antes del PR, con `qa-review` | Aceptada |
| [0020](0020-documentacion-del-codigo.md) | Documentación del código con `document-code`, solo comentarios y `docs/` | Aceptada |
| [0021](0021-contexto-del-proyecto.md) | `/project-context`: contexto del proyecto, documentación base y pruebas desde el inicio | Aceptada |
| [0022](0022-documentacion-inicial-del-proyecto.md) | `/document-project`: documentación inicial y completa del proyecto | Aceptada |
| [0023](0023-guardarrailes.md) | Guardarraíles: permisos `deny`, hook `sdd_guard.py`, pruebas de arquitectura y `pr-check.py`, con la matriz regla → comprobación | Aceptada |
| [0024](0024-via-rapida-para-bugs.md) | Vía rápida para bugs pequeños con `quick-fix` y su compuerta | Aceptada |
| [0025](0025-qa-modo-y-casos-de-prueba.md) | Modo QA de `enrich-us` y skill `test-cases`, con CSV para Azure Test Plans | Aceptada |
| [0026](0026-bucle-de-pipeline-en-la-fase-4.md) | El bucle de pipeline en rojo pasa a la fase 4 | Aceptada |
| [0027](0027-que-se-versiona.md) | Qué se versiona en un proyecto con el kit: fuera `assets/`, `commit-message.md`, `test-cases.csv` y los borradores | Aceptada |
