# Issue tracker

Beads is the durable tracker for this project. `AGENTS.md` governs permission
for commits, publishing, and remote synchronization.

- Inspect context: `bd prime`
- Create work: `bd create "<title>" -t task` (choose another issue type when appropriate)
- Read an issue: `bd show <id>`
- Add a blocking edge: `bd dep add <blocked-id> <blocker-id>`
- Find unblocked work: `bd ready`
- Claim work: `bd update <id> --claim`
- Close verified work: `bd close <id>`

`bd ready` proves only that blockers are cleared; readiness for implementation
also requires a sufficiently specified issue. The `application-delivery` skill
owns planning, validation, and completion gates.
