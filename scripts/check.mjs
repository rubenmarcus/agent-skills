import assert from 'node:assert/strict';
import { existsSync, lstatSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, isAbsolute, join, relative, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = (path) => readFileSync(join(root, path), 'utf8');
const json = (path) => JSON.parse(read(path));
const within = (base, path) => {
  const rel = relative(base, path);
  return rel !== '..' && !rel.startsWith('../') && !isAbsolute(rel);
};

function filesIn(dir) {
  return readdirSync(dir).sort().flatMap((name) => {
    const path = join(dir, name);
    const stat = lstatSync(path);
    assert(!stat.isSymbolicLink(), `Package contains symlink: ${relative(root, path)}`);
    return stat.isDirectory() ? filesIn(path) : [path];
  });
}

// This collection intentionally uses only scalar name/description frontmatter.
function frontmatter(text, file) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  assert(match, `Missing frontmatter: ${file}`);
  const result = {};
  for (const line of match[1].split(/\r?\n/)) {
    const pair = line.match(/^(name|description): (.+)$/);
    assert(pair, `Unsupported metadata line in ${file}`);
    assert(!(pair[1] in result), `Duplicate metadata field in ${file}`);
    result[pair[1]] = pair[2].startsWith('"') ? JSON.parse(pair[2]) : pair[2];
  }
  return result;
}

function checkLinks(path, boundary) {
  const text = readFileSync(path, 'utf8');
  for (const match of text.matchAll(/\[[^\]]*\]\(([^)\s]+)\)/g)) {
    const href = match[1];
    if (/^(?:https?:|mailto:|#)/.test(href)) continue;
    const target = resolve(dirname(path), decodeURIComponent(href.split('#')[0]));
    assert(within(boundary, target), `Escaping reference in ${relative(root, path)}: ${href}`);
    assert(existsSync(target), `Missing reference in ${relative(root, path)}: ${href}`);
  }
}

const pkg = json('package.json');
const portable = json('plugin.json');
const claude = json('.claude-plugin/plugin.json');
const marketplace = json('.claude-plugin/marketplace.json');
assert.equal(pkg.private, true, 'npm publication must remain disabled during preparation');
assert.match(pkg.version, /^\d+\.\d+\.\d+$/);
assert.equal(portable.version, pkg.version);
assert.equal(claude.version, pkg.version);
assert.equal(portable.name, claude.name);
assert.equal(portable.license, pkg.license);
assert.equal(claude.license, pkg.license);
assert.equal(portable.$schema, 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json');
assert.equal(claude.skills, './skills/');
assert.equal(marketplace.plugins.length, 1);
assert.equal(marketplace.plugins[0].name, portable.name);
assert.equal(marketplace.plugins[0].source, './');
assert(!('hooks' in claude) && !('mcpServers' in claude), 'No automatic runtime dependencies');

const skillsRoot = join(root, 'skills');
const names = readdirSync(skillsRoot).sort();
assert(names.length > 0, 'No skills found');
let packagedFileCount = 0;
for (const name of names) {
  const dir = join(skillsRoot, name);
  assert(lstatSync(dir).isDirectory(), `Unexpected skills entry: ${name}`);
  assert.match(name, /^[a-z0-9]+(?:-[a-z0-9]+)*$/);
  const content = read(`skills/${name}/SKILL.md`);
  const meta = frontmatter(content, name);
  assert.equal(meta.name, name);
  assert(meta.description?.length >= 40 && meta.description.length <= 1024, `Description: ${name}`);
  assert(content.split('\n').length < 500, `Move long material into references: ${name}`);
  assert(!/\bTODO\b|\[INSERT|\[REPLACE/.test(content), `Unfinished template: ${name}`);
  const ui = read(`skills/${name}/agents/openai.yaml`);
  for (const key of ['display_name', 'short_description']) {
    const value = ui.match(new RegExp(`^  ${key}: (.+)$`, 'm'))?.[1];
    assert(value?.startsWith('"'), `Quoted UI field missing: ${name}/${key}`);
    const decoded = JSON.parse(value);
    assert.equal(typeof decoded, 'string');
    if (key === 'short_description') assert(decoded.length >= 25 && decoded.length <= 64, name);
  }
  for (const path of filesIn(dir)) {
    packagedFileCount += 1;
    assert(!/\.(?:pem|key|p12|sqlite|db)$/i.test(path), `Unexpected private artifact: ${path}`);
    const text = readFileSync(path, 'utf8');
    assert(!/\/(?:Users|Volumes)\//.test(text), `Machine-local dependency in ${relative(root, path)}`);
    if (path.endsWith('.md')) checkLinks(path, dir);
  }
  assert(read('README.md').includes(`skills/${name}/SKILL.md`), `Missing catalog entry: ${name}`);
}

const scenarios = json('evals/scenarios.json');
assert.equal(scenarios.status, 'not-run');
const ids = new Set();
for (const item of scenarios.cases) {
  assert(names.includes(item.skill), `Unknown scenario skill: ${item.skill}`);
  assert(!ids.has(item.id), `Duplicate scenario: ${item.id}`);
  ids.add(item.id);
  assert(['task', 'boundary'].includes(item.kind));
  assert(item.prompt && item.expected.length > 0, `Incomplete scenario: ${item.id}`);
}
for (const name of names) {
  for (const kind of ['task', 'boundary']) {
    assert(scenarios.cases.some((item) => item.skill === name && item.kind === kind), `${name}: ${kind}`);
  }
}
for (const entry of pkg.files) {
  assert(!isAbsolute(entry) && within(root, resolve(root, entry)), `Unsafe package entry: ${entry}`);
  assert(existsSync(join(root, entry)), `Missing package entry: ${entry}`);
}
for (const path of ['README.md', 'PROVENANCE.md']) checkLinks(join(root, path), root);
console.log(`Checked ${names.length} skills, ${packagedFileCount} skill files, manifests, links, and ${ids.size} unexecuted evaluation cases.`);
