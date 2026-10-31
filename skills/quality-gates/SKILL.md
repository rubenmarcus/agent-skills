---
name: quality-gates
description: Design or repair checks that measure real behavior and fail under a deliberate defect. Use when adding invariants, probes, regression gates, quality thresholds, or diagnosing a green check that misses a real failure.
---

# Quality gates

A gate needs a behavioral contract and evidence that it can reject a broken result.

## Define what it observes

Name the defect the gate should catch and a bad state that could accidentally improve its metric. Measure in the environment where the behavior matters.

Read runtime effects when declarations can differ. A constant's value does not prove a caller uses it. File existence does not prove contents or provenance.

Choose thresholds from a reference, baseline, budget, or requirement. Record the basis and units. Locate other checks of the same contract to avoid contradictory thresholds.

## Prove the check

Exercise a valid baseline, a relevant broken state or deliberate mutation, and a failed or unavailable measurement.

Confirm the mutation actually applied. Preserve output showing that the check caught it, then restore the original state in the owned fixture or worktree.

A missing measurement must not become a passing zero. Represent unavailable evidence explicitly and make the completion decision respect that status.

## Make failure actionable

Report the value, threshold, scenario, input identity, and reproduction command. Visual contracts need inspectable captures as well as numbers.

Keep the check within its execution budget. Document required ordering between producers and consumers of evidence. Regenerate inputs for a new revision.

Do not relax thresholds just to pass. Revisit the contract when the reference, requirement, or measurement is shown to be wrong.
