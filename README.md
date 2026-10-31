# Ruben's agent skills

Engineering workflows for Codex and Claude Code: trace a bug, challenge a change, run a bounded improvement loop, research a claim, coordinate agents, or verify a site's AEO integration.

**Local preview, version 0.1.0.** No public repository or npm release has been created from this checkout. Structural and fixture checks are separate from real-agent behavioral evaluation, which is still pending.

## Choose a workflow

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

The collaboration method was generalized from the author's ECDSA work. Planning, validated iteration, and worktree coordination draw on Ralph Starter. AEO uses the actual aeo.js CLI and adapter surface. See [provenance](PROVENANCE.md) for source revisions and distribution references.

## Try the local checkout

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

### Claude Code

Load this checkout for a local session, using its absolute path:

```sh
claude --plugin-dir /absolute/path/to/agent-skills
```

Ask Claude to use the packaged `critical-adversarial-review` skill for a bounded revision. Plugin skills may appear under the plugin namespace; check the installed client's skill list. No global configuration is changed by the command shown here.

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

The package uses an explicit file list. The article draft and local continuation ledger remain repository artifacts. npm publishing is disabled with `private: true`; Git/plugin distribution does not require a custom installer or npm release.

## Scope and license

MIT for this collection's new text and examples. Referenced projects retain their own licenses. No third-party skill suite, private project source, licensed game asset, or personal voice profile is bundled.

AEO checks establish observed implementation and discovery surfaces. They cannot promise ranking, answer citations, or traffic. For credit analysis or other consequential decisions, these general workflows still need domain-specific requirements, validated data, evaluation, and the appropriate human decision process.
