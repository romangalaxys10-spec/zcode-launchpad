---
description: Draft launch content (changelog, blog, X thread, LinkedIn, Reddit, Product Hunt) from recent git history
allowed-tools: Read, Bash, Write, Edit, Grep, Glob
argument-hint: <ref or date> [audience] [register]
---

Invoke the `launchpad` skill with this input: **$ARGUMENTS**

Arguments: a git ref (tag/commit) or a date like `2026-09-01`, optionally
followed by the audience and register the user wants (e.g. `v1.2 founders
first-person`).

If no arguments are given: ask for the repo range first (default: since the
last tag, `git describe --tags --abbrev=0`), then run the 3-question interview
before drafting. Do not skip the interview to save time; the drafts depend on
it.
