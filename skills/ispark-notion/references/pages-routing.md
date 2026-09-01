# Notion Pages

Use this reference for `ntn pages` operations. Read the exact selected subcommand help before
constructing a command because flags and supported parent types can change.

## Reads

- Use `ntn pages get <page>` only after the user identifies the page or authorizes a narrow lookup.
- Prefer the smallest useful representation. Treat page body, properties, comments, and child
  content as private workspace data; report only the requested facts.
- When identifiers or titles resolve to more than one candidate, show safe distinguishing metadata
  and ask the user to choose.

## Mutations

- `ntn pages create`, `ntn pages edit`, and `ntn pages trash` change Notion state.
- Before each mutation, show the parent or target, requested title/property/content delta, and
  whether the action creates, edits, or archives. Wait for a new explicit confirmation.
- Do not overwrite a page body when the requested patch is ambiguous. Retrieve the authorized
  current content first or ask for the intended replacement scope.
- After a confirmed mutation, verify only the necessary resulting title, property, or revision and
  summarize the result without dumping page content.

For document wording without a Notion API action, use `$ispark-writing` instead.
