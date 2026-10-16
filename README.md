# fi-sdd-standard

Kit del equipo para trabajar con IA siguiendo un mismo flujo SDD (*Spec-Driven Development*): de un
work item de Azure DevOps a código probado, documentado y desplegado, igual en GitHub Copilot
(VS Code y Visual Studio), Claude Code y Codex.

**Versión:** 0.11.0 (candidata a MVP) · **Estado:** en pruebas por olas (`tests/pilots/PLAN-PRUEBAS-MVP.md`) · **Responsable:** Juan Ceballos
**Pilotos:** Bonis y Calls4Grants

> El brief y el plan completo están en el documento «SDD Enterprise · Brief y plan de implantación».
> Las decisiones están en [`docs/adr/`](docs/adr/README.md).

## El flujo

```text
0 project-context (una vez por repositorio) → document-project (opcional, por bloques)
work item (Azure DevOps)
  → 1 enrich-us ─G1─▶ 2 technical-analysis ─G2─▶ 3 wbs-execution
  → 4 qa-review ─G3─▶ 5 document-code ─▶ 6 pr-check y PR a dev ─G4─▶ 7 despliegue (dev → main/Staging → prod)
bug pequeño: quick-fix (sustituye 1–3 si pasa su compuerta) → 4 → 5 → 6
QA: enrich-us <id> qa → test-cases (casos y CSV para Azure Test Plans)
```

G1 a G4 son aprobaciones humanas. Todo el trabajo de un work item queda en
`docs/sdd/<id>-<título>/` del proyecto, versionado (ADR-0002).

## Estructura

```text
fi-sdd-standard/
├── core/
│   ├── AGENTS.base.md      ← reglas comunes a todos los proyectos (inglés, ADR-0003)
│   ├── skills/             ← fuente única de los 9 skills (v3.8): project-context, document-project, enrich-us, technical-analysis, wbs-execution, qa-review, document-code, quick-fix y test-cases
│   ├── prompts/            ← atajos de Copilot que fijan el modelo
│   ├── agents/             ← 7 subagentes estables en formato neutral
│   ├── hooks/              ← sdd_guard.py: hook de Claude Code (ADR-0023)
│   └── templates/          ← .gitmessage, AGENTS.md por proyecto, sdd-guardrails.json y MCP
├── project-templates/docs/ ← plantilla de docs/ para cada proyecto
├── pipelines/              ← plantillas de Azure Pipelines (fase 4)
├── scripts/
│   ├── validate.py         ← valida skills, agentes, reglas comunes, versiones y ADR
│   ├── install.py          ← instala o actualiza el kit en un proyecto (versión mínima para pilotos)
│   ├── new-sdd-item.py     ← crea la carpeta de un work item para preparar story.md
│   ├── check-sdd-item.py   ← comprueba los artefactos de un work item y el mensaje de commit
│   ├── check-encoding.py   ← comprueba (y repara) que los archivos cambiados están en UTF-8
│   └── pr-check.py         ← reglas obligatorias de una rama antes del PR (ADR-0023)
├── tests/
│   ├── compat/             ← prueba de compatibilidad entre herramientas
│   └── pilots/             ← plan de pruebas del MVP, protocolos y resultados de Bonis
├── VERSION
└── docs/
    ├── adr/                ← decisiones del estándar
    └── guias/              ← guías rápidas (dev, QA), git de un work item, MCP y piloto a dev
```

## Instalar en un proyecto

```bash
python scripts/install.py --target <ruta-del-proyecto> --tools copilot,claude --dry-run
python scripts/install.py --target <ruta-del-proyecto> --tools copilot,claude
```

Después, en una sesión nueva: `/project-context`. Escribe la sección *Project context* de
`AGENTS.md` y los `docs/*.md` base con el contenido real del proyecto, y crea el proyecto de
pruebas si falta (ADR-0021). Opcionalmente, `/document-project` documenta todo el proyecto por
bloques, un PR por bloque, con un plan reanudable en `docs/sdd/_documentacion/` (ADR-0022).

También instala los guardarraíles (ADR-0023):
- `.agents/hooks/sdd_guard.py` y `.agents/scripts/` (`pr-check.py` y los comprobadores);
- `sdd-guardrails.json` en la raíz;
- en `.claude/settings.json`, los permisos `deny` y los hooks, sin pisar lo que ya tenga.

Nunca sobrescribe archivos del proyecto: solo crea lo que falta y actualiza lo que instaló el kit
(lista en `.sdd-kit.json`). `copilot` instala en `.agents/skills/` (se versiona); `claude` genera la
copia local de Claude Code en `.claude/skills/` (queda en `.gitignore`); `visualstudio` genera
`.github/copilot-instructions.md` desde `AGENTS.md`. Los agentes con `status: stable` se instalan en
`.github/agents/` (versionado) y en `.claude/agents/` (local), según las herramientas elegidas (ADR-0017).

## Empezar un work item

Desde la raíz del proyecto:

```bash
python <kit>/scripts/new-sdd-item.py <id> "<título del work item>"      # --tipo bug para un bug
```

Crea `docs/sdd/<id>-<título>/` con `story.md`, `bitacora.md` y `assets/`. Copia el work item de
Azure DevOps en `story.md` y guarda sus imágenes y archivos en `assets/` (ADR-0015); después,
`/enrich-us <id>` en una sesión nueva.

## Comprobar un work item

```bash
python scripts/check-sdd-item.py <proyecto>/docs/sdd/<id>-<título>
python scripts/check-sdd-item.py --commit-message <archivo> --id <id>
```

## Validar el kit

```bash
python scripts/validate.py
```

Comprueba el estándar Agent Skills, las anclas y sellos de las plantillas SDD, el formato de los
agentes, el tamaño de `AGENTS.base.md` y que cada ADR esté en el índice. Se ejecuta antes de cada
commit al kit.

## Estado por fases

| Fase | Contenido | Estado |
| --- | --- | --- |
| 0 | Acuerdos, responsable, pilotos y ADR | Decisiones tomadas; ADR en este repositorio |
| 1 | Núcleo: reglas base, plantillas, adaptadores, validador, instalador | Construido; pruebas pendientes (ola 1 y 3): Calls4Grants, repo vacío, carga en Copilot |
| 2 | Flujo completo con subagentes y bucles; prueba del MCP al final | Construido: `quick-fix`, `enrich-us qa`, `test-cases` y `migration-reviewer` estable; el bucle de pipeline pasa a la fase 4 (ADR-0026). Pruebas pendientes (olas 2 y 3): Copilot VS Code y MCP |
| 3 | Guardarraíles: pruebas de arquitectura, hooks, permisos | Construido (ADR-0023); pruebas pendientes en Windows (ola 4) |
| 4 | CI/CD en Azure DevOps | Pendiente |
| 5 | Documentación de código | Adelantada: `document-code` (por work item) y `/document-project` (todo el proyecto); falta DocFX y OpenAPI en el pipeline |
| 6 | Piloto y medición | Pendiente |
| 7 | Extensión al grupo y repositorio en Azure Repos | Pendiente |

## Cómo contribuir

1. Rama desde `main`; un cambio por rama.
2. Si cambia una regla o un comportamiento, añade o sustituye un ADR.
3. `python scripts/validate.py` sin errores.
4. Entrada en `CHANGELOG.md`.
5. Commit según `core/templates/.gitmessage` (ADR-0004).
