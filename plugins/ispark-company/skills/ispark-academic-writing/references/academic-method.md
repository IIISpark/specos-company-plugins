# Academic Revision Method

## Contract and ledger

Before editing, record the fields that can change the result:

- language, discipline, section type, audience, and requested intensity;
- the research question, contribution wording, and paragraph function;
- literal items: citations, BibTeX keys, equations, variables, units, values, labels, names, and markup;
- evidence scope, denominator, conditions, limitations, and modality;
- terms that must remain stable and any source ambiguity that needs a flag.

Treat the ledger as a preservation contract. A style edit may subtract filler or expose a claim already present, but it may not turn an `Unknown` into a fact or a cautious result into a universal conclusion.

For research or experiment-heavy writing, extend the ledger with source provenance,
dataset/version, protocol, baseline, comparison set, exclusions, randomization or seed,
and the analysis decision that produced each reported result. Keep observations,
interpretations, and hypotheses in separate rows. A generated summary is a navigation
aid; the original paper, data, code, or recorded protocol remains the evidence source.

## Intensity

- **Light**: fix obvious formulaic wording, grammar, and local flow. Keep sentence boundaries and paragraph order.
- **Medium**: improve cohesion and sentence rhythm while keeping paragraph function and claim scope.
- **Deep**: recast sentences and split or merge where the argument needs it. Keep every supported fact, reference, condition, and limitation.

If no intensity is specified, use medium. If a stronger revision would require domain knowledge or a new claim, flag the decision instead of guessing.

## Section behavior

- **Abstract**: state problem, method, result, and supported contribution compactly; remove broad importance claims.
- **Introduction**: make the gap and motivation specific to the cited work; do not manufacture urgency.
- **Related work**: keep attribution and comparison boundaries visible; do not collapse distinct papers into one consensus.
- **Methods**: favor reproducible actions, settings, and definitions; avoid promotional adjectives.
- **Results**: separate observed values and comparisons from interpretation; preserve baselines and denominators.
- **Discussion**: distinguish explanation, implication, and speculation; retain conditions and uncertainty.
- **Conclusion**: summarize demonstrated findings and limitations, not desired field-wide impact.
- **Response/rebuttal**: keep the reviewer claim, response scope, evidence, and remaining disagreement explicit.

## Human academic voice

Human voice in a paper means a researcher making bounded choices about evidence and argument. It does not mean adding jokes, fake first person, slang, dramatic fragments, or arbitrary sentence noise. Vary rhythm only when it makes the logic easier to follow.

## Edit loop

1. Find stock framing, empty evaluation, mechanical connectors, nominalized actions, repeated sentence shapes, and unsupported significance.
2. Decide whether each issue is rewordable or hollow. Rewrite the former; flag the latter.
3. Make the smallest source-grounded edit and keep terminology stable.
4. Run the preservation checks in `verification.md`.
5. Stop after at most three focused passes. If the text still lacks a claim, report that the missing substance needs the author or source.
