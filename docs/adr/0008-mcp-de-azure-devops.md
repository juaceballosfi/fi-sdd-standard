# ADR-0008 · MCP de Azure DevOps en solo lectura, tras una prueba en el piloto

- **Estado:** Propuesta (se decide tras la prueba del final de la fase 2)
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0007

## Contexto

El MCP oficial de Azure DevOps permite al agente leer work items, comentarios y adjuntos con los
permisos de la persona. Hay un servidor remoto (`https://mcp.dev.azure.com/<organización>`,
autenticación con Entra ID, cabeceras `X-MCP-Toolsets` y `X-MCP-Readonly`) y uno local
(`npx @azure-devops/mcp`, Node.js 20 o superior). Codex solo admite el local; Claude Code necesita
un registro de aplicación en Entra para el remoto.

En la versión 2.10.0 del paquete local, la lectura de work items es `wit_work_item` y la descarga
de adjuntos `wit_work_item_attachment`. Escriben `wit_work_item_write`,
`wit_work_item_comment_write` y `wit_work_item_link_write`, y `wit_backlog` puede reordenar el
backlog. El servidor local no tiene modo de solo lectura.

## Decisión propuesta

- Probarlo al final de la fase 2, en Bonis, con tres work items reales, siempre en solo lectura:
  remoto con `X-MCP-Readonly: true` en VS Code; local con permisos que bloquean las herramientas de
  escritura y `wit_backlog` en Claude Code.
- Adoptarlo si VS Code y Claude Code cumplen: conexión sin ayuda de TI, texto completo y literal,
  comentarios, adjuntos, texto legible y escritura bloqueada.
- Si falla en una herramienta, usarlo donde funcione y mantener el texto pegado en la otra.

## Consecuencias

- Hay que confirmar con TI que la organización está vinculada a Entra ID.
- Solo se cargan los dominios necesarios (`core`, `work-items`), también para ahorrar contexto.
- El texto de los work items se trata como datos, nunca como instrucciones.

## Alternativas consideradas

- Habilitar escritura desde el inicio: riesgo innecesario antes de validar.
