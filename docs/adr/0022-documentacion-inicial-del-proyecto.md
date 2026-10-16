# ADR-0022 · `/document-project`: documentación inicial y completa del proyecto

- **Estado:** Aceptada (pendiente de probar en Bonis)
- **Fecha:** 2026-10-15
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0014, ADR-0020, ADR-0021

## Contexto

`document-code` (ADR-0020) documenta solo lo que toca un work item. `/project-context` (ADR-0021)
deja el mapa del proyecto: `AGENTS.md` y los `docs/*.md` base. Falta un paso que recorra todo el
proyecto una vez y deje la documentación completa:
- todos los endpoints, entidades y pantallas;
- las reglas de negocio confirmadas;
- y los comentarios `///` y TSDoc del código público, que en Bonis alimentan DocFX.

Es el trabajo de la fase 5 del brief (documentación de código), adelantado porque el kit ya tiene
las piezas: `doc-writer`, `comment_only.py` y los documentos base.

## Decisión

1. **Skill `document-project` v3.8**, después de `/project-context` (lo exige: lee su contexto y
   comprueba con `check_project.py`). Es `document-code` aplicado a código que ningún work item
   tocó.
2. **Plan reanudable** en `docs/sdd/_documentacion/plan.md`: áreas, bloques, estados, hallazgos y
   registro. Cada bloque deja su registro en `B-NN.md` con el mensaje de commit.
3. **Áreas.** Las propone un script determinista, `doc_coverage.py`:
   - una por controlador, con los servicios que solo él inyecta y los tipos que solo él usa;
   - transversales: controladores base, servicios compartidos y el resto de carpetas;
   - en el frontend, una por carpeta de funcionalidad.

   El script también parte las áreas grandes (como máximo 15 archivos de código y 60 símbolos sin
   documentar), sin separar una entidad de su configuración, una interfaz de su clase ni las partes
   de una clase parcial, y propone los bloques. La sesión solo corrige lo que el script no puede
   saber, y `doc_coverage.py --check-plan` comprueba que cada archivo está en un área y solo en una
   (v0.10.1, tras la primera prueba en Bonis).
4. **Orden: dependencias primero, después uso.** Transversal del backend → controladores (los más
   cambiados en 6 meses primero) → transversal del frontend → secciones del frontend. Lo transversal
   va primero para que los comentarios siguientes lo citen con `<see cref>` en vez de repetirlo.
5. **Bloques:** 3 a 5 áreas y como máximo unos 40 archivos. Un bloque por sesión, un commit y un PR.
6. **Pruebas existentes:** solo el resumen de cada clase (qué cubre), con el área de la clase que
   prueban. Nada por prueba.
7. **Mismas garantías que `document-code`:**
   - `doc-writer` escribe; lo que no da el paquete se describe «desde el código»: qué hace, nunca la
     intención;
   - el porqué solo con una fuente escrita: commit con `#<ID>`, carpeta del work item, ADR,
     documento;
   - `comment_only.py` demuestra que solo cambiaron comentarios;
   - build, lint, tipos y DocFX sin avisos nuevos respecto a la línea base del plan;
   - la sesión lee el diff de comentarios y comprueba contra el código las afirmaciones sobre
     autorización, errores, efectos y negocio.
8. **Hallazgos:** lo que parece mal se anota en el plan y, si merece un work item, va a
   `_borradores/`. Nunca se corrige código aquí.
9. **Medible:** `doc_coverage.py` da la cobertura antes y después de cada bloque, y CS1591 si el
   proyecto genera la documentación XML.

## Consecuencias

- La documentación completa de un proyecto grande son varios PR (Bonis: unos 330 endpoints, del
  orden de 10 a 15 bloques), revisables uno a uno.
- Conviene un work item para el esfuerzo («Documentación inicial del proyecto»), para que los
  commits lleven `Ref: #<ID>`.
- Después de un bloque, el código lo mantiene `document-code` en cada work item; `/document-project
  status` avisa de los archivos cambiados después de documentarse.
- `doc-writer` participa también en el paso 0 (`sdd_steps: [0, 5]`).
