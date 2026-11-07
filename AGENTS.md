# rag agent guide

## Sources of truth

### Design documents

Project design documents reside in `docs/design/`:
Read L1-PROJECT.md and L2-DESIGN.md for project intent and architecture. Consult L3-COMPONENTS.md when relevant to the work.

### Context and documentation

Use the terminology and domain invariants in `GLOSSARY.md` when they apply.

## Commands

- Install: `uv sync --locked`
- Check: `./check.sh`
- Test: `uv run --locked pytest`

Run `./check.sh` as the authoritative quality gate. It includes Ruff linting, formatting, mypy and pytest.

Consult actual project tooling before running commands.

## Project invariants

- _Record only non-obvious constraints that should apply to most changes._

## Delivery authority

- Beads is selected for durable work. Run `bd prime` to verify availability before tracker operations; do not use markdown TODO files as the project tracker.
- For tracker operations, read `docs/agents/issue-tracker.md`.
- Do not commit, push, open pull requests, or synchronize an external tracker unless the user explicitly authorizes those actions. Authorization already given for the current task remains valid.

## Planning skills

For `grill-with-docs`, `to-spec`, and `to-tickets`, read
`docs/agents/planning.md`. Follow the repository's tracker, domain
documentation, and delivery authority.
