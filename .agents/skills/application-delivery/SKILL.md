---
name: application-delivery
description: Plan, implement, validate, and hand off changes in this repository. Use for durable application changes and vertical slices, not read-only inspection.
---

# Application delivery

Use the repository's contracts, vocabulary, and delivery permissions. Focused skills retain ownership of their individual procedures.

## Prepare

1. Read `AGENTS.md` and the relevant design, domain, specification, or ADR documents.
2. If `AGENTS.md` declares a tracker, follow its referenced guidance. Otherwise do not require issue creation, claiming, or closure.
3. Small, understood changes may proceed directly. For substantial features or consequential changes, resolve uncertainty and work in independently testable slices.

## Implement and validate

- Implement behavioural changes test-first at the relevant public boundary.
- Run the repository's authoritative validation command. If none is configured, use justified available checks and report the missing quality gate; never invent a passing result.
- A pull request is not completion until applicable integration gates pass.

## Handoff

- Follow `AGENTS.md` permissions for commits, PRs, and external synchronization.
- Write descriptive commit messages. For a PR, briefly state **purpose**, **relevant contract or issue**, **changes**, **verification**, and **known limitations**. Link to specifications rather than copying them. Keep trivial PRs proportionally short.
- Report changed files, verification results, remaining work, and tracker state if configured.
