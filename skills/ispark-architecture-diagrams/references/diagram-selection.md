# Diagram Selection

Choose a notation only after defining the modeling job. Formality is useful when it carries semantics, not as decoration.

## Frame the view

Write a compact contract:

- **One modeling question**: structure, runtime interaction, lifecycle state, workflow, ownership, deployment, schema, dependency, or impact.
- **Audience and decision**: who must understand the view and what they need to verify, discuss, or change next.
- **Source and confidence**: authoritative documents, code, schema, runtime inventory, user statement, and any unresolved or inferred relation.
- **Scope**: included systems, boundary, time/version, environment, and deliberate omissions.
- **One abstraction level**: context, container/deployable unit, component/module, code/type, record/schema, or runtime instance. Use a separate bridge view when two levels must connect.
- **Delivery mode**: durable docs, review artifact, generated CI asset, interactive explorer, editable model, or conversation explanation.

If the source does not establish a node, edge, cardinality, protocol, state, or ownership claim, ask for the smallest missing fact or mark it as inference. Do not make a polished diagram look more certain than its inputs.

## Select the family

| Modeling job | Start with | Use a different form when |
| --- | --- | --- |
| System boundary and major responsibilities | C4 context/container or a restrained architecture map | deployment topology or runtime order is the real question |
| Deployable nodes and runtime placement | deployment or topology diagram | process sequence matters more than placement |
| Components, packages, modules, or interfaces | component/package diagram | code-level class detail is actually required |
| Actor goals and system boundary | use-case view or actor-goal list | a simple list communicates the same facts more clearly |
| Ordered calls, messages, and protocol steps | sequence diagram | topology matters as much as order, then consider communication view |
| Lifecycle rules and valid transitions | state machine | work ownership and parallelism are the main concern |
| Workflow, branching, ownership, or handoff | activity, swimlane, BPMN, or flowchart | executable process interchange requires BPMN semantics |
| Relational schema and constraints | ERD or DBML-backed schema view | domain concepts without persistence are the question |
| Dependency, lineage, coupling, or blast radius | dependency graph, matrix, or focused neighborhood | the full node-link view becomes a hairball |

Use formal UML when notation precision, profiles, methodology alignment, or model interchange matters. Use C4, ERD, BPMN, flowchart, swimlane, dependency graph, or another UML-like view when it answers the question with less ceremony. Prefer several focused views over one diagram mixing business process, deployment, schema, and code detail.

## Detail and labeling

- Preserve names, stable identifiers, boundaries, ownership, and relationship direction.
- Label important edges with verbs, events, protocols, data, cardinality, or guards rather than leaving ambiguous arrows.
- Hide incidental generated members and low-level fields unless they answer the view's question.
- Put scope, version/date, source, generator, and known omissions beside durable exports.
- State one recommended diagram family and one simpler fallback, with the choice tied to audience and modeling job.
