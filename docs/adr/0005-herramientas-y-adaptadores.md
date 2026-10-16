# ADR-0005 · Herramientas soportadas y rutas de cada una

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0011

## Contexto

La mayoría del equipo tiene licencia de GitHub Copilot, varios usan Claude Code y llegarán
licencias de Codex. Es probable que haya quien use Copilot dentro de Visual Studio. Cada
herramienta lee las reglas, skills y agentes de rutas distintas.

## Decisión

Se soportan Copilot en VS Code, Copilot en Visual Studio y Claude Code desde el inicio, y Codex
cuando lleguen las licencias. Rutas que genera el kit en cada proyecto:

| Pieza | Copilot · VS Code | Copilot · Visual Studio | Claude Code | Codex |
| --- | --- | --- | --- | --- |
| Reglas | `AGENTS.md` | `.github/copilot-instructions.md` (generado desde `AGENTS.md`) | `CLAUDE.md` con `@AGENTS.md` | `AGENTS.md` |
| Skills | `.agents/skills/` | `.agents/skills/` (desde 18.5) | `.claude/skills/` (copia generada, en `.gitignore`) | `.agents/skills/` |
| Agentes | `.github/agents/*.agent.md` | `.github/agents/*.agent.md` (preview, sin subagentes) | `.claude/agents/*.md` | `.codex/agents/*.toml` |
| Hooks | — (pipeline) | — (pipeline) | `.claude/settings.json` + PowerShell | — (pipeline) |

Fuentes consultadas entre el 9 y el 13 de octubre de 2026: documentación de VS Code, Visual
Studio, GitHub Copilot, Claude Code y Codex sobre skills, agentes e instrucciones.

## Consecuencias

- VS Code suma las fuentes de instrucciones (`AGENTS.md`, `CLAUDE.md` y
  `.github/copilot-instructions.md`). Donde se genere la copia para Visual Studio, VS Code cargaría
  las reglas dos veces: se evita con `"github.copilot.chat.codeGeneration.useInstructionFiles": false`
  en `.vscode/settings.json`. Por eso `CLAUDE.md` es una sola línea (`@AGENTS.md`): VS Code también lo lee.
- Codex y Copilot en VS Code leen `AGENTS.md` directamente: no necesitan ningún archivo propio de reglas.
- En Visual Studio cada agente se elige a mano en el selector.
- Las rutas cambian con frecuencia: la prueba de compatibilidad se repite en cada versión del kit.

## Alternativas consideradas

- Soportar solo Copilot: deja fuera a quien usa Claude Code y a Codex.
