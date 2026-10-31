// Optional source-based fixture. No network, dependency install, or source writes.
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

assert(process.argv[2], 'Pass an existing aeo.js source checkout with esbuild installed');
const source = resolve(process.argv[2]);
const requireSource = createRequire(join(source, 'package.json'));
const { build } = requireSource('esbuild');
const metadata = requireSource('./package.json');
const revision = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: source, encoding: 'utf8' }).trim();
assert.equal(execFileSync('git', ['status', '--porcelain'], { cwd: source, encoding: 'utf8' }).trim(), '', 'Use a clean source revision');
const scratch = mkdtempSync(join(tmpdir(), 'agent-skills-aeo-'));
const originalCwd = process.cwd();
let server;
try {
  const cli = join(scratch, 'cli.cjs');
  const astro = join(scratch, 'astro.cjs');
  for (const [entry, outfile] of [['src/cli.ts', cli], ['src/plugins/astro.ts', astro]]) {
    await build({ entryPoints: [join(source, entry)], outfile, bundle: true, platform: 'node', format: 'cjs', logLevel: 'silent' });
  }
  const fixture = join(scratch, 'site');
  mkdirSync(fixture);
  writeFileSync(join(fixture, 'package.json'), JSON.stringify({ name: 'aeo-fixture', private: true }));
  const run = (...args) => execFileSync(process.execPath, [cli, ...args], { cwd: fixture, encoding: 'utf8', timeout: 15000 });
  const help = run('--help');
  assert(help.includes('--no-widget') && help.includes('check [url]'));
  const printedVersion = run('--version').trim();
  run('generate', '--url', 'https://example.com', '--title', 'Example documentation', '--out', './public', '--no-widget');
  for (const file of ['robots.txt', 'llms.txt', 'sitemap.xml', 'schema.json']) {
    assert(readFileSync(join(fixture, 'public', file), 'utf8').length > 0, file);
  }
  const audit = JSON.parse(run('check', '--out', './public', '--url', 'https://example.com', '--json'));
  assert(audit.audit && audit.config.url === 'https://example.com');

  // Exercise the documented adapter options on synthetic built HTML. This is
  // an adapter lifecycle fixture, not a real Astro build or deployment.
  process.chdir(fixture);
  const output = join(fixture, 'adapter-output');
  mkdirSync(output);
  writeFileSync(join(output, 'index.html'), '<!doctype html><html><head><title>Example documentation</title></head><body><main><h1>Public guide</h1><p>Fixture content only.</p></main></body></html>');
  const robots = 'User-agent: ExampleBot\nDisallow: /private\n';
  const sitemap = '<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.com/</loc></url></urlset>';
  writeFileSync(join(output, 'robots.txt'), robots);
  writeFileSync(join(output, 'sitemap.xml'), sitemap);
  const { aeoAstroIntegration } = createRequire(import.meta.url)(astro);
  const integration = aeoAstroIntegration({ title: 'Example documentation', url: 'https://example.com', generators: { robotsTxt: false, sitemap: false }, widget: { enabled: false } });
  const config = { outDir: pathToFileURL(output + '/'), publicDir: pathToFileURL(join(fixture, 'public') + '/'), site: 'https://example.com' };
  integration.hooks['astro:config:setup']({ config, command: 'build' });
  const errors = [];
  const logger = { fork: () => logger, info: () => {}, debug: () => {}, error: (message) => errors.push(message) };
  await integration.hooks['astro:build:done']({ dir: config.outDir, logger });
  assert.deepEqual(errors, []);
  assert.equal(readFileSync(join(output, 'robots.txt'), 'utf8'), robots);
  assert.equal(readFileSync(join(output, 'sitemap.xml'), 'utf8'), sitemap);

  const servedFiles = new Map([['/', 'index.html'], ['/robots.txt', 'robots.txt'], ['/sitemap.xml', 'sitemap.xml'], ['/llms.txt', 'llms.txt']]);
  server = createServer((req, res) => {
    const file = servedFiles.get(req.url);
    if (!file) { res.writeHead(404); res.end(); return; }
    res.setHeader('Content-Type', file.endsWith('.html') ? 'text/html; charset=utf-8' : file.endsWith('.xml') ? 'application/xml' : 'text/plain; charset=utf-8');
    res.end(readFileSync(join(output, file)));
  });
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  const origin = `http://127.0.0.1:${server.address().port}`;
  const page = await fetch(origin);
  assert.equal(page.status, 200);
  assert(page.headers.get('content-type').includes('text/html'));
  const html = await page.text();
  assert(/rel="canonical"[^>]*href="https:\/\/example.com\/?"/.test(html), 'Canonical injection');
  assert(html.includes('application/ld+json'), 'JSON-LD injection');
  for (const [, data] of html.matchAll(/<script[^>]*type="application\/ld\+json"[^>]*>([\s\S]*?)<\/script>/g)) JSON.parse(data);
  assert.equal(await (await fetch(`${origin}/robots.txt`)).text(), robots);
  assert.equal(await (await fetch(`${origin}/sitemap.xml`)).text(), sitemap);
  assert((await (await fetch(`${origin}/llms.txt`)).text()).includes('https://example.com'));
  console.log(JSON.stringify({ revision, packageVersion: metadata.version, printedVersion, passed: ['CLI generation', 'local JSON audit', 'documented Astro options', 'existing robots/sitemap preserved', 'served canonical and parseable JSON-LD', 'served discovery files'], scope: 'synthetic CLI and adapter lifecycle fixture; no real Astro build, deployment, or ranking test' }, null, 2));
} finally {
  if (server?.listening) await new Promise((done) => server.close(done));
  process.chdir(originalCwd);
  rmSync(scratch, { recursive: true, force: true });
}
