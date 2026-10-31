---
name: multi-agent-collaboration
description: Coordinate multiple agents on implementation or research with isolated ownership, reproducible handoffs, independent checks, and evidence-based conflict resolution. Use when parallel or peer-agent work is requested or already in progress.
---

# Multi-agent collaboration

Produce a result another agent can reproduce and continue. Use the host's agent, task, or messaging tools when available. A shared document or file queue is sufficient when separate sessions need a mailbox.

## Choose a useful split

Read the continuation record and outstanding messages before assigning work. Identify the objective, acceptance evidence, allowed changes, shared dependencies, and coordinator.

Split by independent questions, hypotheses, or owned files. A literature check and an implementation experiment can proceed together; two agents rewriting the same module need isolation or a sequential handoff. Use one agent when coordination would cost more than it resolves.

Each assignment needs:
- A concrete question or deliverable and the minimum source context.
- Ownership: writable paths or worktree, read-only dependencies, and actions outside scope.
- Acceptance evidence and the artifact the next agent will receive.
- A stopping condition or budget when the task has one.

Use separate worktrees for concurrent code changes. Agents sharing a filesystem must have non-overlapping writes. The coordinator owns integration and reruns acceptance checks after combining changes.

## Exchange reproducible evidence

For substantial handoffs, use [the message contract](references/message-contract.md). Include the exact revision, configuration, input or fixture identity, command, result, and artifact path. Label observations, interpretations, and unresolved claims separately.

Use built-in messaging first. If a mailbox is necessary, record a stable message ID and persist the cursor only after processing the message. Keep messages bounded and point to large artifacts. Do not put credentials or full private datasets in messages.

Worker conclusions remain hypotheses until supported by sufficient evidence. Reproduce consequential claims independently, especially where a different environment, validator, or metric could change the decision.

## Resolve conflicts

Find the smallest test that distinguishes the explanations. Compare inputs, revisions, defaults, units, measurement windows, validation modes, and external reference versions.

A timeout or missing artifact is unknown. Agreement between agents is supporting evidence only when their methods and inputs justify it. Do not turn repeated opinions into a measured result.

When a verified result contradicts an earlier analysis, revise the analysis and record what changed. Share failed hypotheses and their reopening conditions to avoid duplicate retries.

## Converge and preserve

Select a candidate using the acceptance criteria. Integrate it in one owned lane, verify the combined result, and record rejected alternatives and remaining uncertainty.

Before changing agent, branch, or context, update the project-owned continuation record with objective, current revision, completed checks, artifacts, blockers, and the next action. Idle user time alone is not a stopping condition.

Task authorization does not imply permission to publish, deploy, merge, contact others, or spend outside an agreed budget.
