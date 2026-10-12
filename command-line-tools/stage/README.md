# Advanced Tooling: stage

Build this directory as the Docker context. Run `hatch run dev:check` and
`hatch run test:test` with Python 3.12. Runtime and development requirements
are installed from separate hash locks. The Rocky runtime uses UID/GID 2000.
This distribution fixes the dependency environment for the upstream
`stac-asset` CLI; no replacement staging implementation is introduced.
