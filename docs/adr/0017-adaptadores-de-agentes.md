# ADR-0017 · Adaptadores de agentes: `.github/agents/` versionado y `.claude/agents/` local

- **Estado:** Aceptada (pendiente de confirmar en la prueba del bloque 1)
- **Fecha:** 2026-10-14
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0011, ADR-0013, ADR-0014

## Contexto

Los agentes se definen una vez en `core/agents/` con formato neutral (ADR-0011) y cada herramienta
los lee de un sitio distinto:

| Herramienta | Dónde lee los agentes | Formato |
| --- | --- | --- |
| Claude Code | `.claude/agents/*.md` | `name`, `description`, `tools` con nombres de Claude, `model` (`haiku`, `sonnet`, `opus`) y otros |
| Copilot en VS Code | `.github/agents/*.agent.md` **y también** `.claude/agents/*.md` | `.agent.md`: `tools` como lista de VS Code, `user-invocable`, `model` con nombres de Copilot. De `.claude/agents` solo documenta `name`, `description`, `tools` y `disallowedTools` |
| Copilot en Visual Studio | `.github/agents/` (en vista previa) | El de `.agent.md` |
| Codex | `.codex/agents/*.toml` | Fase 7 |

Es la misma situación que con los skills (ADR-0011). Además, la documentación de VS Code no dice
qué hace con el campo `model` de los agentes de Claude, y en la prueba de la v2.0 un `model: sonnet`
en un skill bloqueó Copilot.

## Decisión

Se sigue el mismo patrón que con los skills:

- **`.github/agents/<nombre>.agent.md`, versionado.** Lo leen Copilot en VS Code y en Visual
  Studio. Lleva `user-invocable: false`, para que el agente no salga en el selector y solo se use
  como subagente, y no fija modelo: usa el de la conversación.
- **`.claude/agents/<nombre>.md`, copia local en `.gitignore`.** Lleva los nombres de herramienta y
  el modelo de Claude Code.
- **Solo se instalan los agentes con `status: stable`.** Los borradores se quedan en el kit.
- **Correspondencias:**

| Neutral | Claude Code | Copilot |
| --- | --- | --- |
| `read` | `Read, Grep, Glob` | `read`, `search` |
| `edit` | `Edit, Write` | `edit` |
| `execute` | `Bash` | `execute` |
| `model_tier: fast` | `model: haiku` | (modelo de la conversación) |
| `model_tier: standard` | `model: sonnet` | (modelo de la conversación) |
| `model_tier: reasoning` | `model: opus` | (modelo de la conversación) |

- **Los skills delegan en `code-explorer`** con una convención compartida (skills v3.3). Si la
  herramienta no tiene subagentes, el skill busca por su cuenta con las reglas de entradas grandes.

## Consecuencias

- `code-explorer` corre en Claude Code con un modelo rápido y barato. En Copilot usa el de la
  conversación, porque los nombres de modelo dependen de las licencias de cada organización. Se
  revisará en la fase 6 con los datos de consumo.
- En VS Code, quien tenga también la copia de Claude Code verá dos `code-explorer`, igual que con
  los skills. La prueba del bloque 1 comprueba si VS Code los muestra o usa los dos. Si da
  problemas, la alternativa es instalar para Claude Code solo los campos que VS Code entiende.
- Los nombres de herramienta de Copilot (`read`, `search`, `edit`, `execute`) se toman de la
  documentación de VS Code y se confirman en la prueba. Si uno no existe, VS Code lo ignora.

## Alternativas consideradas

- **Solo `.claude/agents/` versionado, porque VS Code también lo lee:** un único archivo para dos
  herramientas. Se descarta por ahora, porque Visual Studio no lo lee y no está claro qué hace VS
  Code con `model`.
- **Solo `.github/agents/`:** Claude Code no lo lee.
