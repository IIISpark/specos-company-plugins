# Apifox Branches And AI Branches

Use this reference for branch context, AI branches, pick-to, protected branches, merges, and merge
requests.

Before a write, confirm project, source branch, target branch, resource scope, and whether the user is
authorizing direct editing, an isolated AI branch, a merge request, or a merge. Never infer one of these
permissions from approval to edit an API resource.

## AI Branch Boundary

- Creating or switching to an AI branch requires confirmation.
- An AI branch begins without a full copy of source resources. Existing source resources must be
  explicitly picked into it before modification; new resources do not require a pick.
- Keep the same explicit branch on reads, writes, and verification. A default-branch read cannot prove
  what exists on the AI branch.
- Pick-to supports only the directions and resource types shown by current help. Do not use an AI
  branch as an inferred source or import into a main branch through pick-to.
- Permission errors must stop for the user to choose direct-edit permissions or an AI branch. Do not
  create or switch branches as automatic recovery.

## Merge Boundary

Read back and verify changes in the source branch, then preview the merge request or merge impact.
Obtain a separate confirmation immediately before creating an MR, approving one, or merging. Prefer a
merge request for a protected target. Branch deletion or archival is a distinct destructive action and
requires an explicit request.
