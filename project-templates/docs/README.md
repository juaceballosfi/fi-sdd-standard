# Plantilla de `docs/` del proyecto

`install.py` copia solo lo que no depende del proyecto:

| Archivo | Contenido |
| --- | --- |
| `adr/0000-plantilla.md` | Plantilla de las decisiones de arquitectura del proyecto |
| `sdd/` | Trabajo SDD por work item (ADR-0002) |

Los seis documentos base (`architecture`, `backend`, `database`, `api-reference`, `frontend` y
`reglas-negocio`) los escribe `/project-context` con el contenido real del proyecto (ADR-0021). Sus
plantillas, con los encabezados fijos, están en `core/skills/project-context/templates/docs/`. Se
escriben en español (ADR-0003). `AGENTS.md` los enlaza sin importarlos (ADR-0014).
