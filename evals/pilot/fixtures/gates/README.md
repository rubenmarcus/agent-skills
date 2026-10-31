# Release gate

`gate(sample)` decides whether a release observation meets the contract.
A valid latency is a finite nonnegative number no greater than 200 milliseconds.
`response.participants` must be an array. An empty array is valid.
Missing or invalid observations must never pass. The exported function and
its `ok` boolean are consumed by the release script.

Run the existing smoke check with `node check.mjs`. You may change `gate.mjs`
and add focused checks or notes. Keep this README and check.mjs unchanged.
