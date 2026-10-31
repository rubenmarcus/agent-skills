import {createRequire} from 'node:module';
import {dirname,join} from 'node:path';
import {pathToFileURL} from 'node:url';
const require=createRequire(import.meta.url);
await import(pathToFileURL(join(dirname(require.resolve('aeo.js')),'cli.mjs')));
