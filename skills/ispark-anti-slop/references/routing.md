# Anti-Slop Routing Notes

This reference turns an explicit "去 AI 味" request into a bounded handoff. It is a routing aid, not a replacement for the owning skill.

## Common floor

Ask four questions before editing:

1. What job must the output perform?
2. Which details prove that it belongs to this user, system, audience, or domain?
3. Which facts, literals, contracts, and caveats cannot change?
4. Which observations are source-certain, render-observed, or still unknown?

Do not remove a useful table, list, formal phrase, UI primitive, error state, or defensive check merely because a model often overuses it. Explain the actual mismatch and preserve the function.

## Handoff matrix

| Surface | Primary owner | Quality focus | Required evidence |
|---|---|---|---|
| General prose | `ispark-writing` | concrete claims, register, rhythm, fact ledger | source text and intended audience |
| Chinese prose | `ispark-writing` + `chinese-writing.md` | de-nominalization, non-mechanical structure, genre fit | original wording and genre |
| Academic prose | `ispark-academic-writing` | citation/equation preservation, claim scope, section function | manuscript source and citation/notation context |
| Frontend/UI | `ispark-product-design` | intentional hierarchy, visual specificity, complete states | source plus browser render when available |
| Code/PR | `ispark-dev-workflow` + `ispark-review-risk` | root-cause fix, minimal diff, observable failure | call path, tests, contracts, and diff |

## Loading order

Use the smallest loading set that can answer the request:

1. Clearly one domain: load the primary owner only. Its own route decides which reference files are needed.
2. One artifact with two jobs, such as UI copy plus layout: load the primary owner first, then one companion only for the second job.
3. Review or audit across domains: load this matrix, then at most two owner skills; keep findings separated by owner.
4. Do not load `ispark-anti-slop` again after handoff unless the task changes into a cross-domain audit.

Negative boundaries prevent accidental context growth: wording-only work stays with
`ispark-writing`; visual or interaction work stays with `ispark-product-design`; code
implementation stays with `ispark-dev-workflow`; review-only work stays with
`ispark-review-risk`.

## Finding format

For an audit, lead with findings rather than a generic score. Each material finding names:

- `Pattern`: the observable pattern.
- `Where`: file, section, component, or rendered location.
- `Confidence`: source-certain, render-observed, or inferred.
- `Why`: the loss of meaning, usability, trust, or maintainability.
- `Direction`: one bounded correction that preserves the artifact's job.

If the issue is hollow content rather than wording, mark it `HOLLOW` and request or defer the missing fact. Do not fill the gap with plausible detail.

## Success test

The result should be justified by the task, coherent with its domain, and not a token swap into another stock style. A visual or prose pass that only changes colors, words, or formatting has not demonstrated quality by itself.
