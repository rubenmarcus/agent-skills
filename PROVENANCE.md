# Sources and derivation

This collection contains newly written generic instructions and examples prepared with AI assistance. Source inspection informed the methods. References do not imply an upstream endorsement or transfer of an upstream license.

## Author's workflows

| Source | Inspected revision | What informed this collection |
| --- | --- | --- |
| [CORO SOLTO client](https://github.com/corosolto/client) | `86c388b560e43e92cac13cd2675a86a69b715641` | Runtime evidence, independent review, gauntlet rounds, negative controls, staged Git checks |
| [Ralph Starter](https://github.com/rubenmarcus/ralph-starter) | `ee9c7946c386bb9cecc4001a052e29ffa53f8f9a` | Specification, acceptance criteria, bounded executor loops, sessions, circuit breakers, worktrees, coordination strategies |
| [aeo.js](https://github.com/rubenmarcus/aeo.js) | `9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1` | CLI commands, configuration types, generation ownership, framework adapter shape |

The generic collaboration skill also draws on the author's local `ecdsafail-multi-agent-collaboration` workflow: independent hypotheses, revision-pinned evidence, mailbox processing, reproductions, and one integration owner. Domain-specific circuit metrics, quantum arithmetic, scan commands, and original project instructions are excluded. The original skill is unchanged.

Research instructions consolidate the author's evidence-ledger and social-media research practices. The portfolio and Scanrepo were inspected for useful workflows. Their source and private notes are not bundled; Scanrepo-specific analysis and bilingual publication remain possible later extractions, not features of this release.

CORO SOLTO's source is AGPL-3.0; Ralph Starter and aeo.js identify as MIT. This collection links to the source and rewrites general methods in new prose. It does not vendor those projects' source code, skill text, assets, or license them under this collection's MIT grant. The shell example is newly written around the documented gitleaks CLI contract.

## Concrete implementation references

- Ralph: [`src/loop/`](https://github.com/rubenmarcus/ralph-starter/tree/ee9c7946c386bb9cecc4001a052e29ffa53f8f9a/src/loop) and [`src/automation/worktree.ts`](https://github.com/rubenmarcus/ralph-starter/blob/ee9c7946c386bb9cecc4001a052e29ffa53f8f9a/src/automation/worktree.ts). These are method sources, not a promise that this package implements Ralph's runtime.
- Ralph: [`src/loop/swarm.ts`](https://github.com/rubenmarcus/ralph-starter/blob/ee9c7946c386bb9cecc4001a052e29ffa53f8f9a/src/loop/swarm.ts). At this revision the consensus code chooses successful results by iteration count, despite the header's LLM-judge description. The generic skill calls for an explicit acceptance rubric.
- aeo.js: [`src/cli.ts`](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/src/cli.ts), [`src/types.ts`](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/src/types.ts), and [`src/plugins/astro.ts`](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/src/plugins/astro.ts). Package metadata says 0.0.17, while the exported CLI version constant says 0.0.14. Identify the source revision as well as the printed version.

## Distribution references

[Addy Osmani's agent-skills](https://github.com/addyosmani/agent-skills) and [Matt Pocock's skills](https://github.com/mattpocock/skills) informed the idea of a focused repository with discoverable skill folders and plugin metadata. Their skill content is not copied or bundled.

The follow-up comparison on 2026-10-31 inspected Matt's `a496f5513d4a4cf889bc48e189e579f4b0bdf6aa` and Addy's `eb07f19f52c2669f2364897aaa293e2aaddd7b1c`. Matt's [diagnosing-bugs](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/diagnosing-bugs/SKILL.md) also calls for reproductions, competing hypotheses and confirmation that a mutation took effect. Addy's [doubt-driven-development](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/doubt-driven-development/SKILL.md) separates artifact review from the builder, while [constraint-driven-development](https://github.com/addyosmani/agent-skills/blob/eb07f19f52c2669f2364897aaa293e2aaddd7b1c/skills/constraint-driven-development/SKILL.md) uses measurable thresholds and mutation checks. These are overlapping methods. The README links complementary workflows rather than claiming novelty or measured superiority. The local pilot compares this collection's supplied text against no supplied skill; neither upstream collection is an experimental arm.

Manifest layouts follow [OpenAI's plugin packaging documentation](https://developers.openai.com/plugins/build/plugins) and [Claude Code's manifest reference](https://code.claude.com/docs/en/plugins-reference). Installation instructions also follow [Codex's local skill discovery](https://learn.chatgpt.com/docs/build-skills) and [Claude Code's marketplace installation](https://code.claude.com/docs/en/discover-plugins), checked on 2026-10-31. A public Git repository is distinct from a listing in a hosted plugin directory.

Third-party research suites, bundled platform skills, and other authors' packages remain external dependencies or recommendations subject to their own terms. Personal communication workflows and project-specific cover generation are outside this collection's scope.
