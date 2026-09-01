# Source Model And Formats

Treat diagram source, semantic model, layout, and rendered output as different artifacts. Converting among them can lose information.

## Preserve provenance and semantics

- Keep stable source IDs for nodes, edges, ports, groups, lanes, states, fields, and external systems when the source provides them.
- Mark relationships as explicit, inferred, generated, or omitted. Record the rule and confidence for inferred relationships instead of presenting them as source truth.
- Build a normalized model before renderer-specific objects: diagram ID/type/scope/source/version; nodes; edges; groups or lanes; ports; annotations; diagnostics; and optional layout hints.
- Keep semantic attributes such as direction, cardinality, protocol, event, guard, ownership, stereotype, and source reference separate from color or coordinates.
- Treat coordinates as layout hints unless faithful manual placement is part of the maintained contract.

## Choose the maintained source

| Need | Suitable source choices | Important limits |
| --- | --- | --- |
| Formal UML model exchange | XMI, with UMLDI when geometry must travel | vendor profiles and extensions may not round-trip |
| Documentation-first UML-like diagrams | PlantUML, Mermaid, D2, Graphviz DOT | syntax overlap does not imply semantic equivalence |
| Reusable C4 model and several views | Structurizr DSL | keep one architecture model rather than unrelated view files |
| Relational schema documentation | DBML, SQL-derived ERD, Mermaid ER, PlantUML IE/ER | derive from the authoritative schema when possible |
| Executable or interoperable process model | BPMN XML | use a lighter flow/activity source when communication alone is enough |
| Interactive product surface | typed JSON graph or domain model | do not make library node objects the canonical model |
| Visual-editor compatibility | the editor's native source plus provenance | shape geometry alone rarely carries full model semantics |

SVG, PNG, and PDF are output formats, not semantic sources. Keep the source DSL or normalized model beside generated assets when maintenance, regeneration, review, or conversion matters.

## Read, write, and convert deliberately

- On import, identify whether the input is a semantic model, DSL, visual-editor artifact, or rendered image before extracting facts.
- Preserve namespaces, IDs, stereotypes, tags, cardinality, edge direction, and format-specific extensions. Surface unsupported elements and loss warnings.
- On generation, include source files, schema/model version, generator, date, scope, and known omissions.
- Use a staged conversion such as source inventory -> normalized model -> target DSL/renderer -> export. Do not reconstruct architecture from PNG when a semantic or vector source exists.
- Define round-trip ownership before supporting edits: source file wins, diagram model wins, or conflicts require explicit resolution.
- Do not promise lossless conversion among XMI/UMLDI, PlantUML, Mermaid, Graphviz DOT, D2, Structurizr, DBML, BPMN XML, editor files, and renderer models without a tested field-level mapping.
