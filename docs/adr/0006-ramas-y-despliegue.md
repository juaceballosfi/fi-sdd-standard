# ADR-0006 · Ramas y despliegue

- **Estado:** Aceptada
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

Los pipelines de Bonis y Calls4Grants despliegan `dev` a Dev, `main` a Staging y la etiqueta
`prod` a Producción. No todos los proyectos tienen *environment* de Dev. Los YAML no muestran
validación de PR ni aprobaciones.

## Decisión

1. Se trabaja en `feature/<id>-<título>` o `bugfix/<id>-<título>`, creadas desde `dev`.
2. PR a `dev` con `pr-validation.yml` en verde, un revisor, work item enlazado y comentarios
   resueltos. Se recomienda *squash merge*.
3. En `dev` se compila y se prueba; el despliegue a Dev es opcional por proyecto.
4. PR de `dev` a `main` con la misma validación y la aprobación del responsable; `main` despliega a Staging.
5. Producción: solo el PM. Crea la etiqueta `prod` (permiso restringido) y aprueba el
   *environment* de producción.

## Consecuencias

- Las plantillas de pipeline tienen el despliegue a Dev como parámetro.
- Hay que configurar políticas de rama en `dev` y `main` y restringir la etiqueta `prod`.

## Alternativas consideradas

- PR directos a `main`: mezcla trabajo sin integrar con lo que va a Staging.
