# Encoding And Statistical Integrity

Use this reference to decide how values become position, length, shape, area, color, texture, labels, or motion.

## Encode for the comparison

- Prefer position on a shared scale for precise comparison, then aligned length. Area, angle, volume, saturation, and motion have higher decoding cost and need a clear reason.
- Keep each channel's meaning stable. Do not reuse the same color, shape, or line style for unrelated concepts in adjacent views.
- Use direct labels and nearby annotations when they reduce legend lookup. Keep essential values, units, source context, and caveats available without hover.
- Preserve enough whitespace and label separation to prevent collisions from changing the apparent grouping.
- A visual hierarchy may guide reading, but it must not mute evidence that contradicts the highlighted claim.

These are comparison defaults, not universal chart bans. A less precise channel can be appropriate when the task is pattern recognition rather than exact lookup.

## Audit scale/domain and transformation

- State the measure, unit, scale/domain, baseline, and denominator. Keep comparable panels on comparable domains unless the difference is explicit and justified.
- Bars and filled lengths normally need a meaningful zero. A truncated quantitative axis, log scale, dual axis, or broken axis requires visible disclosure and a task-specific reason.
- Validate aggregation, grouping, joins, normalization, sorting, bins, smoothing, and filters against the source. Show weighted versus unweighted choices when they change the claim.
- Do not use cumulative, per-capita, percentage, indexed, or rate views without naming the denominator or reference period.
- Check whether aggregation hides subgroup reversals, outliers, sparse groups, or sample-size differences. Offer a distribution or disaggregated view when those affect the decision.

## Preserve uncertainty and missing data

- Use intervals, distributions, bands, ensembles, ranges, opacity, or explicit labels according to what the uncertainty estimate actually means.
- Name the interval or model; do not imply that a confidence interval, credible interval, prediction interval, and min-max range are interchangeable.
- Keep observations, estimates, forecasts, targets, and reference values visually distinct.
- Distinguish missing data, zero, not applicable, censored, suppressed, stale, and not yet collected. Never silently coerce them to zero or connect a line across a gap.
- If imputation, interpolation, sampling, or downsampling is necessary, preserve the original count and disclose the method where it can affect interpretation.
- Statistical significance, causal identification, effect-size interpretation, multiplicity, and model choice remain with the analysis or academic owner. Preserve supplied results and assumptions; do not infer them from visual separation alone.

## Use color as meaning

- Assign every color a role: categorical identity, ordered magnitude, signed deviation, status, selection, or annotation.
- Use sequential scales for ordered magnitude, diverging scales around a meaningful midpoint, and categorical palettes only for distinct groups.
- Do not encode the only important distinction with color. Add position, shape, line style, texture, text, or a tabular equivalent.
- Check contrast, grayscale, common color-vision differences, dark/light themes, and exported output. Avoid making low confidence look like low importance unless that is the intended meaning.

## Integrity review

Before visual polish, ask whether changing the scale, aggregation, denominator, missing-data treatment, uncertainty display, or annotation would reverse the apparent conclusion. If so, resolve or disclose that dependency before implementation.
