# Plantillas de Azure Pipelines (fase 4)

Se crearán a partir de los pipelines reales de Bonis y Calls4Grants. Primero se pasa a plantillas lo
que ya funciona, sin cambiar su comportamiento; después se añade lo que falta.

| Plantilla | Qué hará |
| --- | --- |
| `app-k8s.yml` | CI/CD actual: build, pruebas, imagen y despliegue a Dev (opcional), Staging y Prod |
| `steps/build-dotnet-spa.yml` | Restauración con feed privado, build y pruebas de .NET + SPA |
| `stages/deploy-k8s.yml` | Despliegue a un entorno: grupo de variables de Consul, namespace y *environment* |
| `pr-validation.yml` | Validación de PR: build, pruebas, lint, seguridad, formato de commit y reglas del estándar |
| `steps/ai-pr-summary.yml` | Paso no bloqueante con Fi Apps: resumen y notas de versión como comentario del PR (ADR-0009) |
