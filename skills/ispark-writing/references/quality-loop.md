# Prose Quality Loop

Use this loop for both new prose and supplied drafts. It improves observable quality; it does not infer authorship or produce a detector-evasion score.

## Select the register first

Identify the audience, channel, genre, and formality before changing wording. A work message may use short fragments; a technical report may need formal syntax; a product label must name an action; a public announcement must distinguish shipped facts from plans. Do not force one "human" voice across all of them.

## Generation mode

For `draft`, establish the controlling point and fact ledger before composing. Write the point directly, give each paragraph one job, use concrete actors and actions, and stop when the reader can understand or act. Avoid stock openings, empty transitions, repeated summaries, decorative emphasis, and mechanically balanced lists when the source does not require them.

## Rewrite mode

For `rewrite`, preserve direct quotes, names, numbers, dates, URLs, citations, commands, required terminology, and the author's claim strength. Change the argument order only when the user asks or the current order prevents understanding. Remove a pattern only when the replacement says the same thing and still fits the register.

## Audit and triage

Inspect paragraph by paragraph, skipping code blocks, quotations, headings, and genuine enumerations. Surface candidates such as empty openings, filler transitions, abstract noun chains, generic praise, negative parallelism, over-balanced lists, chatbot residue, and repeated conclusions. Then apply the removal test:

- `rewordable`: a real claim exists but filler or hedging hides it; rewrite the smallest span.
- `hollow`: deleting the span loses no supported information; flag it and request the missing substance if it matters.

An isolated em dash, adverb, list, or formal phrase is not a defect by itself. Fix clusters and context mismatches, not words on sight.

## Self-check

After each focused pass, compare source and result for newly introduced facts, changed modality, omitted caveats, altered audience, and repeated claims. Stop after three passes. If the text remains hollow, report that better wording cannot supply the missing claim. A paragraph that already does its job should remain unchanged.

For audit-only requests, return findings first with `Pattern`, `Where`, `Why`, and `Direction`; do not perform the rewrite.
