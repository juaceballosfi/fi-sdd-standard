# ADR-0021 · `/project-context`: contexto del proyecto, documentación base y pruebas desde el inicio

- **Estado:** Aceptada (pendiente de confirmar en Bonis y Calls4Grants)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0003, ADR-0011, ADR-0013, ADR-0014, ADR-0020

## Contexto

La sección *Project context* de `AGENTS.md` se escribió a mano en Bonis: 189 líneas, cerca del
límite de 200 (ADR-0014). Calls4Grants, con la misma tecnología, es distinto:
- npm en lugar de yarn;
- traducciones que parecen generadas;
- CQRS en cinco proyectos;
- ningún proyecto de pruebas;
- un `.claude/` previo con agentes, skills y hooks.

Escribirlo a mano en cada proyecto es lento, desigual y se queda viejo. Además, los `docs/*.md` del
kit se instalaban como plantillas vacías, y Bonis ya tenía DocFX.

## Decisión

1. **Skill `/project-context`**, el primer paso después de `install.py`. El instalador lo indica al
   terminar. Se vuelve a ejecutar cuando cambia el stack.
   - Modo `update` (por defecto si ya hay contexto): propone cambios y no borra lo escrito a mano
     sin aprobación.
   - Modo `fresh`: ignora el contexto actual, para comparar.
2. **Datos con fuente:**
   - Un script determinista dentro del skill (`inventory.py`) lee los manifiestos, los pipelines,
     los submódulos, la documentación, las traducciones, las pruebas, Entity Framework, la
     configuración de IA previa y los endpoints REST.
   - `code-explorer` responde en paralelo las preguntas de arquitectura.
   - Lo que no está en el código se pregunta en un solo bloque.
   - Lo dudoso se marca `[REQUIRES-VALIDATION]`.
3. **Se ejecuta todo:** build, pruebas, lint y comprobación de tipos. Se anotan la duración y la
   línea base (avisos, fallos y errores de tipos que ya existían). Un comando mal escrito en
   `AGENTS.md` lo heredarían todos los agentes.
4. **Encabezados fijos** en *Project context*. Los skills y agentes buscan por título:
   *What this is* · *Commands* · *Local run* · *Architecture* · *Authorization and errors* ·
   *Data* · *Tests* · *Internationalization* · *Protected paths* · *Branches, CI and commits* ·
   *Documentation*.
   - Se admiten secciones propias del proyecto.
   - Objetivo: unas 150 líneas en total. El detalle va a `docs/` con un enlace.
5. **Documentación base estandarizada:**
   - `architecture.md`, `backend.md`, `database.md`, `api-reference.md`, `frontend.md` y
     `reglas-negocio.md` con encabezados fijos.
   - Se crean si no existen; si existen, se leen y se corrigen o completan.
   - El instalador ya no crea plantillas vacías.
   - `reglas-negocio.md` solo recoge reglas confirmadas: los `BR-XX` de `docs/sdd/*/pbi.md` y
     comentarios explícitos. Nunca se deduce una regla.
6. **DocFX:** si existe, se propone añadir los `docs/*.md` a su `toc.yml` y a su `content`.
   `api-reference.md` lista los endpoints REST y enlaza a la referencia de tipos de DocFX.
7. **Pruebas desde la instalación:** sin proyecto de pruebas, `/project-context` lo crea con
   `backend-dev`:
   - xUnit v3 y Moq, con el mismo framework que el proyecto;
   - una prueba de humo real;
   - incluido en la solución;
   - y propone el paso `dotnet test` en el pipeline, con aprobación.

   Las pruebas de componentes (`@testing-library`) son una dependencia nueva: se proponen como
   work item aparte.
8. **Configuración de IA previa** (el kit de Clavijo en Calls4Grants):
   - el conocimiento de `CLAUDE.md` y de los skills propios pasa a `AGENTS.md` y a `docs/`;
   - `CLAUDE.md` queda en `@AGENTS.md`;
   - los agentes que el kit sustituye se retiran;
   - los skills sin equivalente en el kit (por ejemplo, el que genera traducciones) se conservan y
     se citan;
   - los hooks se quedan hasta la fase 3.
9. **Comprobación determinista:** `check_project.py`, dentro del skill, valida:
   - los encabezados, el tamaño y el sello;
   - los `docs/*.md` y que `CLAUDE.md` importe `AGENTS.md`;
   - y avisa si las fuentes cambiaron después de la fecha del contexto (marca `sdd:context`).

## Consecuencias

- Un proyecto nuevo queda listo para el flujo SDD en una sesión, con pruebas y documentación base.
- La primera ejecución es larga: tiene que compilar y probar todo.
- El cambio en `docfx.json` y en el pipeline siempre necesita aprobación.
- La documentación completa (todos los endpoints, entidades, pantallas y los comentarios `///` de
  todo el código) no es parte de este paso: es `/document-project` (ADR-0022).

## Alternativas consideradas

- **Escribir *Project context* a mano con una guía:** es lo que se hizo en Bonis; no escala y se
  queda viejo.
- **Solo leer, sin ejecutar:** más rápido, pero los comandos y la línea base quedan sin verificar.
- **Que el instalador cree el proyecto de pruebas:** el instalador no sabe qué referenciar ni cómo
  probarlo; un agente con el inventario y la arquitectura sí.
