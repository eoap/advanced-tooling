# Advanced Tooling: norm_diff

Build this directory as the Docker context. Run `hatch run dev:check` and
`hatch run test:test` with Python 3.12. Runtime and development requirements
are installed from separate hash locks. The Rocky runtime uses UID/GID 2000.
The installed command is `norm-diff-advanced`; existing CWL
`python /app/app.py` commands remain compatible.
