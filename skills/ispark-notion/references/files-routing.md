# Notion Files

Use this reference for `ntn files` operations.

## Read Operations

- Use `ntn files get` or `ntn files list` only for a user-authorized file or page scope.
- Keep returned metadata narrow. Do not download, mirror, or enumerate a workspace's files merely
  to inspect it.
- The local CLI may not implement full list pagination; report that limit rather than simulating a
  broader crawl through another interface.

## Upload Operations

- `ntn files create` uploads bytes or registers an external URL and changes remote state.
- Before starting, confirm the exact local file or URL, target purpose, visibility implications,
  and whether the upload will be attached by a following Notion mutation.
- Read only the minimum local source needed to verify it is the requested artifact. Do not upload
  secrets, private exports, or diagnostic archives.
- Verify the resulting file reference only after confirmation and keep the reference out of the
  user-facing summary unless it is needed for the requested next action.
