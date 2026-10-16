# Project context — [Nombre del proyecto]

**Generado con:** project-context v3.9 · [Claude Code | GitHub Copilot | Codex] · [modelo] · [AAAA-MM-DD]
<!-- sdd:context · [AAAA-MM-DD] · fuentes: [archivos de los que salen los datos: *.csproj, package.json, lockfile, pipeline…] -->

<!-- Fixed headings (ADR-0021): skills and agents look for them by name. Instructions in English
     (ADR-0003). Budget: about 120 lines for this section (the file never over 200); the number after each heading below is its
     maximum. Whatever does not fit goes to docs/ with a link. -->

## What this is
<!-- max 6 lines. 2-4 lines: product, users, deployment name, how the solution is laid out. -->

## Commands
<!-- max 22 lines. Exact commands, verified by running them: restore, build, run (backend and the
     frontend dev server), tests (all · one class · one test), lint, type check, migrations. Tool
     versions: SDK, Node and package manager, locally and in CI when they differ. Then: what CI
     runs, if it differs. -->

## Local run
<!-- max 14 lines. Debug vs Release switches, local user and roles, services to start (docker-compose), URLs,
     what an agent can and cannot check at runtime. -->

## Architecture
<!-- max 15 lines. Layers and dependency direction, where new code goes, rules enforced by tests.
     Details: docs/architecture.md, docs/backend.md, docs/frontend.md. -->

## Authorization and errors
<!-- max 12 lines. Mandatory pattern for new endpoints; the error contract the frontend depends on. -->

## Data
<!-- max 8 lines. Database and ORM, configuration pattern, migration workflow, transactions, other stores.
     Details: docs/database.md. -->

## Tests
<!-- max 14 lines. Backend: framework, location, conventions, how to run one test.
     Frontend: runner, location, what can and cannot be tested.
     Type check, if the build does not do it.
     Baseline (date): warnings, failing tests, type errors that already exist. -->

## Internationalization
<!-- max 14 lines. Translation files, languages read from the files, key convention, generated or hand-edited,
     how frontend and backend use them, how a new key is added. N/A if none. -->

## Protected paths
<!-- max 5 lines. Submodules, generated code, folders agents must never edit. -->

## Branches, CI and commits
<!-- max 8 lines. Branch model, what each branch or tag deploys, commit format (.gitmessage, ADR-0004). -->

## Documentation
<!-- max 4 lines. Where docs live: docs/*.md, docs/adr/, docs/sdd/, DocFX or other site, README. -->
