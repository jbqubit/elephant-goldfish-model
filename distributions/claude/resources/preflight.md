# EGM Preflight

Every EGM skill reads this file before doing anything else. Skip it when
another EGM skill started you in the same conversation, or when you run as a
worker (`is_worker: true`): the caller has already done it.

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

To add a language, see `contributing/language_extension.md` in the EGM
repository.
