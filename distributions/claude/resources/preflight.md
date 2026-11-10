# EGM Preflight

Every EGM skill reads this file before doing anything else. Skip it when
another EGM skill started you in the same conversation, or when you run as a
worker (`is_worker: true`): the caller has already done it.

1.  **Harness.** When running in Codex or ChatGPT Work, read
    [Codex integration](../docs/codex.md). In Claude Code or Cowork, read
    `${CLAUDE_PLUGIN_ROOT}/docs/claude.md`.

2.  **Julia.** From the repository root, run
    `git ls-files -- '*.jl' | head -n 1` (outside Git:
    `find . -name '*.jl' -not -path '*/.*' | head -n 1`). If it prints a
    file, read the [Julia language profile](languages/julia.md) and follow
    its [EatMe](languages/julia.md#eatme) section before continuing.
