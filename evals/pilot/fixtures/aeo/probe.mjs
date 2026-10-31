import {createServer} from 'node:http';
import {readFileSync,existsSync,statSync} from 'node:fs';
import {resolve,join} from 'node:path';
const root=resolve('out');
const server=createServer((req,res)=>{
 const path=decodeURIComponent(new URL(req.url,'http://fixture').pathname);
 let file=resolve(root,'.'+path);
 if(!file.startsWith(root+'/')){res.writeHead(404);res.end();return;}
 if(existsSync(file)&&statSync(file).isDirectory())file=join(file,'index.html');
 if(!existsSync(file)){res.writeHead(404);res.end();return;}
 res.setHeader('Content-Type',file.endsWith('.html')?'text/html':file.endsWith('.json')?'application/json':file.endsWith('.xml')?'application/xml':'text/plain');
 res.end(readFileSync(file));
});
await new Promise(done=>server.listen(Number(process.env.PILOT_HTTP_PORT)||0,'127.0.0.1',done));
try{
 const origin=`http://127.0.0.1:${server.address().port}`;
 for(const path of ['/en/guide/','/pt/guia/','/private/draft/','/robots.txt','/sitemap.xml','/llms.txt']){
  const response=await fetch(origin+path);const body=await response.text();
  const jsonLd=[...body.matchAll(/<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)].map(m=>JSON.parse(m[1]));
  console.log(JSON.stringify({path,status:response.status,contentType:response.headers.get('content-type'),canonical:body.match(/rel="canonical"[^>]*href="([^"]+)"/)?.[1],jsonLdCount:jsonLd.length,body}));
 }
}finally{await new Promise(done=>server.close(done));}
