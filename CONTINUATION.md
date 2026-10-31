# Agent skills collection

## Objective and definition of done

Prepare a reviewable open-source skills collection for Codex and Claude Code, plus a Portuguese article explaining the engineering methods. Draw on the author's real workflows in CORO SOLTO, research, Ralph Starter, Scanrepo, portfolio, and aeo.js. Generalize the ECDSA collaboration method. Public publication, npm release, profile pinning, and editing other projects are separate actions.

Done for this local preparation: portable skills and plugin manifests, source provenance, installation instructions, article draft, package validation, useful isolated checks, and a recoverable Git checkpoint. Report structural validation separately from real-agent behavioral validation and public availability.

## Accepted decisions

- One collection with a shared `skills/` source for both agents.
- Core: evidence, adversarial review, gauntlet loops, research, multi-agent coordination, validation, pre-commit, and AEO.
- Rewrite `ecdsafail-multi-agent-collaboration` as generic collaboration; keep domain-specific originals intact.
- Extract general methods from Ralph Starter, rather than duplicating its product-specific integration skills.
- Include AEO using the actual aeo.js API and CLI.
- Exclude personal communication workflows and project-specific cover generation from this collection.
- Third-party suites remain attributed external recommendations unless explicitly reviewed for vendoring.
- New generic prose and examples; no game assets, project source code, credentials, or personal writing profiles are bundled.

## Current state

- Branch: `codex/skills-package-20261031`; repository initialized, no remote configured.
- Inspected Ralph Starter at `ee9c7946c386bb9cecc4001a052e29ffa53f8f9a` (0.5.2).
- Inspected aeo.js at `9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1` (0.0.17).
- Confirmed Addy Osmani and Matt Pocock's public collections as distribution references, without copying their skills.

## Milestones and validation

1. Source inventory complete. Ralph already ships 9 integration-oriented skills; generalizable methods also live in its executor, validator, session, circuit breaker, swarm, and worktree code.
2. Local collection initialized separately from existing worktrees. No source project or global installation changed.
3. Eleven rewritten skills, their relative references, Codex UI metadata, portable plugin manifest, Claude manifest/marketplace, MIT license, and provenance are present. The shared folders require no custom installer or orchestration runtime.
4. Portuguese article drafted at `articles/skills-dos-projetos-para-um-pacote.pt-BR.md`. It explains concrete failure modes, independent review, social research, the three Ralph extractions, and AEO limits. It does not claim a public release or unmeasured results.
5. Structural and executable-example verification passed on 2026-10-31:
   - `npm run check`: 11 skills, 31 skill files, metadata, local references, manifests, package entries, and 22 explicitly unexecuted behavioral cases.
   - Skill creator `quick_validate.py`: 11/11 passed, using an isolated `uv run --with pyyaml` environment. System Python lacked PyYAML; no global dependency was installed.
   - `npm run check:hook`: shell syntax, unavailable scanner, exact staged/redacted arguments, and scanner exit codes 0/1/42 passed with a fake scanner. This verifies plumbing, not gitleaks detection quality.
   - `claude plugin validate . --strict --json` and `claude plugin validate .claude-plugin/plugin.json --strict --json`: marketplace and plugin passed without warnings.
   - `node scripts/check-aeo.mjs <clean-aeo-source-checkout>`: compiled the pinned source into a temporary directory, generated CLI output, parsed the local JSON audit, exercised the documented Astro adapter options, preserved existing robots/sitemap, and checked served canonical, parseable JSON-LD, and discovery files. This was a synthetic adapter lifecycle fixture, not a real Astro build or deployment. Source was unchanged.
   - aeo.js package metadata 0.0.17 and printed version 0.0.14 differ at the inspected revision. Both are recorded in the reference and article.
   - `npm pack --ignore-scripts`: 41 files; skill references and manifests included, article/ledger and source-specific fixture runner excluded. Extracted the tarball to a temporary directory and reran structural and hook checks there successfully. No third-party runtime dependencies or install scripts.
   - Local package: `artifacts/rubenmarcus-agent-skills-0.1.0.tgz`, 23,997 bytes, SHA-256 `f86037b525aafdeb143a28618fc9eeab729ede108391c3d762f29031f75bb5c5`. This generated tarball is ignored by Git; rebuild with the documented pack command if needed.
   - `git diff --cached --check` passed. `gitleaks protect --staged --redact=100 --no-banner --no-color` scanned about 83.6 KB and reported no leaks. No machine-local source paths or excluded personal skill names appear in the tracked text.
   - npm was initially invoked under the shell's Node 16 and warned about its supported range. Checks were rerun under Homebrew Node 26.12.1; use Node 20+ as documented.

## Next concrete step

Create the scoped Git checkpoint and record its SHA here. Before any public release, review the collection and article, run real-agent evaluations, confirm the destination, and replace local-preview wording only when publication actually happens.

## Deferred work

- Public repository creation/push, article publication, profile pinning, and npm publishing.
- Full Codex and Claude behavioral evaluation on real tasks.
- Scanrepo-specific extraction and a generic bilingual publishing skill can follow once the first package is reviewed.
