# Prueba del bloque 2 de la fase 2 · `backend-dev` y `frontend-dev` · kit v0.6.0

**Objetivo:** comprobar que `wbs-execution` delega cada tarea en el agente de su capa con un paquete
cerrado, que verifica por su cuenta, que respeta los límites de los bucles y que la sesión
principal gasta menos contexto. En el 40944 fueron 175k.

**Work item:** 40933, con 03 y 04 aprobados.

| Tarea | Capa | Quién |
| --- | --- | --- |
| T-01 | Excel | `backend-dev` |
| T-02 | Investigadores | `frontend-dev` |
| T-03 | Modal | `frontend-dev` |
| T-04 | Verificación final | La sesión principal |

**Dónde:** rama `chore/sdd-kit-piloto` de Bonis, en PowerShell, con el kit en `..\fi-sdd-standard`.

## 1 · Instalar

```powershell
cd ..\fi-sdd-standard; python scripts\validate.py; cd ..\bonis_v2
python ..\fi-sdd-standard\scripts\install.py --target . --tools copilot,claude
git add .agents .github/agents .gitignore .sdd-kit.json   # los agentes son archivos nuevos: hay que añadirlos
git commit -m "chore(sdd): actualizar fi-sdd-standard a v0.6.0" -- .agents .github/agents .gitignore .sdd-kit.json
```

Esperado:
- `creado` `.github/agents/backend-dev.agent.md` y `.github/agents/frontend-dev.agent.md`.
- `creado` `.claude/agents/backend-dev.md` y `.claude/agents/frontend-dev.md`, y `.gitignore`
  con `+2 líneas`.
- Los skills, `actualizado` (v3.5).

El `commit` solo lleva archivos del kit. La carpeta del 40933 sigue preparada, sin commit.

Cierra Claude Code y ábrelo de nuevo. Pregunta «¿Qué subagentes tienes disponibles?»: deben salir
`code-explorer`, `backend-dev` y `frontend-dev`.

**Permisos.** Los agentes ejecutan `dotnet` y `yarn`. Claude Code pedirá permiso la primera vez;
acepta solo esos comandos.

## 2 · Ejecutar

Sesión nueva:

```text
/wbs-execution 40933
```

| Momento | Qué comprobar |
| --- | --- |
| Confirmación de inicio | Muestra «Implemented by»: T-01 → `backend-dev`, T-02 y T-03 → `frontend-dev`, T-04 → esta sesión. Propone T-02 ∥ T-03 en paralelo (archivos distintos). **Acepta el paralelo** para probarlo |
| T-01 | Llama a `backend-dev` con un paquete (SPEC literales, archivos, comandos). El informe trae Estado, Pruebas (en rojo primero, luego en verde) y Validación |
| Después de cada tarea | La sesión principal vuelve a ejecutar build y pruebas, y `git status --short`. Solo ella actualiza `05`, `CHANGELOG.md` y `bitacora.md` |
| T-02 y T-03 | Dos `frontend-dev` a la vez. Sin `@testing-library`, devuelven pasos de verificación manual |
| Si algo falla | Vuelve al agente con el error, como mucho 2 rondas, y después te pregunta |
| T-04 | Verificación final con los tres roles; la parte manual la haces tú |
| Al terminar | `/context` (40944: 175k) y `commit-message.md` |

No hagas el commit todavía: después viene el bloque 3 (revisión de QA) con el mismo work item.

## 3 · Resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación sin conflictos y agentes visibles | | |
| 2 | La confirmación asigna cada tarea al agente correcto | | |
| 3 | El paquete es cerrado (el agente no abre 03/04) | | |
| 4 | Pruebas primero en T-01 (rojo y luego verde) | | |
| 5 | Informe del agente con el formato y menos de 80 líneas | | |
| 6 | La sesión principal verifica por su cuenta y revisa el alcance | | |
| 7 | Solo la sesión principal escribe en `docs/sdd/` | | |
| 8 | T-02 y T-03 en paralelo sin conflictos | | |
| 9 | Bucles: ¿hubo reintentos? ¿Respetaron los límites? | | |
| 10 | Build, pruebas y lint en verde al final | | |
| 11 | Contexto de la sesión principal al terminar | | (40944: 175k) |
| 12 | Tiempo total | | |

## 4 · Qué enviar

- El registro de la sesión con `/context` al final.
- La carpeta `docs\sdd\40933-correcciones-rol-delegado\` en un zip (bórralo después del repositorio).
- `git status --short` al terminar.
- La tabla de resultados.
