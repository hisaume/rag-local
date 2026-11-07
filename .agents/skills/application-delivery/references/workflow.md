# Beads workflow

## Start durable work

1. Run `bd prime`.
2. Find work with `bd ready`, inspect it with `bd show <id>`, and claim it with `bd update <id> --claim`.
3. Record follow-up work and dependencies in Beads.
4. Close an issue only after its repository-defined completion and integration gates pass.

## Deliver work

1. Run the repository's authoritative validation command. If it is unconfigured,
   run checks justified by actual project tooling and report the missing quality
   gate; do not invent commands or claim checks passed without execution.
2. Follow the commit, pull-request, and synchronization authority in
   `AGENTS.md`.
3. Hand off changed files, validation, remaining work, and tracker state when a
   tracker is configured.
