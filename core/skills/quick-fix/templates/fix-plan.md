# Plan de corrección — <ID> <Título>

**Generado con:** quick-fix v3.9 · [Claude Code | GitHub Copilot | Codex] · [modelo]
**Work item:** #<ID> · **Fecha:** AAAA-MM-DD · **Estado:** Aprobado (<persona>, AAAA-MM-DD)

## Vía rápida
<!-- sdd:fix-gate -->

| Criterio | Resultado | Evidencia |
| --- | --- | --- |
| Causa en el código | ✓ | `ruta/Archivo.cs:NN` |
| Tamaño (≤ 3 archivos, una capa) | ✓ | N archivos · Backend / Frontend |
| Datos (sin migración ni entidad) | ✓ | — |
| Contratos (rutas, DTO, eventos) | ✓ | — |
| Seguridad (autorización, roles, tenants) | ✓ | — |
| Negocio (sin `[PENDING-BUSINESS]`) | ✓ | story.md: «…» |
| Textos visibles | ✓ | ninguno nuevo / traducidos en es, en, fr |
| Dependencias | ✓ | — |

## Causa
<!-- sdd:fix-cause -->

[Qué hace mal el código y por qué, con `archivo:línea`. Una afirmación sobre el código, no una
hipótesis.]

## Cambio

| Archivo | Cambio |
| --- | --- |
| `ruta/Archivo.cs` | [qué cambia] |

**No cambia:** [contratos, permisos, comportamiento de otros casos].

## Pruebas
<!-- sdd:fix-tests -->

| Prueba | Tipo | Rojo esperado antes del cambio | Archivo |
| --- | --- | --- | --- |
| `Metodo_Escenario_Resultado` | Unitaria / Integración | [falla porque …] | `ruta/Tests.cs` |

**Regresión:** [pruebas existentes que deben seguir en verde].

## Riesgos

[Una o dos líneas, o «Ninguno».]

## Tarea
<!-- sdd:tasks -->

| ID | Tarea | Capa | Estado |
| --- | --- | --- | --- |
| T-01 | [Prueba que reproduce el defecto y corrección] | Backend / Frontend | ⬜ Pendiente |
