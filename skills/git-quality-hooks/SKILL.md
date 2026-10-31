---
name: git-quality-hooks
description: Add or repair local Git hooks for staged secret scanning and project-specific quality checks without overwriting existing workflows. Use for pre-commit, commit-msg, pre-push, or a requested local gate before sharing code.
---

# Git quality hooks

Put fast mechanical checks at the appropriate Git boundary. Preserve existing hook managers and team requirements.

## Inspect the installation

Check the repository, branch, status, core.hooksPath, existing hooks, package scripts, and any hook manager. Determine whether the user requested advice or installation.

A collection's hook example must not activate merely because the skill is installed. Integrate only when hook configuration is part of the task.

## Place checks deliberately

- Pre-commit: staged-secret scanning and fast checks of staged content.
- Commit-msg: the project's actual message contract, if one exists.
- Pre-push: broader project verification before transferring changes.

Check the staged snapshot when the contract concerns the commit. Running a working-tree formatter does not establish what the staged version contains.

Use [the pre-commit example](assets/pre-commit) for gitleaks only when that tool and command fit the environment. It redacts findings and fails if the scanner is unavailable. Compose it with existing hooks; do not overwrite or bypass their checks.

Choose any size or timing limits from project conventions. Do not carry one project's arbitrary numbers into another repository.

## Verify and explain

Use an isolated fixture to check passing input, a failing scanner exit, and an unavailable scanner. Use synthetic data only. Preserve exit codes through wrappers and pipelines.

Document setup, dependencies, and which behavior each hook checks. Local hooks are not automatically active in every clone; use CI for the contracts the team requires remotely.

A hook can enforce mechanical checks. Independent review still needs an actual reviewer and evidence at the revision being shared.
