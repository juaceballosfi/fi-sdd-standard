# Resultados del bloque 4 de la fase 2 · `document-code` · PBI 40933

**Fecha:** 2026-10-15 · **Kit:** v0.8.0 (skills v3.7) · **Quién:** Juan Ceballos
**Alcance:** `9e07c66d` → árbol de trabajo (el 40933 ya está en `dev` con los PR 14468 y 14472).

## Resumen

El paso funciona y su red de seguridad también. `document-code` eligió bien qué documentar:
- 8 comentarios de documentación, todos con su fuente;
- ningún comentario del porqué nuevo, porque los que hacían falta ya estaban con `#40933`;
- nada en los componentes de React, que ya estaban comentados;
- ninguna ADR.

`comment_only.py` y el build detectaron los dos fallos de esta ronda: los avisos CS1573 de
`doc-writer` y el archivo que la sesión principal rompió al arreglarlos a mano. Así no llegó nada roto
al commit.

## Tabla de resultados

| # | Comprobación | Resultado | Notas |
| --- | --- | --- | --- |
| 1 | Instalación y 6 agentes | ✓ | Commit del kit `ce8b2f9b` |
| 2 | Archivos del item tomados del CHANGELOG, sin los del kit | ✓ | 6 archivos de código |
| 3 | Inventario con fuente; nada inventado | ✓ | 03 §3.1, §3.5, BR-03, R-01, CHANGELOG T-01 |
| 4 | Confirmación antes de escribir | ✓ | Ofreció quitar lo opcional (`frontend.md`) |
| 5 | Snapshot antes y `check` después | ✓ | Solo los 3 archivos que se iban a tocar |
| 6 | Build sin avisos nuevos | ✓ al final | La primera versión dejó 80 avisos CS1573: había `<param>` solo en algunos parámetros. Se corrigió |
| 7 | Calidad de los comentarios | ✓ | En español, el porqué y la diferencia `isManager`/`isDelegate`, las fuentes y la pareja cabecera-valor (R-01). Los resúmenes de las pruebas pasaron de `//` a `///` |
| 8 | `docs/` con hechos y fuente | ✓ con ruido | Contrastó la ruta y los roles con el controlador. `(#40933)` se repite en cada viñeta. Detectó que `GetDeletedTrackingsExportExcel` es solo para `Consultant` y `Freelance` |
| 9 | Registro | ✓ | Entrada en el CHANGELOG, una línea en la bitácora y el mensaje `docs(roles)` entero (596 caracteres) |
| 10 | Comprobador | ✓ | `✓ documentación` |
| 11 | Contexto y tiempo | — | Sin `/context`. 1 min de inventario y 7 min 50 s en total |
| 12 | ¿Aprobables en un PR? | ✓ | Ver el diff: comentarios útiles, sin repetir el código |

## Lo que hay que mejorar (aplicado en el kit, sale en la v0.9.0)

1. **`<param>`, todo o nada.** `doc-writer` documentaba solo el parámetro nuevo y C# avisaba de los
   demás (CS1573). Regla nueva: un solo parámetro se explica en `<remarks>`.
2. **La sesión principal no parchea comentarios con scripts.** Un reemplazo con expresión regular
   dejó `\x01` en lugar de `</summary>`. Si algo falla, el comentario vuelve a `doc-writer` o el
   archivo se restaura con el comando nuevo `comment_only.py restore`.
3. **`docs/`:** una sola referencia `(#ID)` por sección, no en cada línea.
4. **Guía git:** las tildes que salen como `├®` en `git diff | Select-String` son cómo las muestra la
   consola de PowerShell, no un fallo del archivo.

## Para el desarrollador

- Los `docs/*.md` del proyecto (`reglas-negocio.md`, `api-reference.md`, `frontend.md`) existen
  solo en la rama del piloto, porque los creó el instalador. Se suben en dos commits: los
  comentarios y la carpeta del item por PR, y `docs/` con el PR del kit.
- Subido:
  - PR 14473 (`docs(roles): documentar el export de seguimientos para delegados`), mezclado en `dev`
    (`529c5c31`).
  - `docs/*.md` en el piloto (`aa30e244`); llegarán con el PR del kit.
  - Build de la rama: 0 errores; las 222 advertencias ya existían (ninguna CS15xx). **Bloque 4 cerrado.**
- Bonis tiene `docs/docfx` en `dev`: hay que decidir si los `docs/*.md` que crea el kit sobran ahí
  (ver `/project-context`).

