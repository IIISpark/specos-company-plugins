# Academic Preservation Checks

Run these checks before delivering a rewrite or edited manuscript. Use the manuscript's native format and the target project's own lint/build commands when available.

## Literal and notation closure

Compare source and revision for:

- citation commands, citation keys, author-year or numbered references, and the scope of each citation;
- LaTeX commands, labels, references, equations, variables, subscripts, units, and mathematical operators;
- figure/table numbers, section names, dataset and model names, code spans, Markdown tables, and placeholders;
- numbers, percentages, sample sizes, baselines, dates, intervals, and denominator wording.

Any missing, added, or moved literal is a review finding until the author explicitly requests that change.

## Claim and argument checks

- A result sentence still says what the source measured, under the same conditions and population.
- `may`, `suggests`, `associated with`, `under the tested conditions`, and stated limitations remain appropriately cautious.
- Citation placement still supports the same proposition; do not move a citation across a sentence boundary merely to improve flow.
- Method statements remain reproducible, result statements remain observational where appropriate, and discussion statements do not become causal claims by grammatical polish.
- Terminology map entries are stable across the edited section and any adjacent section touched by the change.

## Output and flags

For direct rewriting, provide a clean version and concise notes for material changes. For an audit-only request, do not edit. Flag instead of silently fixing when a citation's scope is unclear, a translation has multiple accepted forms, a result lacks support for its modality, or the source is internally inconsistent.

Do not report an internal numeric "humanness" score as evidence of quality. The useful evidence is the preserved ledger, the focused changes, and the unresolved items that remain visible.
