---
name: application-delivery
description: Plan and deliver durable changes in this application repository. Use when shaping approved work, claiming tracked work, implementing a vertical slice, or preparing handoff; do not use for an informational or read-only inspection.
---

# Application delivery

Use this repository's domain language, specifications, and delivery authority.
This workflow coordinates durable work; focused skills retain ownership of
their individual procedures.

## Read what the task needs

1. Read `AGENTS.md`.
2. Read `GLOSSARY.md` when domain vocabulary or invariants matter.
3. Read relevant ADRs and `docs/specs/README.md` before changing consequential
   behaviour.
4. For durable Beads work, read `references/workflow.md`.

## Route the work

- Clarify consequential product or domain uncertainty before implementation.
- For small, well-understood changes with bounded impact, work directly from the
  request and existing contracts; do not create a specification or vertical-slice
  plan solely because those artifacts are absent. Examples include a focused bug
  fix, a local refactor, or a documentation correction.
- Use specifications and independently valuable vertical slices for substantial
  features, consequential contract changes, or work spanning multiple concerns.
  Escalate uncertainty or risk even when the implementation is small.
- Implement behavioural changes test-first at the relevant public boundary.
- Run the authoritative validation command before handoff. If it is unconfigured,
  use checks justified by the actual project and report the missing quality gate;
  never invent a command or claim an unperformed check passed.

## Boundaries

- Keep durable state in Beads; temporary execution notes are not a project tracker.
- A pull request is not completion unless this repository's policy says the
  required integration gates have passed.
- This skill never expands the authority stated in `AGENTS.md`.
