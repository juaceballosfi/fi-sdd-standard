# Agentes en formato neutral

Cada agente se define una vez aquí. `scripts/install.py` genera el formato de cada herramienta
(ADR-0011, ADR-0017):

- `.github/agents/<nombre>.agent.md`, versionado, para Copilot en VS Code y Visual Studio.
- `.claude/agents/<nombre>.md`, copia local en `.gitignore`, para Claude Code.
- Codex (`.codex/agents/*.toml`) llega en la fase 7.

Solo se instalan los agentes con `status: stable`.

## Formato

```yaml
---
name: backend-dev                 # igual al nombre del archivo, minúsculas y guiones
description: What it does. Use ... (English; it decides when the agent is picked)
permissions: [read, edit, execute] # read | edit | execute
model_tier: standard               # fast | standard | reasoning
sdd_steps: [3]                     # pasos del flujo donde participa
skills: []                         # skills de core/skills que puede usar
status: draft                      # draft (no se instala) | stable (se instala)
---
Instructions in English. The output the agent returns is in Spanish.
```

| Neutral | Claude Code | Copilot | Codex |
| --- | --- | --- | --- |
| `read` | `Read, Grep, Glob` | `read`, `search` | sandbox de solo lectura |
| `edit` | `Edit, Write` | `edit` | escritura en el espacio de trabajo |
| `execute` | `Bash` | `execute` | ejecución de comandos |
| `model_tier` | `haiku` / `sonnet` / `opus` | modelo de la conversación | — |

La tabla de modelos está en `scripts/install.py` y se revisa cada mes (ADR-0014). Ningún agente
conoce un proyecto concreto: lee lo que necesita de `AGENTS.md`.

## Estado

| Agente | Estado | Bloque de la fase 2 |
| --- | --- | --- |
| `code-explorer` | stable | 1 |
| `backend-dev`, `frontend-dev` | stable | 2 |
| `qa-reviewer`, `runtime-tester` | stable | 3 |
| `migration-reviewer` | draft | 3 (cuando un work item tenga una migración) |
| `doc-writer` | stable | 4 |
