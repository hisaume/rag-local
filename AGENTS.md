# rag agent guide

## Sources of truth

### Design documents

Project design documents reside in `docs/design/`:
Read L1-PROJECT.md and L2-DESIGN.md for project intent and architecture. Consult L3-COMPONENTS.md and L4-IMPLEMENTATION.md when relevant to the work.

### Domain context and documentation

Use the terminology and domain invariants in `GLOSSARY.md` when they apply.

## Commands

- Install: `uv sync --locked`
- Check: `./check.sh`
- Test: `uv run --locked pytest`

Run `./check.sh` as the authoritative quality gate. It includes Ruff linting, formatting, mypy and pytest.

Consult actual project tooling before running commands.

## Delivery authority

- Tracker: Beads. See `docs/agents/issue-tracker.md`.
- Do not commit, push, open pull requests, or synchronize an external tracker unless the user explicitly authorizes those actions. Authorization already given for the current task remains valid.

## Project invariants

- _Record only non-obvious constraints that should apply to most changes._
