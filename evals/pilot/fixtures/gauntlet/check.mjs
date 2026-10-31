import assert from 'node:assert/strict';
import { summarize } from './route.mjs';
assert.deepEqual(summarize([{userId:'b'},{userId:'a'},{userId:'b'}]), {
 totalEvents:3,participants:[{userId:'b',events:2},{userId:'a',events:1}]
});
assert.deepEqual(summarize([]),{totalEvents:0,participants:[]});
console.log('Response contracts passed');
