# EGM Preflight

Every EGM skill reads this file before doing anything else. Skip it when
another EGM skill started you in the same conversation: the caller has
already done it. If an EGM skill started you as a helper in a fresh context
(a worker with `is_worker: true`, a scout, a reviewer, or the synthesizer),
skip steps 1 and 2 and use the files your caller listed (step 3).

1.  **Harness.** When running in Codex or ChatGPT Work, read
    [Codex integration](../docs/codex.md). In Claude Code or Cowork, read
    `${CLAUDE_PLUGIN_ROOT}/docs/claude.md`.

2.  **Languages.** For each row of the table below, run
    `git ls-files -- '<pattern>' | head -n 1` from the repository root
    (outside Git: `find . -name '<pattern>' -not -path '*/.*' | head -n 1`).
    If it prints a file, read that language's profile and follow its
    Preflight section, if it has one, before continuing. When several
    languages match, read each profile; each applies to its own files.

| Language | Pattern | Profile |
| --- | --- | --- |
| Julia | `*.jl` | [Julia language profile](languages/julia.md) |

3.  **Helpers.** Whenever you start a helper in a fresh context, add to its
    prompt the profiles you read and the files their Preflight sections name
    for helpers, in this form: "Language notes and package maps for this
    repository: <paths>. Read or search them when they help your task. Map
    files are long; search them by heading instead of reading them whole."
    Leave this out only where a skill says a helper reads nothing but the
    document (the Comprehension Test in `egm-review`).

To add a language, see `contributing/language_extension.md` in the EGM
repository.
