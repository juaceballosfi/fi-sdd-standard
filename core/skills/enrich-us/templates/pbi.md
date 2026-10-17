# [Título descriptivo del PBI]

**Generado con:** enrich-us v3.10 · [Claude Code | GitHub Copilot | Codex] · [modelo]
**Work item:** #[ID] | **Sprint:** [iteración, si se conoce] | **Fecha:** [AAAA-MM-DD] | **Tipo:** PBI | **Fuente:** story.md (work item #[ID], revisión [N])

---

## Descripción funcional
<!-- sdd:description -->
[Descripción clara desde la perspectiva del usuario: "como [rol] quiero [acción] para [beneficio]",
ampliada con el detalle técnico necesario.]

## Criterios de aceptación
<!-- sdd:acceptance-criteria -->
| ID | Criterio | Tipo | Prioridad | Origen |
| -- | -------- | ---- | --------- | ------ |
| CA-01 | Dado [contexto] Cuando [acción] Entonces [resultado] | Funcional | Alta | story.md |

## Campos / entidades afectadas
| Entidad / DTO | Campo | Tipo | Cambio | Validaciones | Origen |
| ------------- | ----- | ---- | ------ | ------------ | ------ |
| … | … | … | Nuevo / Modificar / Eliminar | … | … |

## Endpoints
| Verbo | URL | Request | Response | Auth | Descripción | Origen |
| ----- | --- | ------- | -------- | ---- | ----------- | ------ |
| … | … | `{ … }` | `{ … }` | [Rol] | … | … |

## Archivos / módulos a modificar
| Archivo | Capa | Cambio | Origen |
| ------- | ---- | ------ | ------ |
| `ruta/archivo` | [Dominio / Aplicación / Infraestructura / UI] | Nuevo / Modificar | Inferido del código / story.md |

## Reglas de negocio
| ID | Regla | Condición | Acción | Origen |
| -- | ----- | --------- | ------ | ------ |
| BR-01 | … | … | … | story.md |

## Clasificación de QA
<!-- sdd:qa-classification -->
[Solo en modo `qa`. Sin modo QA: «N/A».]

| CA | Clasificación | Fuente | Pregunta (si A confirmar) |
| -- | ------------- | ------ | ------------------------- |
| CA-01 | Definido / Deducción directa / A confirmar | story.md § / `assets/…` / `archivo:línea` | … |

## Textos visibles e idiomas
<!-- sdd:i18n -->
**Sistema de traducción:** [archivo(s) · mecanismo | N/A] · **Idiomas:** [es, en, fr, pt… | N/A]
**Convención de claves:** [p. ej. la clave es el texto literal en inglés | namespaces | N/A]
**Si falta una clave:** [cae al idioma por defecto sin aviso | muestra la clave | error | N/A]

| Texto (idioma de la historia) | Clave | Dónde se muestra | Cambio | Origen |
| ----------------------------- | ----- | ---------------- | ------ | ------ |
| … | … | [pantalla / mensaje / correo / exportación] | Nuevo / Modificar / Eliminar | story.md / Propuesto — validar con PO |

[Sin sistema de traducción o sin textos visibles: escribir solo "N/A" bajo el encabezado.]

## Requisitos no funcionales
[Omitir la sección si no hay evidencia. Nunca inventar métricas.]

| Categoría | Requisito | Métrica |
| --------- | --------- | ------- |
| Seguridad | … | … |

## Pruebas requeridas
| Tipo | Componente | Escenario | Ubicación |
| ---- | ---------- | --------- | --------- |
| Unitaria | … | … | `ruta/test` |
| Integración | … | … | `ruta/test` |

## Definición de hecho
- [ ] Endpoints implementados y funcionando
- [ ] Validaciones aplicadas según las reglas de negocio
- [ ] Pruebas unitarias escritas y en verde
- [ ] Pruebas de integración en verde (si aplica)
- [ ] Sin regresiones en la funcionalidad existente
- [ ] Textos nuevos o modificados presentes en todos los idiomas del proyecto (o N/A)
- [ ] Code review aprobado

## Notas de implementación
[Sugerencias técnicas, patrones a seguir, advertencias de acoplamiento.]

## Campos pendientes de aclaración
<!-- sdd:pending -->
[Lista de `[PENDING-BUSINESS: pregunta concreta]`, o exactamente la palabra "Ninguno".]
