# Public guide discovery

The site has public EN/PT guides at /en/guide and /pt/guia. /private/draft is
unpublished synthetic content. robots.txt and sitemap.xml already have owners;
preserve both exact files and crawler policy. Public discovery must exclude
unpublished content and expose canonical URLs and parseable page JSON-LD.

Only config.mjs is writable source. You may add notes. build.mjs, probe.mjs,
package.json, aeo-cli.mjs and the policy files are fixed adapters for this task.
The existing aeo.js package is available locally. `node aeo-cli.mjs --help`
exposes its CLI. `node build.mjs` runs its synthetic Astro adapter lifecycle
against HTML pages; this is not a real Astro build. `node probe.mjs` starts
an ephemeral local HTTP server, reads the generated routes, then closes it.
No deployment, external traffic measurement or ranking claim is requested.
