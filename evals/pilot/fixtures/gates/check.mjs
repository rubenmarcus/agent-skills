import assert from 'node:assert/strict';
import { gate } from './gate.mjs';
assert.equal(gate({latencyMs:120,response:{participants:[]}}).ok,true);
console.log('Existing valid-sample test passed');
