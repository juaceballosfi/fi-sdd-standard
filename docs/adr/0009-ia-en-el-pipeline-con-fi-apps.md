# ADR-0009 · IA dentro del pipeline con Fi Apps

- **Estado:** Aceptada (con preguntas pendientes a los administradores de Fi Apps)
- **Fecha:** 2026-10-13
- **Decide:** Juan Ceballos

## Contexto

La propuesta de GitHub Actions usaba un modelo para reescribir el README, pero sin enviarle nada
del repositorio, así que generaba texto inventado. Fi Apps es la plataforma interna, ofrece una API
compatible con OpenAI y hoy no tiene coste extra.

## Decisión

- Un paso no bloqueante del pipeline de PR envía a Fi Apps (modelo Performance) el diff del PR,
  con un límite de tamaño y sin `appsettings*.json` ni `.env`, junto con los work items enlazados.
- Publica un comentario en el PR con un resumen del cambio, un borrador de notas de versión y los
  puntos que conviene revisar. Nunca escribe en una rama.
- Clave: personal de Juan Ceballos en el piloto (opción B); identidad técnica para la extensión
  (opción A). Se guarda como secreto en el grupo de variables `fi-apps-ia`, autorizado solo para
  los pipelines que la usan, y se renueva con aviso dos semanas antes de caducar.
- El script vive en la plantilla del repositorio central, para que un PR no pueda modificarlo.

## Consecuencias

Preguntas pendientes para los administradores de Fi Apps (fase 4):

1. ¿Se puede crear una clave con identidad técnica? ¿Quién la aprueba?
2. ¿Cuál es la caducidad máxima?
3. ¿Hay cuotas por clave?
4. ¿La API es accesible desde fuera de la red corporativa? (crítica)
5. ¿Fi Apps guarda el contenido que recibe?

## Alternativas consideradas

- Azure OpenAI: pago por uso y nueva configuración; descartado por ahora.
- Sin IA en el pipeline: se pierde el resumen para el revisor, sin otro coste.
