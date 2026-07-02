---
name: ispark-browser-qa
description: Use when validating websites or web apps in a real browser, checking UI behavior, screenshots, console/network state, responsive layout, forms, deployments, canaries, benchmarks, or scraping.
---

# ISpark Browser QA

Use this whenever visual, frontend, or deployment behavior must be observed rather than inferred from code.

## Route

- Browser inspection and interaction: read `references/browser.md`.
- QA loop: read `references/qa.md`.
- Canary or post-deploy checks: read `references/canary.md`.
- Performance and scraping: read `references/perf-scrape.md`.

## Defaults

- Write QA reports and visual findings in Simplified Chinese unless the target issue, PR, or artifact explicitly requires another language.
- Store temporary screenshots, traces, HAR-like exports, and scrape outputs under `.tmp/` or `tmp/`; keep durable QA plans or audit notes under `working-delta/` when the repo uses it.
- Observe the real page.
- Check console and network when behavior depends on runtime state.
- Capture screenshots or concrete DOM/page observations for visual claims.
- If browser tooling is unavailable, mark frontend verification incomplete.
