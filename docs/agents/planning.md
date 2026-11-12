# Planning Workflow

## Overview

Use this workflow for substantial application development or consequential changes that warrant formal specifications and implementation tickets; small, well-understood changes should follow the normal delivery workflow.

## Skills and sources

- Use `GLOSSARY.md` for domain vocabulary and relevant ADRs under `docs/adr/`
  for durable architectural decisions. Read other design documents according
  to `AGENTS.md`. Create glossary entries and ADRs only when justified.

## Tracker mapping

Beads is the authoritative tracker for specifications and tickets. Read
`docs/agents/issue-tracker.md` for commands and `AGENTS.md` for delivery
permissions.

- **Specification:** Publish the full spec as a Beads epic. Record its issue ID
  in `docs/specs/README.md` as the current contract; retain references to
  superseded specifications in its historical record. Do not duplicate the
  full specification in the index.
- **Tickets:** Publish one Beads task per approved vertical slice. When derived
  from a specification epic, create it as that epic's child. Record blocking
  dependencies with `bd dep add <blocked-id> <blocker-id>`.
- **Approval label:** `ready-for-agent` means the specification or ticket was
  approved for its next agent handoff. Apply the literal Beads label with
  `bd label add <id> ready-for-agent` after the corresponding review. When
  creating children of a labelled epic, use `--no-inherit-labels` and label
  approved tickets explicitly.
- **Work selection:** `bd ready` checks blocking dependencies, not approval.
  Implementation work must also be an approved, sufficiently specified task;
  a specification epic is not an implementation task.

The project-local `application-delivery` workflow governs implementation,
validation, and completion. Planning skills do not supersede its gates.
