# Agent skills collection

## Objective and definition of done

Prepare a reviewable open-source skills collection for Codex and Claude Code, plus Brazilian Portuguese and English articles in the portfolio explaining the engineering methods. Draw on the author's real workflows in CORO SOLTO, research, Ralph Starter, Scanrepo, portfolio, and aeo.js. Generalize the ECDSA collaboration method. The user authorized public repository creation and portfolio article integration on 2026-10-31. Production deployment, npm release, and profile pinning remain separate actions.

Done for this local preparation: portable skills and plugin manifests, source provenance, installation instructions, paired portfolio articles, package validation, useful isolated checks, and a recoverable Git checkpoint. Report structural validation separately from real-agent behavioral validation and public availability.

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

- Branch: `codex/skills-package-20261031`, tracking `origin/main`. Public remote: `https://github.com/rubenmarcus/agent-skills.git`; default branch `main`.
- Implementation checkpoint: `b78f8872a0406132a1ac9dbd374ff85017f9abcc` (`Add portable agent workflows and article draft`). A following documentation checkpoint records this completion state; use `git log -2 --oneline` to recover both.
- Inspected Ralph Starter at `ee9c7946c386bb9cecc4001a052e29ffa53f8f9a` (0.5.2).
- Inspected aeo.js at `9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1` (0.0.17).
- Confirmed Addy Osmani and Matt Pocock's public collections as distribution references, without copying their skills.

## Milestones and validation

1. Source inventory complete. Ralph already ships 9 integration-oriented skills; generalizable methods also live in its executor, validator, session, circuit breaker, swarm, and worktree code.
2. Local collection initialized separately from existing worktrees. No source project or global installation changed.
3. Eleven rewritten skills, their relative references, Codex UI metadata, portable plugin manifest, Claude manifest/marketplace, MIT license, and provenance are present. The shared folders require no custom installer or orchestration runtime.
4. Historical Portuguese draft was moved out of this collection into paired portfolio articles (content key `portable-agent-skills`). Its original text remains recoverable in `b78f887`. The portfolio owns subsequent editorial changes.
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

Public repository creation and push completed on 2026-10-31 at `https://github.com/rubenmarcus/agent-skills`, default branch `main`, initial public revision `6b6af62`. Next: verify CI and a fresh public checkout, finish the paired portfolio article review, then execute the documented behavioral scenarios in disposable tasks on Codex and Claude.

## Deferred work

- Production publication of the portfolio articles, profile pinning, and npm publishing. Public repository creation/push is complete.
- Full Codex and Claude behavioral evaluation on real tasks.
- Scanrepo-specific extraction and a generic bilingual publishing skill can follow once the first package is reviewed.

## Resume milestone: public repo and portfolio articles (2026-10-31)

- Recovered the complete preceding objective and inspected the clean baseline at `3d05053054178d5d9668e98ea0089d81e70044a1`.
- User correction accepted: the article belongs in the portfolio and must have PT-BR and English versions. Retired the draft under `articles/`; Git preserves the original.
- Portfolio isolated branch: `blog/portable-agent-skills-pt-en`, base `6bc75b58bbeebb84ac78b0adc04aeba2f3cd3dd1`. Shared content key `portable-agent-skills`; its project ledger is `docs/agent-skills-article-continuation.md`.
- Prepared English and Brazilian Portuguese READMEs, public Git/Claude marketplace installation, package repository metadata, and CI for structural, hook, and pack checks.
- Checked official Codex discovery and Claude marketplace documentation. Public Git distribution does not imply OpenAI directory listing or a full real-agent evaluation.
- Public remote created and initial code pushed successfully at `6b6af62`. GitHub API confirms `isPrivate: false` and default branch `main`. Initial CI and fresh-clone verification are complete. The portfolio article is in review.

- Resume validation passed: `npm run check` (11 skills, 31 files, 22 unexecuted cases), `npm run check:hook` (syntax, missing scanner, arguments and 0/1/42 exit propagation), and strict Claude marketplace validation. Full current Git history passed gitleaks with 100 percent redaction. Dry-run pack: 42 files, 27,054 bytes before final ledger text.

- Public verification milestone: a fresh unauthenticated HTTPS clone at `b39c0dc` passed `npm run check` and `npm run check:hook`. GitHub Actions runs `41152451560` (`6b6af62`) and `41152471604` (`b39c0dc`) both completed successfully. Public repo page and files were also inspected in Ego Lite.
- Paired portfolio content was committed at `26c8ae3`, with its evidence ledger at `a8e4863`. Both language pages, shared cover and language navigation were exercised locally. The portfolio owns its separate PR and deployment status; this collection does not publish the articles.
