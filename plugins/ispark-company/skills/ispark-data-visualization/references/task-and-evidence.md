# Task And Evidence

Use this reference before choosing a chart family or drawing a layout.

## Frame the job

Write a compact contract:

- **Analytical question**: the comparison, pattern, relationship, distribution, location, sequence, or exception the view must expose.
- **Viewer and decision**: who reads it, what they already know, and what they should understand or do next.
- **Mode**: exploratory analysis, explanatory communication, operational monitoring, scientific figure, or editable analytical tool.
- **Data shape**: table, time series, distribution, multivariate records, matrix, hierarchy, network, schedule, geospatial layer, stream, or simulation.
- **Delivery**: browser, dashboard, notebook, paper, report, slide, print, embedded product surface, or conversation artifact.
- **Reading path**: the first comparison, supporting detail, caveat, and optional exploration in that order.

Do not begin with a library name. If the analytical question or source fields are still unknown, state the smallest missing fact rather than inventing a story for the data.

## Keep an evidence ledger

Record what a reader would need to reproduce or challenge the claim:

- source, owner, collection method, time coverage, population, sample, and update cadence;
- units, denominator, reference period, category definitions, joins, filters, and transformations;
- aggregation, normalization, binning, smoothing, interpolation, imputation, and exclusions;
- missing data, censored or suppressed values, uncertainty, model assumptions, and known bias;
- for live data, stream/snapshot/polling mode, event time versus arrival time, ordering, stale threshold, and last-known-good behavior;
- version or snapshot date, licensing or sensitivity constraints, and caveats.

Separate source facts from derived metrics and annotations. A title may state a finding only when the plotted evidence supports that claim; otherwise use a descriptive title and make the open question explicit.

## Choose the narrowest useful view

| Analytical job | Start with | Escalate when |
| --- | --- | --- |
| Exact lookup or mixed values | table with aligned columns | a pattern is hard to scan |
| Comparison or ranking | dot plot or bar on a common baseline | dense labels require small multiples |
| Change over time | line, slope, or interval view | overlapping series require faceting or interaction |
| Distribution | histogram, ECDF, dot/strip, box, or violin | groups or tails need layered detail |
| Relationship | scatterplot or small multiples | density requires hexbin, contours, or sampling |
| Part to whole | stacked view with a stable denominator | precise comparison requires a table or separate bars |
| Matrix | aligned table or heatmap | clustering or topology changes the question |
| Geography | map plus a comparison view | location, distance, or spatial pattern is actually evidence |
| Network or hierarchy | tree, adjacency, node-link, or flow | topology is central and labels remain legible |
| Evidence-bearing schedule or planned spans | timeline or Gantt | duration, dependencies, capacity, or uncertainty drive the decision; route software process, state, and sequence semantics to `$ispark-architecture-diagrams` |

Maps are not a substitute for ranking, and node-link diagrams are not a substitute for a table. Use geography, topology, animation, or narrative sequence only when it carries information the simpler view cannot.

## Define completion

The contract is ready for encoding when the main comparison, units, denominator, source, caveat, intended reading path, and required output modes are known. Keep unresolved evidence gaps visible through implementation and critique.
