# Verified aeo.js surface

Inspected package: `aeo.js` 0.0.17, source revision `9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1`. Verify the installed package before adapting these examples.

At this revision, `package.json` says 0.0.17 while the exported `VERSION` constant, and consequently CLI help, says 0.0.14. Record the source revision or installed package metadata alongside the printed CLI version.

- [CLI implementation](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/src/cli.ts)
- [Configuration types](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/src/types.ts)
- [Framework examples](https://github.com/rubenmarcus/aeo.js/blob/9955ce8d9ee77d9ca0c6cd4e26e047a1081697a1/README.md)
- [Documentation](https://aeojs.org)

## Installed CLI

From a project where the dependency is already available:

```sh
npx --no-install aeo.js --help
npx --no-install aeo.js check https://example.com --json
npx --no-install aeo.js report https://example.com
```

Replace the example origin with the user's target. URL checks require network access. A local check without a URL inspects local configuration and output; it does not establish what production serves.

Generation writes files. In an owned scratch directory or after inspecting existing output ownership:

```sh
npx --no-install aeo.js generate --url https://example.com --title "Example documentation" --out ./public --no-widget
```

`init --yes` also generates output. `init --force` overwrites configuration. Neither belongs in a read-only audit.

## Astro integration

For an existing Astro configuration, compose the integration with its current settings:

```js
import { aeoAstroIntegration } from 'aeo.js/astro';

const aeo = aeoAstroIntegration({
  title: 'Example documentation',
  url: 'https://example.com',
  generators: { robotsTxt: false, sitemap: false },
  widget: { enabled: false },
});
```

Add `aeo` to the existing integrations array. The disabled generators illustrate preserving a robots/sitemap owner; choose them from the actual project. Source content and identity must come from verified project data.

Other supported adapters and their configuration are documented upstream. Inspect their actual exports and build lifecycle rather than pasting the Astro shape into another framework.

## Verification evidence

Record build revision, enabled generators, canonical origin, output paths, route checks, and served HTTP observations. Check HTML injection when JSON-LD is required; generating a separate schema file alone is insufficient.

Keep crawler permissions and discovery outcomes separate. A diagnostic score is not evidence of ranking, answer citations, or conversion.
