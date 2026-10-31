# Three paired task probes

This pilot compares one fresh Claude Code session given a selected workflow's text with one fresh session given the same task without that text. The three synthetic tasks exercise gate calibration, bounded route improvement, and public EN/PT discovery with aeo.js.

The protocol, prompts, fixtures, and independent checks are frozen before scored execution. Each task has one execution per arm. Six sessions cannot establish a general effectiveness ranking, a statistical effect, or validation of all 11 skills. Matt Pocock and Addy Osmani's collections are source references, outside this experiment.

The first six sessions used `protocol.json`, frozen at `66f7b1a`. Five requested shell/Git commands outside the permitted tools and remain unscored. `protocol-v2.json` freezes one bounded repeat, adding the same explicit Node-only tool guidance to both arms. Fixtures, skill texts, checks, model, permissions and limits are unchanged. Preserve both rounds in the report; the second round does not replace the first round's record.

## Controls

- Claude Code 2.1.280, `claude-opus-5-5[1m]`, medium effort, identical tool permissions and limits within each pair.
- Safe mode disables personal skills, hooks, plugins and project instructions. Restricted mode confines file tools to the fixture. No MCP servers or additional agents are available. Auth uses the existing client login.
- Allowed `node` commands resolve through a wrapper outside the fixture, forcing macOS `sandbox-exec`. The same sandbox runs independent checks. Node can read its fixture and installed system/runtime files, write its fixture except `node_modules`, and use only that AEO fixture's assigned loopback port. Other file contents, sibling arms and external network access are denied. The client itself retains network access for authenticated model requests.
- The AEO package and runtime dependencies are copied into each owned fixture without host symlinks. Their hashes are checked afterward. Each subprocess has a dedicated process group, terminated on completion or timeout.
- Candidate Node receives only `PATH`, fixture-local `HOME`/`TMPDIR`, `LANG` and `PILOT_HTTP_PORT`; macOS also supplies `__CF_USER_TEXT_ENCODING`. Claude gets a separate OS-variable allowlist and its existing login; API/token environment variables are excluded from the client and its shell tools.
- The only intended treatment is explicit skill text plus its local references in the user prompt. This measures following supplied instructions; native skill discovery and automatic routing are separate questions.
- Separate fixture copies, new sessions, no resume or cross-arm feedback. At most two concurrent target processes. The scheduled order is recorded in `protocol.json`.
- A 240-second deadline and reported API-budget limit of USD 2 per execution bound this pilot. The CLI's budget accounting is not a statement of what a subscription bills. Running it consumes the authenticated account's model usage.
- Independent Node checks run outside the candidate's editable source. Fixed fixture files are hash-checked. Incomplete execution, denied permissions, broken grading, or changed fixed files produce an unscored status.

## Tasks and observations

| Case | Editable source | Independent observations |
| --- | --- | --- |
| `gates` | `gate.mjs` | Valid samples pass; slow, missing, malformed and unavailable observations cannot pass |
| `gauntlet` | `route.mjs` | Response/order and input preservation; string edge cases; actual input property reads at most half the 16,440-read baseline |
| `aeo` | `config.mjs` | Exact existing robots/sitemap preserved; unpublished routes/content excluded; served public canonicals and parseable page JSON-LD |

The Gauntlet case measures property reads in a synthetic route, with a three-round task limit. It measures neither visual quality nor latency. A human or independent critic's review during the loop is outside the target sessions; any missing review must stay explicit in the report.

The AEO case uses the installed aeo.js 0.0.16 adapter against synthetic HTML and an ephemeral HTTP server. This is an adapter lifecycle check, separate from a complete Astro build, a public deployment, or search/citation outcomes. This installed version differs from the 0.0.17 source reference in the skill; both arms get the same installed package.

## Reproduce

Use macOS with `/usr/bin/sandbox-exec`, Node.js 20+, Python 3, the recorded Claude Code client/model, and an existing aeo.js 0.0.16 installation. No dependency is downloaded by this runner. Review the protocol and runner first.

From the collection root, set `aeo_package` to that installed package directory and choose new local output directories:

```sh
aeo_package=/absolute/path/to/node_modules/aeo.js
python3 evals/pilot/run.py --self-check --aeo-package "$aeo_package" \
  --output artifacts/pilot-runs/calibration
python3 evals/pilot/run.py --run --aeo-package "$aeo_package" \
  --protocol evals/pilot/protocol-v2.json --output artifacts/pilot-runs/run-2
```

`--self-check` spends no model usage. It grades the supplied defective state, applies a separate reference correction in the owned copy, and requires the corrected state to pass. `--run` starts the six model sessions and does not overwrite an existing output directory.

The local output records the protocol/runner/fixture hashes, source revision, prompts, raw event streams, tool calls, final responses, candidate files, observed model IDs, process status, independent checks, and measurements. Raw runs are ignored by Git. Publish a reviewed summary and synthetic evidence excerpts after execution; keep incomplete runs and ties visible. The separate 22-case evaluation plan in `../scenarios.json` remains unexecuted until run as specified there.
