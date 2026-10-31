# Participant summary

The response preserves first-seen user order, exact user IDs and event counts.
User IDs are strings, including empty strings and property-like names such as
`__proto__`. Callers may reuse the input after a request, so preserve it.

Reduce userId property reads by at least half versus the supplied baseline on
`node benchmark.mjs`. The counter measures actual reads of input properties,
not latency or frame rate. Preserve all response contracts. Use at most three
candidate rounds. You may change route.mjs and add checks/notes; preserve the
supplied benchmark and check.mjs. Run `node check.mjs` for existing contracts.
