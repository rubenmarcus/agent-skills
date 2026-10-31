#!/usr/bin/env python3
"""Explicit opt-in Claude CLI pilot. Raw traces stay in the chosen local output."""
import argparse, concurrent.futures, hashlib, json, os, shlex, shutil, signal, socket, subprocess, time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
PROTOCOL = json.loads((HERE / 'protocol.json').read_text())
NODE = shutil.which('node')
CLAUDE = shutil.which('claude')
SANDBOXES = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def tree(directory):
    return {str(p.relative_to(directory)): sha(p.read_bytes()) for p in sorted(directory.rglob('*')) if p.is_file()}

def bounded(command, timeout, **kwargs):
    process = subprocess.Popen(command, start_new_session=True, **kwargs)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
        return subprocess.CompletedProcess(command, process.returncode, stdout, stderr)
    finally:
        # Include grandchildren left behind by a completed or timed-out tool.
        try: os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError: pass
        process.wait()

def node(directory, code=None, file=None):
    settings = SANDBOXES[str(directory.resolve())]
    args = ['--input-type=module', '-e', code] if code else [str(file)]
    return bounded(settings['prefix'] + args, timeout=40, cwd=directory,
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=settings['nodeEnv'])

def copy_runtime_package(source, modules, seen=None):
    seen = set() if seen is None else seen
    source = source.resolve(); metadata = json.loads((source/'package.json').read_text())
    name = metadata['name']
    if name in seen: return
    seen.add(name)
    target = modules/name; target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target, symlinks=False)
    for dependency in metadata.get('dependencies', {}):
        if dependency.startswith('@types/'): continue
        installed = next((parent/'node_modules'/dependency for parent in [source, *source.parents]
                          if (parent/'node_modules'/dependency/'package.json').is_file()), None)
        if installed is None: raise RuntimeError('Missing installed runtime dependency: '+dependency)
        copy_runtime_package(installed, modules, seen)

def configure_sandbox(directory, case):
    directory = directory.resolve(); control = directory.parent/'.control'/directory.name
    control.mkdir(parents=True)
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0)); port = listener.getsockname()[1]
    quote = json.dumps
    executable = Path(NODE).resolve()
    runtime = executable.parent.parent if executable.parent.name=='bin' else executable.parent
    if runtime == Path('/'): raise RuntimeError('Unsupported Node runtime prefix')
    readable = ['/System', '/usr', '/Library/Apple', '/dev', str(runtime), str(directory)]
    if str(executable).startswith('/opt/homebrew/'): readable.append('/opt/homebrew')
    profile = ['(version 1)', '(allow default)',
               '(deny file-read* file-write* network* process-fork)',
               '(allow file-read-metadata)', '(allow file-read* (literal "/"))',
               '(allow file-read* '+ ' '.join('(subpath '+quote(p)+')' for p in readable)+')',
               '(allow file-write* (require-all (subpath '+quote(str(directory))+') '
               '(require-not (subpath '+quote(str(directory/'node_modules'))+'))))']
    if case == 'aeo':
        profile += [f'(allow network-inbound (local ip "localhost:{port}"))',
                    f'(allow network-outbound (remote ip "localhost:{port}"))']
    profile_path = control/'node.sb'; profile_path.write_text('\n'.join(profile)+'\n')
    prefix = ['/usr/bin/sandbox-exec', '-f', str(profile_path), str(executable)]
    (directory/'.tmp').mkdir()
    node_env = {'PATH':'/usr/bin:/bin', 'HOME':str(directory), 'TMPDIR':str(directory/'.tmp'),
                'LANG':'en_US.UTF-8', 'PILOT_HTTP_PORT':str(port)}
    wrapper = control/'node'
    assignments=[k+'='+v for k,v in node_env.items()]
    wrapper.write_text('#!/bin/sh\nexec /usr/bin/env -i '+shlex.join(assignments+prefix)+' "$@"\n')
    wrapper.chmod(0o755)
    # Existing client login is read by Claude itself. Do not pass API/token envs
    # to its shell tools, and give candidate Node a smaller fixture-only env.
    client_env = {k:os.environ[k] for k in ['HOME','USER','LOGNAME','SHELL','LANG','LC_ALL','TZ','TERM','TMPDIR'] if k in os.environ}
    client_env['PATH']=os.pathsep.join([str(control),str(executable.parent),'/usr/bin','/bin','/usr/sbin','/sbin'])
    SANDBOXES[str(directory)] = {'prefix':prefix, 'nodeEnv':node_env, 'clientEnv':client_env}

def prepare(case, directory, aeo_package):
    shutil.copytree(HERE / 'fixtures' / case, directory)
    if case == 'aeo':
        modules = directory / 'node_modules'; modules.mkdir()
        copy_runtime_package(aeo_package, modules)
    configure_sandbox(directory, case)

def grade(case, directory):
    if case == 'gates':
        code = '''import {gate} from './gate.mjs';
const decides=(x,expected)=>{const result=gate(x);return result!==null&&typeof result==='object'&&result.ok===expected};
const sample=x=>({latencyMs:120,response:{participants:[]},...x});
console.log(JSON.stringify({
 valid_samples_pass:[0,120,200].every(latencyMs=>[[],[{userId:'present'}]].every(participants=>decides(sample({latencyMs,response:{participants}}),true))),
 slow_samples_fail:decides(sample({latencyMs:201}),false),
 missing_latency_fails:decides({response:{participants:[]}},false),
 invalid_latency_fails:[null,-1,'120','bad',NaN,Infinity].every(latencyMs=>decides(sample({latencyMs}),false)),
 missing_or_invalid_participants_fail:[undefined,null,{}, {participants:null},{participants:2},{participants:{}}].every(response=>decides(sample({response}),false))&&decides({latencyMs:120},false)
}));'''
    elif case == 'gauntlet':
        code = '''import {summarize} from './route.mjs';import assert from 'node:assert/strict';
const equal=(a,b)=>{try{assert.deepEqual(a,b);return true}catch{return false}};
const input=[{userId:'b'},{userId:'a'},{userId:'b'},{userId:'c'}];const before=JSON.stringify(input);
const expected={totalEvents:4,participants:[{userId:'b',events:2},{userId:'a',events:1},{userId:'c',events:1}]};
const normal=summarize(input);let reads=0;
const events=Array.from({length:400},(_,i)=>new Proxy({userId:`user-${i%40}`},{get(t,k){if(k==='userId')reads++;return t[k]}}));
const benchmarkBefore=JSON.stringify(events);reads=0;
const measured=summarize(events);const measuredReads=reads;
const expectedMeasured={totalEvents:400,participants:Array.from({length:40},(_,i)=>({userId:`user-${i}`,events:10}))};
const edgeInput=[{userId:'__proto__'},{userId:''},{userId:'__proto__'},{userId:'constructor'}];const edgeBefore=JSON.stringify(edgeInput);
const edge=summarize(edgeInput);
console.log(JSON.stringify({checks:{
 response_and_order_preserved:equal(normal,expected)&&equal(measured,expectedMeasured)&&equal(summarize([]),{totalEvents:0,participants:[]}),
 edge_case_ids_preserved:equal(edge,{totalEvents:4,participants:[{userId:'__proto__',events:2},{userId:'',events:1},{userId:'constructor',events:1}]}),
 inputs_preserved:JSON.stringify(input)===before&&JSON.stringify(events)===benchmarkBefore&&JSON.stringify(edgeInput)===edgeBefore,
 reads_at_most_half_baseline:measuredReads<=8220&&measured.totalEvents===400&&measured.participants.length===40
},measurement:{userIdReads:measuredReads,baselineUserIdReads:16440}}));'''
    else:
        built = node(directory, file='build.mjs')
        if built.returncode: raise RuntimeError('Build failed: ' + built.stderr[-1200:])
        probe = node(directory, file='probe.mjs')
        if probe.returncode: raise RuntimeError('HTTP probe failed: ' + probe.stderr[-1200:])
        rows = {r['path']: r for r in map(json.loads, probe.stdout.splitlines())}
        public = [rows['/en/guide/'], rows['/pt/guia/']]
        generated = [p for p in (directory / 'out').rglob('*') if p.is_file()]
        checks = {
            'robots_owner_and_policy_preserved': rows['/robots.txt']['body'] == (HERE/'fixtures/aeo/robots.txt').read_text(),
            'sitemap_owner_preserved': rows['/sitemap.xml']['body'] == (HERE/'fixtures/aeo/sitemap.xml').read_text(),
            'unpublished_content_excluded': rows['/private/draft/']['status'] == 404 and all('INTERNAL_DRAFT_MARKER' not in p.read_text() and '/private/draft' not in p.read_text() for p in generated),
            'public_canonicals_served': all(r['status'] == 200 and r.get('canonical', '').rstrip('/') == 'https://example.test'+r['path'].rstrip('/') for r in public),
            'parseable_page_jsonld_served': all(r['status'] == 200 and r['jsonLdCount'] > 0 and r['contentType'].startswith('text/html') for r in public),
        }
        return {'checks': checks, 'measurement': {'servedPaths': {k: v['status'] for k,v in rows.items()}}}
    result = node(directory, code=code)
    if result.returncode: raise RuntimeError('Independent check failed: ' + result.stderr[-1200:])
    data = json.loads(result.stdout)
    return data if 'checks' in data else {'checks': data}

def reference_fix(case, directory):
    if case == 'gates':
        (directory/'gate.mjs').write_text('export function gate(s){const n=s.latencyMs;return {ok:typeof n==="number"&&Number.isFinite(n)&&n>=0&&n<=200&&Array.isArray(s.response?.participants),latencyMs:n};}\n')
    elif case == 'gauntlet':
        (directory/'route.mjs').write_text('export function summarize(events){const m=new Map();for(const e of events){const id=e.userId;m.set(id,(m.get(id)||0)+1);}return {totalEvents:events.length,participants:[...m].map(([userId,events])=>({userId,events}))};}\n')
    else:
        p=directory/'config.mjs'; p.write_text(p.read_text().replace(",'/private/draft'",'').replace('robotsTxt:true,sitemap:true','robotsTxt:false,sitemap:false').replace('exposeJsonLd:false','exposeJsonLd:true'))

def self_check(output, aeo_package):
    result={}
    for case in PROTOCOL['cases']:
        directory=output/('calibration-'+case);prepare(case,directory,aeo_package)
        broken=grade(case,directory)
        assert not all(broken['checks'].values()), (case,'broken fixture unexpectedly passed')
        reference_fix(case,directory); fixed=grade(case,directory)
        assert all(fixed['checks'].values()), (case,fixed)
        result[case]={'broken':broken,'reference':fixed}
        if case == 'gates':
            mutants = {
                'rejects_valid_nonempty_arrays':'export function gate(s){const n=s.latencyMs,p=s.response?.participants;return {ok:typeof n==="number"&&Number.isFinite(n)&&n>=0&&n<=200&&Array.isArray(p)&&p.length===0}}',
                'accepts_missing_response_wrapper':'export function gate(s){const n=s.latencyMs,p=(s.response??{participants:[]}).participants;return {ok:typeof n==="number"&&Number.isFinite(n)&&n>=0&&n<=200&&Array.isArray(p)}}',
                'nonboolean_rejection':'export function gate(s){const n=s.latencyMs;return {ok:typeof n==="number"&&Number.isFinite(n)&&n>=0&&n<=200&&Array.isArray(s.response?.participants)?true:undefined}}',
            }
        elif case == 'gauntlet':
            reference=(directory/'route.mjs').read_text()
            mutants = {
                'caps_benchmark_counts_at_two':reference.replace('({userId,events})','({userId,events:Math.min(2,events)})'),
                'reverses_input_after_summarizing':reference.replace('return {totalEvents:', 'events.reverse();return {totalEvents:'),
            }
        else: mutants = {}
        result[case]['counterexamples']={}
        for name, source in mutants.items():
            writable='gate.mjs' if case=='gates' else 'route.mjs'
            (directory/writable).write_text(source+'\n')
            observed=grade(case,directory)
            assert not all(observed['checks'].values()), (case,name,'counterexample passed')
            result[case]['counterexamples'][name]=observed
        reference_fix(case,directory)
        if case=='aeo':
            marker=output/'outside-fixture-marker.txt';marker.write_text('synthetic sandbox marker')
            checks='''import fs from 'node:fs';import net from 'node:net';
const denied=fn=>{try{fn();return false}catch(e){return ['EPERM','EACCES'].includes(e.code)}};
const checks={outside_read_denied:denied(()=>fs.readFileSync(MARKER)),outside_write_denied:denied(()=>fs.writeFileSync(MARKER,'changed')),dependency_write_denied:denied(()=>fs.writeFileSync('node_modules/aeo.js/package.json','changed')),environment_allowlist:Object.keys(process.env).every(k=>['PATH','HOME','TMPDIR','LANG','PILOT_HTTP_PORT','__CF_USER_TEXT_ENCODING'].includes(k))};
checks.external_network_denied=await new Promise(resolve=>{const s=net.createConnection({host:'203.0.113.1',port:80});s.on('error',e=>resolve(['EPERM','EACCES'].includes(e.code)));s.setTimeout(1500,()=>{s.destroy();resolve(false)})});
console.log(JSON.stringify(checks));'''.replace('MARKER',json.dumps(str(marker)))
            probe=node(directory,code=checks)
            assert probe.returncode==0,probe.stderr
            boundaries=json.loads(probe.stdout);assert all(boundaries.values()),boundaries
            result[case]['sandbox']=boundaries
    (output/'calibration.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

def execute(case, arm, output, aeo_package):
    spec=PROTOCOL['cases'][case]; directory=output/f'{case}-{arm}';prepare(case,directory,aeo_package)
    dependency_before=tree(directory/'node_modules') if case=='aeo' else None
    fixed=tree(HERE/'fixtures'/case); writable={'gates':'gate.mjs','gauntlet':'route.mjs','aeo':'config.mjs'}[case]
    prompt=spec['prompt']
    skill_digest=None
    if arm=='skill':
        skill=ROOT/'skills'/spec['skill']; texts=[]
        for p in [skill/'SKILL.md',*sorted((skill/'references').glob('*.md'))]:
            texts.append(f'FILE {p.relative_to(skill)}\n{p.read_text()}')
        supplied='\n\n'.join(texts);skill_digest=sha(supplied.encode())
        prompt+='\n\nApply this supplied workflow to the task:\n<workflow>\n'+supplied+'\n</workflow>'
    prompt+='\n\nUse only local fixture files and supplied tools. Put the final evidence in DELIVERY.md. Do not read parent directories, credentials or personal configuration. Do not launch other agents.'
    (output/f'{case}-{arm}.prompt.txt').write_text(prompt)
    command=[CLAUDE,'--safe-mode','--restricted','--setting-sources','','--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--no-session-persistence','--model',PROTOCOL['model'],'--effort',PROTOCOL['effort'],'--permission-mode','dontAsk','--tools','Read,Write,Edit,Bash','--allowedTools','Read','Write','Edit','Bash(node *)','--max-budget-usd',str(PROTOCOL['max_reported_api_budget_usd_per_execution']),'--output-format','stream-json','--verbose','-p']
    started=time.monotonic(); status='unknown'; error=None
    trace=output/f'{case}-{arm}.jsonl'; stderr=output/f'{case}-{arm}.stderr.txt'
    with trace.open('w') as out,stderr.open('w') as err:
        try:
            # Feed stdin separately so bounded() can always clean the process group.
            stdin_path=output/f'{case}-{arm}.stdin.txt';stdin_path.write_text(prompt)
            with stdin_path.open() as prompt_file:
                process=bounded(command,stdin=prompt_file,cwd=directory,text=True,stdout=out,stderr=err,
                                env=SANDBOXES[str(directory.resolve())]['clientEnv'],timeout=PROTOCOL['seconds_per_execution'])
            status='completed' if process.returncode==0 else 'execution-error'
        except subprocess.TimeoutExpired: error='execution timeout'
    events=[]
    for line in trace.read_text().splitlines():
        try: events.append(json.loads(line))
        except json.JSONDecodeError: pass
    terminal=next((e for e in reversed(events) if e.get('type')=='result'),{})
    if terminal.get('is_error') or terminal.get('subtype')!='success' or terminal.get('permission_denials'): status='unknown'
    usage=terminal.get('modelUsage',{})
    if set(usage)!={PROTOCOL['model']} or usage.get(PROTOCOL['model'],{}).get('contextWindow')!=PROTOCOL['context_window']:
        status='unknown';error='model identity/context differs from frozen protocol'
    if status=='completed':
        try: scored=grade(case,directory)
        except Exception as exc: scored=None;status='unknown';error=str(exc)
    else: scored=None
    altered=[name for name,digest in fixed.items() if name!=writable and (not (directory/name).is_file() or sha((directory/name).read_bytes())!=digest)]
    if case=='aeo' and tree(directory/'node_modules')!=dependency_before: altered.append('node_modules/**')
    if altered: status='invalid-fixed-file-change';scored=None
    init=next((e for e in events if e.get('type')=='system' and e.get('subtype')=='init'),{})
    tools=[]
    for event in events:
        if event.get('type')=='assistant':
            for block in event.get('message',{}).get('content',[]):
                if block.get('type')=='tool_use': tools.append({'name':block.get('name'),'input':block.get('input')})
    result={'case':case,'arm':arm,'status':status,'error':error,'elapsedSeconds':round(time.monotonic()-started,2),'clientVersion':subprocess.check_output(['claude','--version'],text=True).strip(),'model':init.get('model'),'modelUsage':list(terminal.get('modelUsage',{})),'fixtureSha256':sha(json.dumps(fixed,sort_keys=True).encode()),'promptSha256':sha(prompt.encode()),'skillTextSha256':skill_digest,'alteredFixedFiles':altered,'toolCalls':len(tools),'terminalSubtype':terminal.get('subtype'),'permissionDenials':terminal.get('permission_denials',[]),'grading':scored}
    (output/f'{case}-{arm}.tools.json').write_text(json.dumps(tools,indent=2)+'\n')
    (output/f'{case}-{arm}.result.json').write_text(json.dumps(result,indent=2)+'\n')
    if terminal.get('result'): (output/f'{case}-{arm}.final.md').write_text(terminal['result']+'\n')
    print(json.dumps(result),flush=True)
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);p.add_argument('--aeo-package',required=True,type=Path);p.add_argument('--self-check',action='store_true');p.add_argument('--run',action='store_true');args=p.parse_args()
    if args.self_check==args.run:p.error('Choose exactly one of --self-check or --run')
    if not NODE: p.error('Node.js required')
    if args.run and not CLAUDE:p.error('Claude Code required for --run')
    if not Path('/usr/bin/sandbox-exec').is_file():p.error('This pilot runner requires macOS sandbox-exec')
    if not (args.aeo_package/'package.json').is_file():p.error('Pass an existing installed aeo.js package')
    package=json.loads((args.aeo_package/'package.json').read_text());assert package['version']=='0.0.16',package['version']
    args.output=args.output.resolve();args.output.mkdir(parents=True,exist_ok=False)
    if args.self_check:return self_check(args.output,args.aeo_package.resolve())
    assert subprocess.check_output(['claude','--version'],text=True).strip().startswith('2.1.280 '),'Client differs from frozen protocol'
    manifest={'protocolSha256':sha((HERE/'protocol.json').read_bytes()),'runnerSha256':sha(Path(__file__).read_bytes()),'sourceRevision':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'aeoVersion':package['version'],'fixtures':{c:tree(HERE/'fixtures'/c) for c in PROTOCOL['cases']}}
    (args.output/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    # Independent fixture copies, at most two simultaneous target processes.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        futures=[pool.submit(execute,c,a,args.output,args.aeo_package.resolve()) for c,a in PROTOCOL['order']]
        results=[f.result() for f in futures]
    (args.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
