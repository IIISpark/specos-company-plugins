# Anti-Slop Audit

Audit observable writing patterns. Do not claim that a person or model authored the text; these findings describe quality and distribution-default signals, not provenance.

## Critical findings

### Fabricated specificity

The prose introduces an unsourced metric, quotation, testimonial, customer, date, causal explanation, or example to make a claim sound concrete.

Fix direction: remove it, mark it as pending, or request the authoritative fact. Never replace it with a different plausible detail.

### Confidence inflation

The rewrite upgrades uncertainty or scope: `may` becomes `will`, a pilot becomes a launch, a proposal becomes a decision, or a local result becomes a general conclusion.

Fix direction: restore the original modality, scope, population, denominator, and publication state.

### Source blending

Conflicting sources or verified and inferred material are merged into one smooth account without attribution.

Fix direction: separate the claims, name their sources, and preserve the unresolved conflict.

### Authority laundering

The prose presents a template, historical note, model suggestion, or secondary summary as the current source of truth.

Fix direction: cite the actual authority or state that the claim is unverified.

## Major findings

### Empty abstraction

Phrases such as "全面赋能", "构建能力体系", "实现价值闭环", "深度协同", or "提升整体效能" appear without a named actor, action, object, or observable result.

Fix direction: name who does what, to which artifact or system, and how the reader can observe the result.

### Stock opening

The text opens with broad temporal or industry framing that does not affect the decision, such as "在当今快速发展的数字化时代".

Fix direction: start with the concrete problem, decision, change, or reader consequence.

### Structure before thought

The artifact uses a preselected frame such as background, challenges, solution, advantages, and outlook even though the content does not support those sections.

Fix direction: reorganize around the reader's actual question and remove empty symmetry.

### Mechanical parallelism

Every paragraph has the same length, every list has three items, or multiple sentences repeat the same grammatical pattern without a rhetorical reason.

Fix direction: let information density and relationship determine form. Keep genuine parallel structures parallel.

### Transition scaffolding

"首先", "其次", "此外", "与此同时", "值得注意的是", or "综上所述" carries the structure because the underlying relationship is not stated.

Fix direction: state the relationship directly: cause, contrast, dependency, consequence, or sequence. Delete the connector when no transition is needed.

### Redundant conclusion

The ending repeats the introduction or previous section without adding a decision, consequence, next action, or evidence boundary.

Fix direction: end at the last useful fact or replace the recap with the required action.

### Generic praise

The prose calls a plan "重要", "强大", "创新", "领先", "高质量", or "令人兴奋" without evidence or a reader-relevant comparison.

Fix direction: provide the specific property and evidence, or remove the evaluation.

### Voice flattening

A PRD, incident note, candidate assessment, customer announcement, and direct message all sound like the same polished corporate essay.

Fix direction: restore the artifact's job, reader knowledge, stakes, and natural level of formality.

### Fake intimacy

The text adds jokes, enthusiasm, apologies, rhetorical questions, or conversational filler that the author did not intend.

Fix direction: use warmth only when it serves the relationship and situation. Do not manufacture personality.

### Format camouflage

Excessive headings, bold fragments, callouts, tables, or bullets create the appearance of structure while splitting one simple argument into visual pieces.

Fix direction: keep formatting that improves retrieval, comparison, or action; return the rest to prose.

## Minor findings

- Meta narration: "下面我们将", "本文旨在", or "接下来让我们" when the document can simply begin.
- Weak verb: repeated "进行", "开展", "实现", or "提供" where a direct verb is available.
- Modifier stack: several adjectives or adverbs attempt to supply evidence.
- Repeated restatement: the same claim appears in a heading, lead sentence, callout, and conclusion.
- Uniform cadence: sentence and paragraph lengths remain mechanically identical.
- Placeholder language: "相关", "等", "某种程度", or "视情况而定" hides a boundary that could be named.

Minor findings are contextual signals, not banned tokens. Keep a phrase when it is accurate, necessary, and natural in the target voice.

## Audit output

Return findings first, ordered by severity. For each finding include:

- `Pattern`: the named finding.
- `Where`: file, section, paragraph, or a short quoted fragment.
- `Why`: the concrete loss of meaning, trust, or reader fit.
- `Direction`: one bounded correction, without silently rewriting the artifact.

End with counts by severity and a one-sentence assessment of the dominant problem. If no material findings exist, say so and identify any unverified fact or audience assumption that remains.
