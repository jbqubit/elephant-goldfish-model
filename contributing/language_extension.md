# Adding Support for a Language

This guide explains how EGM handles programming languages, where
language-specific behavior lives, how to add a language, and what to test
before you open a pull request. The Julia profile is the worked example.

## How Language Support Works

EGM's skills are written to be language-neutral. Language knowledge enters in
three places:

1.  **The preflight** ([`resources/preflight.md`](../resources/preflight.md)).
    Every skill reads it first. Its table maps each supported language to a
    file pattern and a profile. When the repository holds a matching file, the
    skill reads that language's profile before it starts work.
2.  **The language profile** (`resources/languages/<language>.md`). One file
    holds everything a skill needs to know about the language: how to
    recognize its files, how projects are laid out, how tests run, how to find
    definitions and the public interface, what the agent must never change,
    and notes for each skill. Where a profile and a skill disagree about that
    language, the profile wins, so most language rules belong in the profile,
    not in the skills.
3.  **A few rules inside `egm-bootstrap`** that run before any profile is
    read, chiefly the list of source file extensions (see the next section).

A profile can also name a **synopsis tool**: a program that reads the code the
way the language's own tools do and writes one file that serves as the map of
a package. For Julia this is [EatMe.jl](https://github.com/brittonlab/EatMe.jl),
which writes `EatMe.jl.md`. See [Synopsis Tools](#synopsis-tools).

## Where Language-Specific Behavior Lives

| File | Section | What it holds | Change it when adding a language? |
| --- | --- | --- | --- |
| `resources/preflight.md` | **Languages** table | Language, file pattern, profile link | Yes: add a row |
| `resources/languages/<language>.md` | whole file | The profile | Yes: new file |
| `skills/egm-bootstrap/SKILL.md` | Step 2, item 3, *Source Code Files* | Extensions that count as source when pruning folders | Yes: add the extensions |
| `skills/egm-bootstrap/SKILL.md` | Step 0 | Build manifest to test command (`Cargo.toml` to `cargo test`, ...) | Optional; the profile's Tests section can supply this instead |
| `skills/egm-bootstrap/SKILL.md` | Step 2, item 1 | Build manifests kept during discovery | Optional, as above |
| `skills/egm-bootstrap/SKILL.md` | Step 2, item 3, *Test Directory Exclusion*; Step 4, *Scout Constraints* | Test folder names, entry-point names (`main.*`, `__init__.py`, ...), test file patterns | No: override them in the profile's Skill Notes |
| `skills/egm-bootstrap/references/unsupported-source-check.md` | whole file | Warns about code-like extensions missing from *Source Code Files* | No: it reads the list above |
| `resources/execution_instructions.md` | Design-Only Scope | Example code extensions the design skills must not create | No: the examples end with "or any other code files" |
| `scripts/pack_plugin.py` | `REQUIRED_SHARED` | Files every package must contain | Yes: add the profile |
| `resources/README.md` | list | Index of shared resources | Yes: add the profile |

No other skill branches on language. If you find yourself editing a second
skill file, put the rule in the profile's Skill Notes instead.

## Writing a Profile

Start the file with `# <Language> Language Profile` and a short paragraph
that links back to the preflight (`../preflight.md`). A unit test
(`tests/unit/test_language_profiles.py`) checks the title, the link, and the
two required sections.

| Section | Required | Contents |
| --- | --- | --- |
| Recognize | yes | Source extensions, project and manifest files (and how to tell them from other tools' files of the same name), lockfiles, and generated files to ignore |
| Preflight | no | Steps every skill runs before starting, such as running a synopsis tool |
| Layout | recommended | The conventional folders and entry points, and what is *not* a unit (for example, in Julia a folder is not a module) |
| Tests | recommended | Where tests live, the command, and whether running it changes files |
| Dependencies | recommended | Where direct, optional, and test-only dependencies are declared |
| Definitions and Search | recommended | Definition keywords, how to find every definition of a name, and where to split long files |
| Interface | recommended | What makes a name public, re-exports, extension points, and what counts as a breaking change |
| Documentation as Evidence | recommended | Docstring and documentation conventions; code wins over docs |
| Environment Safety | recommended | Files and commands the agent must never touch or run in the project's own environment |
| Verification Tools | recommended | Tools that ship with the language, before any third-party tool |
| Skill Notes | yes | One subsection per skill that needs language-specific behavior |

Write rules an agent can follow without judgment calls. Give commands it can
copy. Say "record the command; do not run it" wherever running a command
would change files. Never tell an agent to edit a project's manifests or
environment.

## Synopsis Tools

A synopsis tool is optional, but for a language that agents read poorly as
text it can matter more than the profile itself. If a profile relies on one,
its Preflight section must say how to:

1.  **Find the tool**, for example from an environment variable, and what to
    do when it is missing: tell the user and fall back to the profile's text
    rules.
2.  **Check freshness** before regenerating. The output should record the
    commit it was built from, and the tool should report whether it is
    current. EatMe.jl does both: the first line of `EatMe.jl.md` records the
    commit, and `scripts/eatme check` compares it with the package's tracked
    source.
3.  **Ask before running the project's code.** Loading or building a package
    runs it and can download dependencies.
4.  **Write the output beside the package's manifest**, as EGM's own outputs
    sit in the repository, and never change any other file.
5.  **Read the output** before the source, trusting it in proportion to its
    provenance labels.
6.  **Hand it to helpers.** Name the files that the preflight's Helpers step
    passes to workers, scouts, and reviewers, since they start in a fresh
    context and cannot see what the calling skill read. Keep the output
    searchable by heading, and split rarely needed detail into a second file
    (EatMe.jl writes `EatMe.jl.md` and `EatMe.jl.index.md`).

## Steps

1.  Write `resources/languages/<language>.md` (see [Writing a Profile](#writing-a-profile)).
2.  Add its row to the Languages table in `resources/preflight.md`.
3.  Add its source extensions to *Source Code Files* in
    `skills/egm-bootstrap/SKILL.md`.
4.  Add the profile to `REQUIRED_SHARED` in `scripts/pack_plugin.py` and to
    `resources/README.md`.
5.  Add test scenarios (see [Testing](#testing)).
6.  Regenerate the Claude package:
    `python3 scripts/pack_plugin.py --target claude --output <dir>`, then
    replace `distributions/claude` with the generated `egm-claude` folder.
7.  Run the tests and the manual checks below.

## Testing

Before opening a pull request:

*   **Unit tests.** `pytest tests/unit` passes (see [TESTING.md](../TESTING.md)).
    Among others, this checks the profile's shape and registration, relative
    links, that the packaged copy is current, and that each skill stays under
    Antigravity's 24,000-byte limit.
*   **Scenarios.** Add at least one scenario to
    `skills/egm-bootstrap/test_scenarios.yaml` in which a tree of the new
    language's files is bootstrapped without an unsupported-source warning and
    with the profile's test command as the Verification command.
*   **Real repositories.** Run `/egm-bootstrap` and one design skill
    (`/egm-draft` or `/egm-review`) on at least two real repositories in the
    language with different layouts (for example a single package and a
    repository with several packages or mixed languages), and on one
    repository without the language, where the preflight must not read the
    profile. If the profile uses a synopsis tool, also exercise its missing,
    current, and stale paths.
*   **Record the results** in the pull request's Verification section: each
    repository and commit, what the preflight did, the files written, and
    anything that went wrong.

A new language changes how every skill behaves on that language's code, so
treat it as a feature: open a Feature Inquiry before writing the profile (see
[CONTRIBUTING.md](../CONTRIBUTING.md)).

## Worked Example: Julia

| Step | Change |
| --- | --- |
| Profile | [`resources/languages/julia.md`](../resources/languages/julia.md): `Project.toml` recognition, `src/<Name>.jl` entry point, `test/runtests.jl`, method tables instead of single definitions, `export` and `public`, and skill notes |
| Preflight row | Julia, `*.jl` |
| Bootstrap | `.jl` added to *Source Code Files* |
| Synopsis tool | EatMe.jl: `scripts/eatme check`, `prepare`, `finish`, and `prompts/run.md` for the host; output `EatMe.jl.md` beside `Project.toml` |
