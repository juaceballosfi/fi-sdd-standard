# [Título descriptivo del bug]

**Generado con:** enrich-us v3.9 · [Claude Code | GitHub Copilot | Codex] · [modelo]
**Work item:** #[ID] | **Sprint:** [iteración, si se conoce] | **Fecha:** [AAAA-MM-DD] | **Tipo:** Bug | **Fuente:** story.md (work item #[ID], revisión [N])

---

## Descripción del defecto
<!-- sdd:description -->
[Descripción clara del problema reportado.]

## Pasos de reproducción
| Paso | Acción | Resultado actual |
| ---- | ------ | ---------------- |
| 1 | … | … |

**Precondiciones:** …
**Frecuencia:** Siempre / Intermitente / Rara
**Entorno:** [dónde se detectó]

## Comportamiento esperado vs actual
| Aspecto | Esperado | Actual |
| ------- | -------- | ------ |
| … | … | … |

## Causa raíz inferida
[Análisis técnico de la causa probable a partir del código. Si no hay evidencia suficiente,
marcar `[REQUIRES-VALIDATION: motivo]`.]

**Archivo(s) sospechoso(s):**
- `ruta/archivo` línea ~N — [descripción del problema]

## Archivos / módulos a modificar
| Archivo | Capa | Cambio | Origen |
| ------- | ---- | ------ | ------ |
| `ruta/archivo` | [Dominio / Aplicación / Infraestructura / UI] | Modificar | Inferido del código / story.md |

## Criterios de aceptación (corrección)
<!-- sdd:acceptance-criteria -->
| ID | Criterio | Tipo | Prioridad | Origen |
| -- | -------- | ---- | --------- | ------ |
| CA-01 | Dado [contexto] Cuando [acción] Entonces [resultado correcto] | Funcional | Alta | story.md |

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

## Pruebas requeridas
| Tipo | Componente | Escenario | Ubicación |
| ---- | ---------- | --------- | --------- |
| Unitaria | … | Caso que reproduce el bug | `ruta/test` |
| Regresión | … | El fix no rompe nada existente | `ruta/test` |

## Impacto y alcance
| Dimensión | Detalle |
| --------- | ------- |
| Usuarios afectados | … |
| Módulos relacionados | … |
| Riesgo de regresión | Alto / Medio / Bajo |

## Definición de hecho
- [ ] Bug reproducido en una prueba antes del fix
- [ ] Fix implementado
- [ ] Prueba de regresión en verde
- [ ] Sin regresiones en la funcionalidad existente
- [ ] Textos nuevos o modificados presentes en todos los idiomas del proyecto (o N/A)
- [ ] Code review aprobado

## Notas de implementación
[Sugerencias técnicas, advertencias, dependencias.]

## Campos pendientes de aclaración
<!-- sdd:pending -->
[Lista de `[PENDING-BUSINESS: pregunta concreta]`, o exactamente la palabra "Ninguno".]
