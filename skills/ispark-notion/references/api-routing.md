# Notion API Escape Hatch

Use `ntn api` only when a dedicated `ntn pages`, `ntn datasources`, or `ntn files` command cannot
express the authorized operation. Read `ntn api --help` first and use the local CLI's supported
request format.

## Required Boundary

- Establish the exact method, endpoint, authorized workspace object, request body, and expected
  effect before issuing the call.
- Treat `GET` and `POST` differently: a POST may still mutate state. Do not infer safety from the
  HTTP verb alone.
- For any non-read operation, present a compact mutation preview and obtain a new explicit
  confirmation immediately before the call.
- Do not use arbitrary API access to bypass missing CLI support, permission checks, pagination
  limits, or a user decision about scope.

## Output

- Do not display authorization material, full headers, raw request bodies containing private data,
  or full responses.
- Verify the smallest observable outcome and report a concise result, error category, and any
  next decision the user must make.
