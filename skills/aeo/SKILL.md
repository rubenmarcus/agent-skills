---
name: aeo
description: Audit and implement answer-engine discovery using aeo.js, crawler policy, canonical identity, structured data, and machine-readable content. Use for AEO/GEO audits, llms.txt, AI crawler access, or integrating aeo.js into a website.
---

# AEO with aeo.js

Make the site's intended public content discoverable and attributable, then verify the actual output. Read [the aeo.js reference](references/aeojs.md) for verified commands and API examples.

## Audit before changing

Identify framework, installed aeo.js version, canonical origin, locales, build output, existing robots/sitemap owners, structured data, and intended crawler policy.

Run the installed CLI's help before relying on options. Prefer the project's pinned dependency. For a URL audit, use the documented check/report command or available AEO MCP tools. Save the timestamp and relevant baseline findings.

If package acquisition is needed, follow the project's package manager and dependency policy. Do not execute an unreviewed remote install script.

Inspect both source and served behavior: status, redirect target, content type, canonical URL, indexability, crawler directives, and availability of the relevant metadata or content. Distinguish static inspection from runtime verification.

## Implement the smallest useful integration

Use the framework adapter or CLI that fits the existing build. Compose with current configuration rather than replacing it.

Preserve explicit robots restrictions. Search crawling, retrieval, and model training may have different policies; do not broadly enable crawlers to improve a score. If existing tooling owns robots or the sitemap, keep that owner and disable the overlapping generator.

Populate titles, identity, organization, authorship, dates, and relationships from verified project data. Do not invent reviews, credentials, contacts, or schema claims.

Generate only intended public content. Exclude private routes, secrets, signed URLs, and unpublished material from machine-readable exports.

## Verify end to end

Run the relevant build. Inspect generated files and the site's actual injection path for structured data. A schema.json file alone does not prove that a page exposes that schema.

Check canonical and localized URLs, robots.txt, sitemap.xml, llms.txt, and other enabled surfaces. Compare the resulting URLs against real routes and check for duplicate or conflicting generators.

When an authorized preview or deployment is available, verify served HTTP responses there and rerun the audit. Deployment itself requires the user's actual authorization.

## Report the limit

Report observed defects fixed, commands and revision, before/after evidence, and pending checks. A readiness score is a tool diagnostic; it does not establish search placement, citations in answers, or traffic gains.

llms.txt and related discovery conventions do not replace access control or guarantee that a crawler follows a policy.
