import {mkdirSync,rmSync,readFileSync,writeFileSync} from 'node:fs';
import {join} from 'node:path';
import {pathToFileURL} from 'node:url';
import {aeoAstroIntegration} from 'aeo.js/astro';
import config from './config.mjs';
const out=join(process.cwd(),'out');rmSync(out,{recursive:true,force:true});mkdirSync(out,{recursive:true});
for(const route of config.routes){
 const dir=join(out,route);mkdirSync(dir,{recursive:true});
 const lang=route.startsWith('/pt/')?'pt-BR':'en';
 const text=route.startsWith('/private/')?'INTERNAL_DRAFT_MARKER':'Public fixture guide';
 writeFileSync(join(dir,'index.html'),`<!doctype html><html lang="${lang}"><head><title>Fixture guide</title></head><body><main><h1>${text}</h1><p>Synthetic discovery fixture.</p></main></body></html>`);
}
for(const name of ['robots.txt','sitemap.xml'])writeFileSync(join(out,name),readFileSync(name));
const adapter=aeoAstroIntegration({url:config.origin,title:'Synthetic guides',generators:config.generators,widget:{enabled:false}});
const astro={outDir:pathToFileURL(out+'/'),publicDir:pathToFileURL(process.cwd()+'/'),site:config.origin};
adapter.hooks['astro:config:setup']({config:astro,command:'build'});
const errors=[];const logger={fork:()=>logger,info:()=>{},debug:()=>{},error:m=>errors.push(m)};
await adapter.hooks['astro:build:done']({dir:astro.outDir,logger});
if(errors.length)throw Error(JSON.stringify(errors));
if(!config.exposeJsonLd) for(const route of config.routes){
 const file=join(out,route,'index.html');
 writeFileSync(file,readFileSync(file,'utf8').replace(/<script[^>]*type="application\/ld\+json"[^>]*>[\s\S]*?<\/script>/g,''));
}
console.log('Synthetic adapter lifecycle complete; not a full Astro build.');
