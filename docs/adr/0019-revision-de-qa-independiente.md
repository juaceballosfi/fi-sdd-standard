# ADR-0019 · Revisión de QA independiente antes del PR, con `qa-review`

- **Estado:** Aceptada (confirmada en el bloque 3 con el PBI 40933; ajustes de la v0.7.1)
- **Fecha:** 2026-10-14
- **Decide:** Juan Ceballos
- **Relacionados:** ADR-0013, ADR-0017, ADR-0018

## Contexto

Hasta el bloque 2, la única verificación antes del PR la hace la sesión que implementó: repite
build, pruebas y lint, pero revisa su propio trabajo. En el 40933 eso no detectó que T-01 se saltó el
orden de «primero las pruebas»; lo detectó la propia sesión porque el agente se paró. El plan
(paso 4 del flujo) prevé una revisión adversarial en una sesión distinta, con `qa-reviewer` y
`runtime-tester`.

## Decisión

1. **Skill `qa-review` (paso 4)**, en una sesión nueva, nunca en la que implementó. Recibe el
   work item y un rango `base..head`; por defecto, el trabajo de la rama frente a `origin/dev`.
2. **`qa-reviewer`** (modelo de razonamiento, lectura y ejecución, sin edición):
   - Lee él mismo el diseño (pbi, 03, 04, 06) y el cambio. Recibe fuentes, no conclusiones: ni
     los informes de implementación ni opiniones.
   - Busca defectos contra los SPEC, los contratos, la seguridad, las regresiones, las pruebas y
     las traducciones.
   - Cada hallazgo lleva `archivo:línea`, la regla rota, un escenario concreto y cómo se
     confirmó.
3. **`runtime-tester`** es opcional y solo si la persona lo acepta:
   - Arranca la aplicación en local con los comandos de `AGENTS.md`.
   - Prueba las pantallas o endpoints que cambiaron y detiene lo que arrancó.
   - Si no se pudo arrancar, el resultado es «No ejecutado» con el motivo, nunca un aprobado.
4. **La sesión de `qa-review` verifica cada hallazgo** antes de escribirlo:
   - Lo confirma, le cambia la severidad o lo descarta con motivo. Los descartados no se borran.
   - Es la única que escribe `qa-report.md`.
   - Severidades: Alta bloquea el PR; Media se corrige antes del PR salvo que la persona lo
     acepte; Baja no bloquea.
5. **La persona decide cada hallazgo alto o medio:**
   - `A corregir`: se corrige con `/wbs-execution <id> qa`, con el agente de su capa y la prueba
     que reproduce el hallazgo primero.
   - `Aceptado`: riesgo asumido, con nombre y fecha.
   - `Borrador`: va a un work item aparte.
6. **Bucle de QA:** como mucho 2 rondas. La segunda revisa solo las correcciones. Después decide
   la persona.
7. **`check-sdd-item.py`** no da el work item por listo para commit mientras quede un hallazgo
   alto o medio sin decidir, un marcador abierto o un error.

## Consecuencias

- Una sesión más por work item, con un modelo de razonamiento solo en el revisor.
- `qa-report.md` es la evidencia de la revisión. Viaja en el mismo commit que el código, o en
  uno de seguimiento si la revisión llega después del merge.
- Sin subagentes (Visual Studio), la sesión de `qa-review` revisa siguiendo la definición de
  `qa-reviewer`. Sigue siendo una sesión distinta de la que implementó.
- `migration-reviewer` sigue en borrador: entra cuando un work item del piloto tenga una migración.

## Alternativas consideradas

- **Revisar en la misma sesión de `wbs-execution`:** la sesión que implementó se revisa a sí
  misma y arrastra su contexto y sus sesgos.
- **Que `qa-reviewer` escriba el informe y corrija:** el revisor y el corrector serían el mismo, y
  habría dos escritores en la carpeta del work item.

## Resultado de la prueba (v0.7.1)

Resultados en `tests/pilots/bonis/RESULTADOS-BLOQUE3.md`:
- La revisión encontró 3 hallazgos bajos reales que la verificación del bloque 2 no vio. Se
  corrigieron con el modo `qa` (PR 14472).
- La ronda 2 verificó las correcciones y encontró QA-04, que se aceptó.

Ajustes:
- La bitácora solo crece.
- El mensaje de commit se escribe entero tras el último cambio.
- El *Resultado* del informe refleja el estado actual.
- Procesos y datos locales de `runtime-tester` en el informe. No se propone cuando el usuario local
  no puede tener el rol que hace falta.
- *Rojo* por mutación cuando la tarea solo añade pruebas.
