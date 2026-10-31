import { summarize } from './route.mjs';
let reads=0;
const events=Array.from({length:400},(_,i)=>new Proxy({userId:`user-${i%40}`},{get(target,key){if(key==='userId') reads++;return target[key];}}));
const result=summarize(events);
console.log(JSON.stringify({userIdReads:reads,totalEvents:result.totalEvents,participants:result.participants.length}));
