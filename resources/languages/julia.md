# Julia Language Profile

The [preflight](../preflight.md) sends every EGM skill here when the
repository contains Julia code. Follow [Preflight](#preflight) first. The
shared sections apply to every skill; the last section adds notes for each
skill. Where this profile and a skill disagree about Julia specifics, follow
this profile.

## Recognize

*   **Source**: files ending in `.jl`. A `.jl` file whose first line is
    `### A Pluto.jl notebook ###` is a notebook; treat it as an example, not as
    package source.
*   **Project file**: `JuliaProject.toml`, or `Project.toml` when no
    `JuliaProject.toml` is beside it (Julia prefers `JuliaProject.toml`).
    Other tools also use the name `Project.toml`, so treat one as Julia's only
    if it has a `uuid`, a `[deps]` table whose values are UUIDs, or
    `julia = ...` under `[compat]`. Its `name` is the package name.
*   **Lockfiles and metadata**: `Manifest.toml`, `JuliaManifest.toml`,
    `Manifest-v*.toml`, and `Artifacts.toml`. Treat them as configuration,
    never as source or interface.

## Preflight

[EatMe.jl](https://github.com/brittonlab/EatMe.jl) loads a Julia package and
writes `EatMe.jl.md` beside its project file: the public interface, every
method, the methods it adds to other packages' functions, invariants, side
effects, tests, and an internal index, with each description labeled by its
source. EGM relies on it as the map of each Julia package; the text rules in
the rest of this profile are for checking it and for working without it.

1.  **Find the packages.** Each Julia project file (see
    [Recognize](#recognize)) with both a `name` and a `uuid` is a package.
    Environments such as `docs/`, `test/`, and `benchmark/` have no `uuid`;
    skip them.
2.  **Find EatMe.** Use the folder named by the `EATME_JL` environment
    variable. If it is unset or has no `scripts/eatme`, tell the user that
    EatMe is not available, then continue with the text rules below and say
    in your output that the package map was built without EatMe.
3.  **Run it.** For each package, follow `$EATME_JL/prompts/run.md`. It
    checks whether `EatMe.jl.md` is current and asks the user before loading
    the package. Do this once per package per conversation.
4.  **Read it.** Read `EatMe.jl.md` before the package's source. Read the
    sections before the Internal Index in full; read the Internal Index only
    for the files you work on. Treat descriptions labeled *inferred* or
    *unclear* as leads to check in the code, not as facts. If the file is
    stale, say so and check its claims against the code. `EatMe.jl.md` is
    generated output: never treat it as source, and do not edit it.

## Layout

| Path | Role |
| --- | --- |
| `src/<Name>.jl` | Entry point. Defines `module <Name>`, its `include`s, and its `export` and `public` names. `<Name>` comes from the project file, not from the folder name `src`. |
| `src/**/*.jl` | Files `include`d into a module. A folder is not a module. |
| `ext/` | Package extensions. `[weakdeps]` lists the optional packages; `[extensions]` maps each extension to the packages that load it. |
| `test/` | Tests (see [Tests](#tests)). |
| `docs/make.jl`, `docs/src/` | Documenter build script and documentation pages. |
| `benchmark/` | Benchmarks. |
| `lib/<Sub>/Project.toml` | A subpackage in a monorepo, with its own entry point and tests. |

## Tests

*   Tests live in `test/` (singular). `test/runtests.jl` is the entry point and
    `include`s the other test files; `@testset` blocks group the tests.
*   Test-only dependencies are listed under `[extras]` and `[targets]` in the
    project file, in `test/Project.toml`, or in both; read both.
*   Command, run from the folder of the nearest project file:
    `julia --project=. -e 'using Pkg; Pkg.test()'`. Coverage:
    `Pkg.test(coverage=true)`.
*   Record the command; do not run it unless the user asks. `Pkg.test()`
    writes a `Manifest.toml` into a project that lacks one.
*   Treat `test/` as a test-only directory, like `tests/` in other languages.
    This rule applies to Julia projects only.

## Dependencies

*   The project file lists direct dependencies under `[deps]`, optional ones
    under `[weakdeps]` (loaded through `[extensions]`), and test-only ones as
    described in [Tests](#tests). Reading these needs no Julia.
*   The full resolved list, including indirect dependencies, comes from
    `Pkg.status(mode = Pkg.PKGMODE_MANIFEST)` or `Pkg.dependencies()` run in a
    temporary environment; `EatMe.jl.md` lists it under Dependencies.
    Resolving the project's own environment writes a `Manifest.toml`. The resolved list
    contains neither optional nor test-only dependencies.

## Definitions and Search

*   **Definitions**: `module`, `function`, `macro`, `struct`,
    `mutable struct`, `abstract type`, `primitive type`, `const`, `@enum`,
    `@kwdef struct`, and one-line methods such as `area(c::Circle) = pi * c.r^2`.
*   **Functions are method tables.** One function can have methods in many
    files and modules. To find all of `f`, search for `function f(`, for lines
    starting with `f(` that contain ` = `, and for qualified definitions such
    as `function Base.f(` and `Base.f(`. Check every method's argument types
    before saying a method exists or is missing.
*   **Counting methods**: text search finds where methods are defined, not
    how many exist. A definition with optional positional arguments, such as
    `f(x, tol=1e-8)`, creates one method per number of arguments; keyword
    arguments add a hidden entry point; and every `struct` gets default
    constructors. Do not state a method count from text search alone; read
    the signatures, or take the count from `EatMe.jl.md`.
*   **Imports**: `using M`, `using M: a, b`, `import M: f` (needed to add
    methods to `f` without qualifying it), and `include("path.jl")`, which
    pastes a file into the current module.
*   **Splitting long files**: split at top-level `function`, `macro`,
    `struct`, `abstract type`, and `module` lines, and keep each docstring
    with the definition below it.

## Interface

*   **Public names** are those listed in `export` or, from Julia 1.11, in
    `public` inside the module that owns them, usually in `src/<Name>.jl`.
    Before calling a name in an `include`d file public, check the owning
    module's `export` and `public` lines.
*   **Re-exports**: a module can export a function it imported from a
    dependency, such as `CommonSolve.solve`. The name is part of the
    interface, but the contract lists only the methods this package adds and
    names the package that owns the function.
*   **Methods added to other modules' functions** (for example
    `Base.show(io::IO, x::T)` or `Base.getindex`) are part of the contract.
    List them by function and argument types. This includes methods added to
    another module's internal functions, such as
    `Base.replace_in_print_matrix`; mark those as extending an internal API,
    because the owning module can change it without notice. Text search
    cannot tell whether such a function is public; `EatMe.jl.md` marks it.
    Adding methods to another
    module's function for another module's types is type piracy; report it.
*   **Abstract types** often define informal interfaces (subtypes must
    implement certain functions). Record such a rule as an invariant only when
    the code or a docstring states it.
*   **Breaking changes**: removing or renaming an exported or public name,
    removing a method, or narrowing argument types breaks users. Under
    semantic versioning that needs a new major version, or a new minor
    version before 1.0.

## Documentation as Evidence

Docstrings (string literals directly above a definition, or `@doc`),
Documenter pages under `docs/src/`, and `README.md` describe intent. Use them
as evidence, but the code wins when they disagree; report the disagreement
instead of repeating the claim. `jldoctest` blocks are examples that
Documenter runs.

## Environment Safety

*   Do not create or edit `Project.toml`, `JuliaProject.toml`, or any
    manifest anywhere in the source tree.
*   Do not run `Pkg` commands that change an environment (`add`, `rm`,
    `update`, `develop`, `compat`, `instantiate`, `resolve`) in the project's
    environment.
*   For experiments, use a temporary environment outside the tree:
    `Pkg.activate(; temp=true)` or `julia --project=$(mktemp -d)`.

## Verification Tools

Prefer what ships with Julia:

| Purpose | Built-in tool |
| --- | --- |
| Unit tests | `Test`, run with `Pkg.test()` |
| Coverage | `Pkg.test(coverage=true)` or `julia --code-coverage` |
| Build | `Pkg.precompile()` |
| Performance | `@time`, `@allocated`, and the `Profile` standard library (`@profile`, `Profile.Allocs`) |
| Type stability | `@code_warntype` from `InteractiveUtils` |
| Logging | `Logging` (`@info`, `@debug`) |

Name a third-party tool (for example Aqua.jl, JET.jl, BenchmarkTools.jl, or
Documenter.jl) only when the project already depends on it, as shown by its
project file, `test/Project.toml`, or `docs/Project.toml`.

## Skill Notes

### egm-bootstrap

*   Count `.jl` as a source extension and keep Julia project files with the
    other manifests.
*   Use the [Tests](#tests) command as `VerificationCommand`, taken from the
    nearest project file for each package and subpackage.
*   Read `src/<Name>.jl` first. For a folder of `include`d files, read the
    owning module file before deciding which names are public.
*   Document each package extension in `ext/` as a component and name the
    packages that load it.
*   Treat `docs/` and `benchmark/` as tooling, not components, unless the user
    asks to include them.
*   Build the Interface, Invariants, and Side Effects sections of each
    package from its `EatMe.jl.md` (see [Preflight](#preflight)). Without
    one, use the text rules above and say so in the contract.

### egm-brainstorm

Add these Julia questions to the lenses:

*   **Migration & Backward Compatibility**: Does the change remove or rename
    an exported or public name, or change method signatures? Which `[compat]`
    bounds and version bump does it need?
*   **Cost, Quota & Token Economics**: Is the new code type-stable? What does
    it allocate? Does it add load or compile latency?
*   **Long-Term Tech Debt & Maintenance**: Does it risk type piracy or method
    ambiguities? Should an optional dependency be a package extension?
*   **UX & Developer Ergonomics**: Does the API extend existing generic
    functions where users expect it, instead of adding new names?
*   **Observability & SRE Debuggability**: Does it log through `Logging`?

### egm-draft

*   Describe the Technical Plan in terms of modules, types, generic functions,
    and methods with their argument types.
*   List target files with the `include` line that adds each new file to its
    module, and the test file that `test/runtests.jl` must `include`.
*   Write the Verification Plan with the [built-in tools](#verification-tools)
    and the [test command](#tests); state performance requirements in terms
    of `@time` or `@allocated` measurements.

### egm-review and egm-review-loop

Reviewers apply the [Interface](#interface) and
[Definitions and Search](#definitions-and-search) rules. In particular, flag
changes to exported or public names without a version plan, methods added to
other modules' functions for types the package does not own, and claims of
type stability or performance without a measurement plan.

### egm-resolve

Before accepting or rejecting a finding that says the document contradicts
the code, search for every method of the function involved as described in
[Definitions and Search](#definitions-and-search).

### egm-drift-report

*   Locate every method of each documented function, including qualified
    definitions such as `Base.f`.
*   For the Incomplete Models check, compare documented fields with each
    `struct` definition.
*   Report documented exports that the module no longer exports or defines.
*   Report methods added to other modules' functions, internal ones
    included, that the documentation omits.
*   Use a current `EatMe.jl.md` (see [Preflight](#preflight)) to confirm
    exports and the methods added to other modules' functions.
