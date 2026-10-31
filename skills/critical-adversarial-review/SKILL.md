---
name: critical-adversarial-review
description: Independently review a proposed change, design, or analysis for concrete failures and unsupported claims. Use when adversarial review is requested or a consequential result needs verification by someone other than its author.
---

# Critical adversarial review

Return actionable failures supported by evidence. A useful review can find nothing; never invent findings to fill a quota.

## Establish the review surface

Pin the specification, current revision or artifact hash, and relevant diff or analysis. Read the applicable project rules. For the initial independent pass, give the reviewer the required behavior and raw artifacts without the builder's persuasive summary.

Review the actual result. Verify that cited files, screenshots, traces, or measurements belong to the revision under review.

## Try to falsify the result

Choose failure modes that fit:
- A missed caller, compatibility boundary, or state transition.
- Authorization, privacy, or untrusted input crossing a trust boundary.
- Retries, concurrency, partial failure, stale state, or data loss.
- A test that checks a declaration while the runtime uses something else.
- A metric that improves while the desired behavior gets worse.
- A conclusion depending on an unstated assumption, sample, or source.

Prefer a small counterexample or focused check over rerunning unrelated suites. Inspect code read-only by default. Execute target-controlled code only within the task's allowed environment and permissions.

For visual changes, inspect captures at the intended viewport. Technical checks cannot establish human visual acceptance.

## Report and close

Use [the finding contract](references/review-contract.md). Include location, trigger, demonstrated failure, impact, and the smallest sound correction. Distinguish demonstrated findings from concerns needing validation.

Keep style preferences separate from defects. Report no actionable findings when that is what the evidence supports, together with material limits on coverage.

After fixes, review the new revision and check the original failure again. A resolved discussion is not evidence that the behavior changed.
