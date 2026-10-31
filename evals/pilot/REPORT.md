# Three paired task probes

This pilot records two frozen rounds of three synthetic tasks. Each round has one fresh session per arm: the task alone, or the task plus one skill's text and local references. The model is Claude Code 2.1.280 using `claude-opus-5-5[1m]` at medium effort. Matt Pocock and Addy Osmani's collections are outside the experimental arms.

## Observed outcome

All six sessions in the clarified second round completed with no tool denials or changes to fixed sources. Gate and route checks tied. AEO passed one additional check with the supplied skill: the unpublished route was excluded.

| Second-round task | No supplied skill | Supplied skill |
| --- | --- | --- |
| Release gate | 5/5 checks | 5/5 checks |
| Participant summary | 4/4 checks, 400 reads | 4/4 checks, 400 reads |
| Public EN/PT discovery | 4/5 checks | 5/5 checks |
| Total | 13/14 checks | 14/14 checks |

The AEO baseline kept `/private/draft` in `config.routes` and disabled optional discovery generators. The independent HTTP probe still received 200 for the unpublished page, and its generated HTML retained `INTERNAL_DRAFT_MARKER`. The skill-supplied candidate removed that route; the probe received 404 and generated files excluded the path and marker. Both preserved the exact owned robots/sitemap files and served public canonicals and parseable page JSON-LD.

The baseline's delivery explicitly treated removing the draft as outside its request. The fixture labels that content unpublished, and the frozen exclusion check requires it to be absent from public output. This result depends on that stated fixture interpretation. It is one observed difference in one task, insufficient for a general benefit claim or a ranking against other collections. The two ties provide no demonstrated pass-rate benefit for those tasks.

## What the checks measure

| Task | Selected skill | Independent checks |
| --- | --- | --- |
| Release gate | `quality-gates` | 5 groups: valid observations pass; slow, missing and malformed observations return `ok: false` |
| Participant summary | `gauntlet-loop` | 4 groups: full response/order, string edge cases, input preservation and at least halved input property reads |
| Public EN/PT discovery | `aeo` | 5 groups: exact robots/sitemap preservation, unpublished content exclusion, served canonicals and parseable page JSON-LD |

The initial route performs 16,440 input property reads for 400 events and 40 users. The target is at most 8,220 reads. These counts measure reads in this fixture, not latency or frame rate. The AEO fixture exercises the real aeo.js 0.0.16 adapter with synthetic HTML and local HTTP responses; it is separate from a complete Astro build, a deployment or search/citation outcomes.

## First round: tool mismatch stays visible

[`protocol.json`](protocol.json) was frozen at [`66f7b1a`](https://github.com/rubenmarcus/agent-skills/commit/66f7b1a). All six sessions reached a terminal result. Five requested shell/Git commands outside the permitted tool policy and remain `unknown`, without scores. A tool denial is an execution limit, not evidence that the candidate source failed the task.

| Task | No supplied skill | Supplied skill |
| --- | --- | --- |
| Release gate | Unknown, 1 denied request | Unknown, 2 denied requests |
| Participant summary | Completed, 4/4 checks, 400 reads | Unknown, 2 denied requests |
| Public EN/PT discovery | Unknown, 2 denied requests | Unknown, 1 denied request |

The rejected requests included shell loops with `cat`/`ls`, `grep`, copying with `cp`, and Git commands. The task instructions had not explained that shell commands must be complete Node invocations. No pair in this first round supports a treatment comparison.

## One bounded repeat

[`protocol-v2.json`](protocol-v2.json) was frozen at [`be6b8d7`](https://github.com/rubenmarcus/agent-skills/commit/be6b8d7) before repeating all three pairs once. Both arms received the same extra explanation: use Read/Write/Edit for files, use complete Node invocations for commands, use Node APIs for extra checks and artifact hashes, and do not use Git or shell utilities. The fixtures, skill texts, independent checks, model, permissions, limits and scheduled order stayed unchanged. The runner's amendment selects and records the protocol file; its execution and grading functions are unchanged from the first freeze.

The second round is an adaptive clarification of the tool contract. It is reported separately and does not replace the six earlier sessions. No third round was planned for this follow-up.

## Calibration and review

Before scored model execution, independent checks rejected each defective starting fixture and accepted a separate reference correction. Read-only review found missing valid nonempty participant arrays, incomplete benchmark-response checks, a palindromic input-mutation witness and missing response/boolean cases. Those were corrected before the first freeze. Five extra broken implementations are now rejected, including capped benchmark counts and reversed inputs.

The [calibration record](calibration.json) contains those checks and observed sandbox controls: outside reads/writes, dependency writes and external network access are denied, and candidate Node sees the environment allowlist. Both allowed client transport and a controlled process-group timeout were exercised before freezing. Subsequent source review found no remaining actionable issue in the protocol or its tool clarification.

## Scope and reproducibility

Both arms use separate fixture copies, new sessions, matching tools/settings and no MCP or additional agents. Supplied text is the treatment; native skill routing and Codex behavior are untested. Each execution has a 240-second deadline and a reported USD 2 API-budget cap. That cap is CLI accounting, not a subscription-billing claim. At most two target processes run concurrently. Elapsed time is recorded for traceability, not compared as a speed result.

Node commands and independent grading run through macOS `sandbox-exec`. AEO dependencies are copied and hash-checked. Node can read file contents in its fixture and installed system/runtime files, and inspect file metadata elsewhere; fixture dependencies are read-only to Node. Its only network exception is the assigned local HTTP port. The authenticated client keeps its own transport and a separate OS-variable allowlist. Full details and reproduction commands are in the [pilot README](README.md).

[results.json](results.json) records both rounds, source/protocol/runner hashes, observed model IDs, tool-denial counts, independent observations, candidate hashes and raw-trace hashes. The `evidence/` patches preserve only the editable synthetic sources. Raw event streams, workspace copies and agent-authored delivery notes remain under ignored local artifacts; those delivery notes are not accepted as independent grading evidence.

One execution per arm and three small tasks cannot establish a general effectiveness ranking, a statistical effect or validation of all 11 workflows. Gauntlet's independent critic during the loop and human visual approval are outside these target sessions. The [22-case Codex/Claude plan](../scenarios.json) remains unexecuted. Repeated project tasks, boundary behavior and native routing need their own evaluation before expanding the catalog.
