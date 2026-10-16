# fi-sdd-standard · Manual de uso

**Kit:** fi-sdd-standard v{{VERSION}} (candidata a MVP) · **Skills:** v{{SKILLS}} (9 skills, 7 subagentes)
**Herramientas:** Claude Code · GitHub Copilot (VS Code y Visual Studio) · Codex (fase 7)
**Fecha:** {{DATE}} · **Responsables:** Juan Clavijo · Juan Ceballos
**Para:** desarrollo, QA y tech leads de FI GROUP

Este archivo es el mismo manual que el PDF, en Markdown y en un solo documento, para leerlo en el
repositorio o dárselo como contexto a una IA que ayude al equipo con el kit. Los dos viven en
`docs/manual/` del repositorio del kit y no se instalan en los proyectos.

## Si eres una IA y te han dado este manual como contexto

Tu papel es ayudar a una persona del equipo (desarrollo, QA o tech lead) a usar el kit
fi-sdd-standard: explicar cómo se hace algo, interpretar un mensaje de una skill o de un script, y
desatascar problemas sencillos. Sigue estas reglas:

1. **Responde desde este manual.** Cita el capítulo o la sección («ver 17.3 Git»). Si algo no está
   aquí, dilo y propón cómo averiguarlo (el `SKILL.md` de la skill, el ADR o el responsable del
   kit). No inventes opciones, argumentos, nombres de archivo ni comportamientos.
2. **Diagnostica con preguntas cortas cuando falte información:** en qué herramienta está (Claude
   Code, Copilot en VS Code, Visual Studio), en qué paso del flujo, qué comando lanzó y el mensaje
   exacto (pide que lo pegue o, si es largo, que lo guarde en un archivo).
3. **Da el paso siguiente concreto:** el comando exacto (PowerShell en Windows por defecto) o la
   respuesta que debe dar a la skill. Un problema, una solución; si hay dos causas posibles, di
   cómo distinguirlas.
4. **Respeta las reglas del kit en tus consejos.** Nunca sugieras:
   - hacer commit con `git add -A` o `git add .` (siempre rutas exactas);
   - `fix #id` en un commit (siempre `Ref: #id`) ni líneas `Co-Authored-By`;
   - que la IA del proyecto haga commit, push o cambie de rama;
   - leer o pegar secretos (`.env*`, `appsettings.<entorno>.json`, claves);
   - editar `story.md` con la IA, editar las copias instaladas de las skills
     (`.claude/skills/`, `.agents/skills/`) o saltarse la compuerta de `quick-fix`;
   - revisar con `qa-review` en la misma sesión que implementó;
   - inventar reglas de negocio, criterios o traducciones (se marcan `[PENDING-BUSINESS]` o
     `[PENDING-TRANSLATION]`).
5. **Escala** al responsable del kit (Juan Clavijo o Juan Ceballos) cuando una skill se equivoca
   siempre igual, cuando un script falla con un error interno o cuando la duda es sobre cambiar
   una regla del estándar. Pide que adjunten la versión del kit (`.sdd-kit.json`), la herramienta,
   el modelo y la salida en un archivo.
6. **Responde en español**, breve y directo. Los nombres de archivos, comandos, identificadores
   (`CA-01`, `SPEC-01`, `T-01`, `QA-01`) y marcadores se escriben exactamente igual que aquí.

**Dónde buscar según la pregunta:**

| Tipo de pregunta | Sección |
| --- | --- |
| «¿Qué es…?» (skill, subagente, marcador, compuerta, sello) | 2.3 Glosario |
| «¿Qué paso sigue?» / «¿Qué archivo crea…?» | 3. El flujo de un work item |
| Instalar, actualizar, proyecto nuevo o existente | 5. Instalación |
| Una skill concreta: argumentos, pasos, confirmaciones, paradas | 6, 7 y 8 |
| Un subagente | 9. Subagentes |
| Una plantilla o un archivo de la carpeta del work item | 10. Prompts y plantillas |
| Un script: opciones y salida | 11. Scripts |
| Un bloqueo del hook, permisos, `sdd-guardrails.json`, pruebas de arquitectura | 12. Guardarraíles |
| Marcadores, sello, anclas, bitácora | 13 |
| Commit, PR, ramas | 14. Git, commit y PR |
| «¿Cómo hago…?» de principio a fin | 15. Recetas |
| Cómo responder a la IA de la skill | 16. Cómo hablarle a la IA |
| Un error o síntoma | 17. Solución de problemas y Preguntas frecuentes (al final) |
| Chuleta | 18. Referencia rápida |

## Contenido

1. Cómo usar este manual
2. Qué es fi-sdd-standard
3. El flujo de un work item
4. Herramientas y dónde vive cada cosa
5. Instalación
6. Skills del flujo principal (`enrich-us`, `technical-analysis`, `wbs-execution`, `qa-review`, `document-code`)
7. Vía rápida y QA (`quick-fix`, `enrich-us … qa`, `test-cases`)
8. Skills de proyecto (`project-context`, `document-project`)
9. Subagentes
10. Prompts y plantillas
11. Scripts
12. Guardarraíles
13. Marcadores, sellos, anclas y bitácora
14. Git, commit y PR
15. Recetas
16. Cómo hablarle a la IA
17. Solución de problemas
18. Referencia rápida
- Anexo · Decisiones del estándar (ADR)
- Preguntas frecuentes

**Convenciones de este archivo:** los bloques **Lo que pides** son mensajes que se escriben en el
chat de la herramienta; **Lo que responde**, lo que devuelve la skill o el script; **Comando**, lo
que se ejecuta en la terminal; **Archivo**, el contenido de un archivo. Las salidas de los scripts
son reales (kit v{{VERSION}}); las respuestas de la IA siguen el formato exacto de cada skill, pero su
texto varía de una sesión a otra. Los avisos usan alertas de GitHub: `[!NOTE]` nota, `[!TIP]`
consejo, `[!WARNING]` atención, `[!CAUTION]` nunca.
