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

- Current authorized follow-up (2026-10-31): correct the paired article heading to `Comecei pelos modos de erro`, make installation of one selected skill clear for both clients, update both READMEs, open PRs and merge after scoped checks. The user explicitly authorized both PR creation and merge before leaving.
- Collection branch: `docs/skill-by-skill-install-20261031`, baseline public main `8068d0fc537c7c1b380f9704ac5ce88873538e6d`. Remote: `https://github.com/rubenmarcus/agent-skills.git`.
- Paired portfolio branch: `blog/skill-by-skill-install-20261031` in `../portfolio-agent-skills`, baseline main `d65c4ed2bd30149498f0c02caee07ab6e172bc8b`. PR #39 has already merged and both article routes were verified in production. Preserve the unrelated dirty original portfolio checkout.
- Installation scope: one project skill using optional Vercel `skills` CLI or manual whole-folder copies. Claude's full 11-skill plugin remains an explicit optional bundle. No global skills, hooks or plugins are activated.
- Current local verification artifacts: `artifacts/pilot-runs/skill-by-skill-20261031/` (ignored). Final merged SHAs, PRs, CI and production evidence will be recorded in `FINAL-STATE.md` there. Portfolio owns its paired article ledger and browser evidence.
- Original implementation checkpoint: `b78f8872a0406132a1ac9dbd374ff85017f9abcc`. Source revisions and pilot outcomes below are historical validated milestones, not the current branch state.

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

Validate the exact README copy commands and selective CLI installation in disposable projects, run collection checks and review the affected diff. Open the collection PR and the paired portfolio PR, request current-head review, merge verified heads using the user's authorization, then verify CI and public article routes. Record final identifiers in the ignored completion checkpoint above.

## Deferred work

- Profile pinning and npm publishing. Portfolio articles were published through PR #39; this follow-up authorizes their correction and publication.
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

## Editorial follow-up: title and practical examples (2026-10-31)

- User accepted the collection and requested the article title `The skills I use in every project`, plus examples of where to use every skill in the README. PT-BR title: `As skills que uso em todos os projetos`.
- Collection baseline: `851ccbcfad20bcf936e7de40d87309b49f41f064`. Added 11 concrete scenarios, copyable prompts, and expected artifacts to each README, with direct links from the workflow catalog. Examples remain trial tasks, separate from completed behavioral evaluation.
- Scenarios distinguish review, measured improvement rounds, tracing a dashboard count, calibrating a checkout gate, library retry research, peer-agent hypothesis resolution, planning invitations, webhook implementation, isolated cache candidates, staged scanning, and bilingual site discovery.
- Focused structural validation passed: 11 skills, 31 skill files, manifests, links, and 22 unexecuted evaluation cases. No skill instructions, executable examples, manifests, or hook configuration changed.
- Portfolio title, descriptions, and both localized social cards updated in its isolated worktree. Existing filenames and language routes remain stable. Portfolio validation and PR #39 own that part of the follow-up.
- Read-only adversarial review covered both READMEs against all 11 skill contracts and both article metadata/social cards; no actionable findings. Portfolio Astro check passed with 0 errors and 0 warnings. Ego Lite verified the new titles, language switch, canonical/OG metadata, and no page overflow at desktop 1500 and mobile emulation 390.
- The follow-up checkpoint contains only both READMEs and this ledger; recover its SHA from `git log -1`. Next: verify its public `main` CI after push. Keep production publication and behavioral evaluation as separate follow-up work.

## Authorized positioning and pilot comparison (2026-10-31)

- User accepted the comparison recommendation: keep the 11 personal workflows, emphasize AEO and Gauntlet, link complementary Matt Pocock/Addy Osmani workflows, and run three same-task comparisons with and without the selected skill before expanding the catalog.
- Start revisions: collection `5f0b743`; portfolio `56d1b79`, PR #39. Both revisions' CI passed. Existing unrelated checkouts remain excluded.
- Definition of done: paired README/article positioning, a frozen three-case protocol, six isolated agent executions, evidence-backed results including ties/failures, scoped checks, review and recoverable pushed checkpoints. A pilot does not complete the 22-case Codex/Claude evaluation plan or establish a ranking against upstream collections.
- Next: freeze fixtures and rubrics before any scored execution. Use one installed client/model and matching tools/settings in each pair. Store raw local traces outside the public package; publish only synthetic inputs, reproducible checks and reviewed summaries.

- Pilot protocol prepared in `evals/pilot/`: `quality-gates`, `gauntlet-loop`, and `aeo`, one baseline and one skill-text-injected session each. Same Claude Code 2.1.280 / claude-opus-5-5[1m], medium effort, safe/restricted mode, no MCP or child agents, independent copies, at most two target processes, 240 seconds and reported USD 2 API-budget accounting per execution. Full native routing and all 22 planned cases remain outside this pilot.
- Calibration exercises known-defective inputs and independent reference corrections before scored runs. It caught a baseline metadata discrepancy (16,440 actual property reads, corrected before freezing); all three reference corrections now pass and all three broken states fail relevant checks. CLI transport succeeded with safe mode and the pinned canonical model; tool transport is checked separately before scored execution.
- Raw outputs will stay under ignored `artifacts/pilot-runs/`; protocol, fixtures, runner and reviewed results stay in `evals/pilot/`. Next: checkpoint the frozen protocol, then launch the six scored sessions without editing it.

- Preflight review found seven evaluation gaps before any scored execution: missing nonempty valid arrays, incomplete benchmark responses, a palindromic mutation witness, missing response/boolean cases, loose model matching, process cleanup, and executable access outside fixtures. Corrected the rubric and runner. Calibration-v6 rejects all original broken states and five extra counterexamples; all three reference corrections pass. Its AEO sandbox probes deny outside reads/writes, dependency writes and external network. Earlier calibration setup failures remain in ignored artifacts, including the macOS root-directory read and localhost-rule adjustments.
- Node tool execution and grading now use an outside-fixture wrapper forcing macOS `sandbox-exec`; copied runtime dependencies replace the host symlink. Exact model/context checks and dedicated process-group cleanup apply to each execution. A second read-only review and a client-to-sandbox transport check precede protocol freezing. Scored runs remain unstarted at this checkpoint.
- Final preflight milestone: nine source findings addressed, including runtime-path portability and inherited environment variables. Read-only reviewer found no remaining actionable issue. Calibration-v8 passes all reference corrections, rejects five extra mutants and passes five sandbox/environment controls. Client transport with the final environment allowlists successfully ran Node/build/HTTP probe, with no permission denials. A controlled timeout left no running grandchild. Dry-run pack contains 60 files, 18 pilot files and no raw traces, Python bytecode or other generated bulk. The next commit freezes the protocol before six scored executions; editorial README/provenance changes remain a separate diff.
- First execution milestone: source `66f7b1a`, raw `artifacts/pilot-runs/run-1/`. All six sessions reached a terminal result. Five are unscored (`unknown`) because they requested denied shell/Git commands; Gauntlet baseline completed, passed 4/4 checks and read 400 userId properties. The protocol omitted an explicit explanation of the Node-only shell policy. Preserve these outcomes in the public report, without treating unscored sessions as task failures or passes.
- One bounded repeat is authorized within the three-pair task objective. Freeze `protocol-v2.json` before repeating all three pairs, adding the same explicit tool/fixture guidance to both arms. Keep fixtures, skill texts, independent checks, model, budget, permissions and stop rules unchanged. The runner only gains selection/recording of the protocol file. No third attempt or catalog expansion is part of this follow-up.
- Completed pilot milestone: v2 frozen at `be6b8d7`, raw `artifacts/pilot-runs/run-2/`. All six sessions completed with no tool denials and no fixed-file changes. Gate tied 5/5; Gauntlet tied 4/4 and 400 reads in both arms; AEO scored 4/5 baseline and 5/5 supplied skill. Baseline kept the unpublished route served at 200; treatment excluded it and received 404. Interpretation is fixture-specific, one session per arm, with no general effect or upstream ranking claim.
- Prepared public `evals/pilot/{REPORT.md,results.json,calibration.json,evidence/}`: 12 session summaries, source/protocol/runner and trace hashes, 12 small editable-source patches, calibration and five extra rejected mutants. All fixture and skill-text hashes match across both rounds; all fixed source files are unchanged. Raw traces/workspaces and delivery notes stay ignored. Both READMEs and paired portfolio prose now include the overlap/positioning and honest pilot result. Next: final read-only review, scoped checks, actual browser rendering, and pushed checkpoints/CI. CodeRabbit/production publication remain separate.
- Final package validation passed: structural check, local editorial links, all 12 public patch hashes and dry-run package inventory (76 files, 167,937 unpacked bytes before final ledger text; no traces/bytecode/bulk). Read-only adversarial review covered every public result/patch/hash, both README/article versions, provenance and scope, with no actionable finding. Portfolio's text gate and Astro check passed; its build/preview remain owned by its ledger. Ego Lite verified paired tables, language navigation and no page overflow; mobile tables scroll horizontally as designed. Next: commit/push this reviewed result and verify public CI/report availability.
- Published result checkpoint `57554a21bd7a4df75884b204d08fb0344ebc90a0` passed collection CI run `41158481090`. The public report rendered successfully in Ego Lite; the 12 small source patches, summaries and calibration are public, while raw traces remain ignored.
- Paired portfolio content checkpoint `a55aa8bee56a65dd097ba0c12d770dd05a76b2a4` passed CI run `41158594113` and Vercel Preview. Authenticated HTTP requests verified both localized titles, canonical URLs, score tables, report links and pinned upstream links. PR #39's description now covers the final scope and AI assistance. No CodeRabbit review/threads or reply to the existing request; no production merge/deploy, npm release, global activation or catalog expansion performed.
- This documentation checkpoint closes the authorized positioning and three-case pilot follow-up. Next: portfolio PR review and any future review findings. The 22-case Codex/Claude plan remains unexecuted; one completed session per arm does not establish general effectiveness or an upstream ranking.

## Individual installation verification (2026-10-31)

- Both READMEs now recommend selecting one skill with `--skill` and `--agent`, using the optional Vercel CLI. Node.js 22.20+ is documented for that CLI; the collection still has no npm release. Full plugin installation is labeled as the optional 11-skill bundle.
- Ran the exact manual shell blocks extracted from both README languages for both clients and all 11 skills (44 copies). Every file's relative path and SHA-256 matched its source folder, including supporting references. Existing destination directories, files and dangling symlinks were refused; sibling skill files stayed unchanged.
- Real `skills@1.7.4` discovery listed all 11 skills. Installed `aeo` then `critical-adversarial-review` independently for Codex and Claude Code in disposable projects; copied content matched, existing sibling files survived and other collection skills were absent. Automatic confirmation was used only in disposable validation, not the public commands. Telemetry was disabled for validation.
- `npm run check` passed: 11 skills, 31 files, manifests, links and 22 explicitly unexecuted evaluation cases. Verification report and command logs: `artifacts/pilot-runs/skill-by-skill-20261031/installation-verification.json`. These checks validate file layout/content, not native client routing or model behavior.
- Next: scoped PRs, current-head review, authorized merge and public CI/publication verification. Final state will be in the ignored `FINAL-STATE.md` alongside that report.
