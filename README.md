# Ruben's agent skills

The 11 workflows I use across projects with Codex and Claude Code, rewritten as reusable instructions. Debugging, adversarial review, bounded improvement loops, research, collaboration, Git hooks, and AEO.

[Português brasileiro](README.pt-BR.md)

**Version 0.1.0.** Eleven skills, one shared source, MIT license. Structural checks and a [small paired pilot](evals/pilot/REPORT.md) are recorded; full Codex/Claude behavioral evaluation remains pending. Distribution is through this Git repository and plugin metadata; there is no npm release.

## Choose a workflow

Two starting points come directly from my project work: [AEO](skills/aeo/SKILL.md) for aeo.js integration and served discovery checks, and [Gauntlet](skills/gauntlet-loop/SKILL.md) for measured improvement rounds such as game lighting. The other workflows organize the checks, research, and implementation around those tasks.

| Skill | Use it for |
| --- | --- |
| [critical-adversarial-review](skills/critical-adversarial-review/SKILL.md) | Independent review tied to an exact revision and reproducible defects |
| [gauntlet-loop](skills/gauntlet-loop/SKILL.md) | Repeated build, critique, and regression rounds with an acceptance bar |
| [evidence-driven-debugging](skills/evidence-driven-debugging/SKILL.md) | Tracing the user's reported failure through the real data and runtime path |
| [quality-gates](skills/quality-gates/SKILL.md) | Gates that measure the intended behavior and reject a deliberately broken control |
| [source-backed-research](skills/source-backed-research/SKILL.md) | Technical and social-media research with traceable sources and explicit uncertainty |
| [multi-agent-collaboration](skills/multi-agent-collaboration/SKILL.md) | Reproducible peer-agent handoffs, ownership, and conflict resolution |
| [spec-to-plan](skills/spec-to-plan/SKILL.md) | Turning a request into testable acceptance criteria and implementation slices |
| [validated-coding-loop](skills/validated-coding-loop/SKILL.md) | Iteration with real diagnostics, checkpoints, and a stop condition |
| [agent-worktree-orchestration](skills/agent-worktree-orchestration/SKILL.md) | Isolated writers and explicit selection among parallel implementation candidates |
| [git-quality-hooks](skills/git-quality-hooks/SKILL.md) | Staged secret scanning and project-specific Git checks |
| [aeo](skills/aeo/SKILL.md) | AEO audits and integration using aeo.js, crawler policy, structured data, and served evidence |

Start with the skill that matches the current task. Review, debugging, and quality gates address different failure modes; they do not each need a separate agent. Multi-agent skills apply when parallel work is requested or already authorized.

The [example tasks](#example-tasks) give a scenario, prompt, and expected artifact for all 11 skills.

The collaboration method was generalized from the author's ECDSA work. Planning, validated iteration, and worktree coordination draw on Ralph Starter. AEO uses the actual aeo.js CLI and adapter surface. See [provenance](PROVENANCE.md) for source revisions and distribution references.

## Complementary collections

[Matt Pocock's skills](https://github.com/mattpocock/skills) and [Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills) cover several of the same decisions. Independent review, negative controls, and agent coordination also appear in their workflows. I keep this collection as my project selection; choose the instructions that fit your task and existing setup.

| Task | Another workflow to read |
| --- | --- |
| Reproduce a bug before changing code | [Matt's diagnosing-bugs](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/diagnosing-bugs/SKILL.md) |
| Review an artifact against its contract | [Addy's doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/doubt-driven-development/SKILL.md) |
| Define measurable constraints and broken controls | [Addy's constraint-driven-development](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/constraint-driven-development/SKILL.md) |
| Set up repository checks before commits | [Matt's setup-pre-commit](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/misc/setup-pre-commit/SKILL.md) |

These links pin the inspected revisions. Their content stays in the upstream repositories. This collection makes no effectiveness ranking against either suite.

## Install or try one workflow

Clone the collection first:

```sh
git clone https://github.com/rubenmarcus/agent-skills.git
cd agent-skills
```

No installation script runs automatically. Review a skill and its references before enabling it. The Git hook is an inert example inside a skill; this package does not activate it.

### Codex

For an isolated project trial, copy one selected folder into the target project's `.agents/skills/`. From this collection's root, after choosing an existing target directory:

```sh
target_project=/absolute/path/to/your-project
mkdir -p "$target_project/.agents/skills"
test ! -e "$target_project/.agents/skills/critical-adversarial-review" &&
  cp -R skills/critical-adversarial-review "$target_project/.agents/skills/"
```

Start or refresh the agent session as required by the installed client, then invoke `$critical-adversarial-review` with the actual revision and scope. Preserve any folder already present instead of overwriting it. The root `plugin.json` also provides portable plugin metadata for hosts that support it.

This follows [Codex's documented project skill discovery](https://learn.chatgpt.com/docs/build-skills). Plugin metadata does not mean this repository has been listed in OpenAI's plugin directory.

### Claude Code

Load this checkout for a local session, using its absolute path:

```sh
claude --plugin-dir /absolute/path/to/agent-skills
```

Ask Claude to use the packaged `critical-adversarial-review` skill for a bounded revision. Plugin skills may appear under the plugin namespace; check the installed client's skill list. No global configuration is changed by the command shown here.

To install through Claude Code's marketplace instead, run these commands inside a Claude session:

```text
/plugin marketplace add rubenmarcus/agent-skills
/plugin install rubenmarcus-skills@rubenmarcus
```

The plugin name and marketplace name come from this repository's manifests. Choose the desired installation scope in the client. See [Claude Code's installation documentation](https://code.claude.com/docs/en/discover-plugins) for permissions and available scopes.

For either agent, tool access, permissions, and project instructions still come from the host. These Markdown workflows do not ship an orchestration runtime, install aeo.js, or start background agents.

## Validate and package

Node.js 20+ is enough for the structural check; no npm dependencies are required. Python 3 runs the isolated hook fixture.

```sh
npm run check
npm run check:hook
claude plugin validate . --strict
npm pack --ignore-scripts --pack-destination /tmp
```

`check` verifies skill metadata, local references, manifest consistency, package entries, and the scenario inventory. It is a deliberately small check for this repository's scalar metadata format, not a general YAML parser or a behavioral evaluator. `check:hook` uses a fake scanner to verify argument and exit propagation, including the missing-scanner case; it does not measure gitleaks detection quality.

[Evaluation scenarios](evals/scenarios.json) describe positive and boundary cases for a future Codex/Claude run. Record client/model versions, revision, tool permissions, actual outputs, failures, and review decisions when executing them. A green package check does not establish that an agent followed the workflow.

The [three-task pilot](evals/pilot/REPORT.md) compared supplied skill text with no supplied skill in fresh Claude sessions. After one symmetric tool clarification, gate and route checks tied (5/5 and 4/4); AEO passed 5/5 with the skill and 4/5 without it. The baseline still served an unpublished draft. All 12 task sessions across both frozen rounds are recorded, including five unscored first-round sessions after tool denials. One execution per arm in each round does not establish a general effectiveness ranking; native routing and the separate 22-case plan remain untested.

The package uses an explicit file list. The companion articles in Brazilian Portuguese and English are maintained in the author's portfolio, outside this collection. npm publishing is disabled with `private: true`; Git/plugin distribution does not require a custom installer or npm release.

## Example tasks

Each example gives you a situation, a starting prompt, and an artifact to look for. Replace revisions, routes, versions, fixtures, and budgets with your project's inputs. These prompts describe tasks to try; [evaluation scenarios](evals/scenarios.json) track the behavioral checks still to run.

### critical-adversarial-review

Use it before merging an API change, when you need an independent check of pagination and its callers.

```text
Use critical-adversarial-review on BASE..HEAD. The endpoint must preserve
pagination when the filter changes. Read the diff and callers, without
editing files. Report locations, triggers, expected and observed behavior,
and minimal reproductions. Label unexecuted hypotheses. Zero findings is OK.
```

Look for: evidence-backed findings at the reviewed revision, plus coverage limits.

### gauntlet-loop

Use it when improving a game's map lighting needs several rounds of captures, critique, and regression checks.

```text
Use gauntlet-loop to improve this map's lighting against the supplied
visual criteria. Keep the same camera path, viewport, and capture settings.
Record a baseline, compare each candidate with an independent critique,
and check the other reference scenes. Use the agreed round budget.
```

Look for: a round record with baseline and candidate captures, regressions, and a keep, revise, or reject decision. Human visual approval stays explicit.

### evidence-driven-debugging

Use it when a dashboard's participant count disagrees with the underlying records.

```text
Use evidence-driven-debugging on the active-participant count shown here.
Trace the displayed value through the request, query, stored records,
and render. Check distinct participants versus event counts and stale
responses. Reproduce the mismatch, fix its cause, and rerun that path.
```

Look for: the reproduced failure, its cause, and before/after evidence from the same UI and data path.

### quality-gates

Use it when CI passes even though a checkout regression is still visible.

```text
Use quality-gates to assess the existing checkout regression gate.
In a disposable copy, apply one known-broken change and verify that the
gate rejects it for the expected reason. Restore the copy afterward.
Confirm the mutation took effect. Also exercise a missing measurement.
```

Look for: results for the valid baseline, the deliberate defect, and unavailable evidence, with the measured behavior and reproduction commands.

### source-backed-research

Use it before choosing a library whose retry behavior could duplicate a write.

```text
Use source-backed-research to compare the documented retry semantics
of these two libraries at the supplied versions. Check official docs
and source for write retries and idempotency. Keep URLs, dates, source
claims, and inferences in the evidence ledger. Report unresolved questions.
```

Look for: a comparison tied to versions and sources, the recommendation's assumptions, and the next check that could change it.

### multi-agent-collaboration

Use it when two agents already investigating an intermittent failure disagree about whether caching or retries cause it.

```text
Use multi-agent-collaboration to reconcile these two investigations.
Keep the existing ownership boundaries. Have each agent hand off its
revision, configuration, exact input, command, result, and artifact paths.
Choose the smallest experiment that distinguishes their explanations.
```

Look for: reproducible handoffs, the discriminating experiment, and a shared conclusion that records rejected hypotheses and remaining unknowns.

### spec-to-plan

Use it when an issue says "add team invitations" but leaves expiry, permissions, and repeated acceptance unclear.

```text
Use spec-to-plan on this team-invitations issue. Inspect the current
auth and membership contracts. Identify decisions about expiry, roles,
and repeated acceptance. Write observable acceptance criteria and order
the implementation slices. Surface product decisions that need an answer.
```

Look for: a scoped plan with failure cases, dependencies, unresolved decisions, and the first implementable slice.

### validated-coding-loop

Use it when implementing an agreed fix for duplicate webhook delivery requires several code and validation attempts.

```text
Use validated-coding-loop to implement the approved webhook deduplication
spec on this branch. Work from the supplied delivery fixtures and checks.
After each focused change, save the actual diagnostic and checkpoint.
Meet the acceptance criteria within the agreed budget; diagnose repeated
failures and preserve the next action if the run stops.
```

Look for: a recoverable implementation, a record of attempts, and acceptance evidence at the current revision.

### agent-worktree-orchestration

Use it when you've authorized two implementation candidates for a cache change and want to compare them without shared writes.

```text
Use agent-worktree-orchestration for the two authorized cache candidates.
Start from the same base commit in separate branches and worktrees.
Record each writer's allowed paths and budget. Compare both with the
supplied correctness and latency checks. Return both revisions and the
selection evidence to one integration owner.
```

Look for: an ownership map, isolated candidate commits, a comparison using the same inputs, and a verified integration handoff.

### git-quality-hooks

Use it when adding staged secret scanning to a repository that already has Husky or another hook manager.

```text
Use git-quality-hooks to add staged gitleaks scanning to this repository.
Inspect core.hooksPath and the existing hook manager first. Preserve its
checks, redact scanner output, and fail if the scanner is unavailable.
Verify argument and exit-code propagation with synthetic isolated fixtures.
```

Look for: a composed hook, setup instructions, and fixture results. The fixture proves hook plumbing; scanner detection needs its own evidence.

### aeo

Use it when an Astro site has English and Portuguese content, existing crawler restrictions, and discovery files that need to agree with real routes.

```text
Use aeo to audit this site's EN/PT discovery with the pinned aeo.js version.
Inspect existing robots and sitemap ownership, canonical URLs, and JSON-LD.
Fix the observed gaps while preserving crawler policy. Build and verify
the public routes and enabled discovery files on the authorized preview.
```

Look for: an audit and served-response evidence for canonical URLs, structured data, and discovery files, with remaining gaps recorded.

## Scope and license

MIT for this collection's new text and examples. Referenced projects retain their own licenses. No third-party skill suite, private project source, licensed game asset, or personal voice profile is bundled.

AEO checks establish observed implementation and discovery surfaces. They cannot promise ranking, answer citations, or traffic. For credit analysis or other consequential decisions, these general workflows still need domain-specific requirements, validated data, evaluation, and the appropriate human decision process.
