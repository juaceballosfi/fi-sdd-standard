# Prueba del bloque 1 de la fase 2 · `code-explorer` · kit v0.5.1

**Objetivo:** comprobar que `code-explorer` se instala y se usa en Claude Code y en Copilot (VS
Code), y que baja el contexto de `technical-analysis`. En el PBI 40944 llegó a 551k tokens; el
objetivo es quedar por debajo de 150k.

**Dónde:** en la rama `chore/sdd-kit-piloto` de Bonis. Comandos en PowerShell, desde la raíz de
Bonis, con el kit en `..\fi-sdd-standard`.

## 1 · Instalar

```powershell
cd ..\fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
```

Esperado:

- `creado .github/agents/code-explorer.agent.md`, que se versiona.
- `creado .claude/agents/code-explorer.md`, que es local; en `.gitignore` aparece `+1 líneas`.
- `actualizado` en los skills, que pasan a v3.3.
- «Todo en orden».

## 2 · ¿Lo ven las herramientas?

| Comprobación | Resultado |
| --- | --- |
| Claude Code: existe `.claude\agents\code-explorer.md` con `model: haiku`, y en una sesión **nueva** «¿Qué subagentes tienes disponibles?» incluye `code-explorer` (el asistente `/agents` ya no existe en Claude Code) | |
| VS Code: el selector de agentes **no** muestra el `code-explorer` de `.github/agents` (es solo subagente) | |
| VS Code: ¿aparece otro `code-explorer` por la copia de `.claude/agents`? ¿En el selector o en la lista de subagentes? | |
| VS Code: en *Configure Tools* está activo *Run Subagent* (`agent/runSubagent`) | |

Prueba directa en cada herramienta, en una sesión nueva:

```text
Usa el subagente code-explorer para responder: ¿dónde se construye el menú lateral del servicio y
qué decide qué entradas ve cada rol?
```

| Comprobación | Claude Code | Copilot (VS Code) |
| --- | --- | --- |
| Llama a `code-explorer` (no busca por su cuenta) | | |
| La respuesta sigue el formato: Respuesta · Archivos · Patrones · Pruebas · No cubierto, en menos de 60 líneas | | |
| Cita `nav-items.ts` y `tenant-layout.tsx` con líneas | | |
| Contexto de la sesión principal al terminar (`/context` en Claude Code) | | — |

## 3 · Work item real

Elige un PBI o bug **pequeño** de Bonis, mejor si toca backend y frontend: servirá también para el
bloque 2. Prepara la carpeta como siempre (`new-sdd-item.py`, `story.md` y comprobador).

Con Claude Code, cada paso en una sesión nueva:

| Paso | Qué comprobar |
| --- | --- |
| `/enrich-us <ID>` | Usa `code-explorer` en el paso 3 (contexto técnico) · `/context` al terminar |
| `/technical-analysis <ID>` | Lanza varias preguntas a `code-explorer` antes del resumen de confirmación, a ser posible en paralelo · solo abre archivos para confirmar líneas · `/context` al terminar (**objetivo: menos de 150k**) |

Si necesitas pasarle un log, guárdalo en un archivo y dale la ruta: no lo pegues.

## 4 · Resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos | | |
| 2 | `code-explorer` visible en Claude Code | | |
| 3 | `code-explorer` usable como subagente en VS Code | | |
| 4 | Duplicados en VS Code (`.github/agents` + `.claude/agents`) | | |
| 5 | La prueba directa devuelve el formato esperado | | |
| 6 | `enrich-us` delega la exploración | | |
| 7 | `technical-analysis` delega la exploración | | |
| 8 | Contexto de `enrich-us` | | (40944: 107k) |
| 9 | Contexto de `technical-analysis` | | (40944: 551k) |
| 10 | Calidad del diseño 00–06 comparada con el 40944 | | |

## 5 · Qué enviar

- La tabla de resultados.
- La salida de `/context` de cada paso.
- La carpeta `docs/sdd/<id>-<título>/`.
- Si algo falla en VS Code, una captura del selector de agentes y de *Configure Tools*.
