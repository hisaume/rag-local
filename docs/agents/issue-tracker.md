# Issue tracker

Beads is the durable work tracker. Follow `AGENTS.md` for delivery authority and the project-local `application-delivery` skill for implementation and validation gates.

- Inspect context: `bd prime`
- Create work: `bd create "<title>" -t task`
- Inspect work: `bd show <id>`
- Find unblocked work: `bd ready`
- Claim work: `bd update <id> --claim`
- Record a blocker: `bd dep add <blocked-id> <blocker-id>`
- Close verified work: `bd close <id>`

`bd ready` establishes dependency readiness, not approval or specification completeness. Close issues only after the repository's completion gates pass.
