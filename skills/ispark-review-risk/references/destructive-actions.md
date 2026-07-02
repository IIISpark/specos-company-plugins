# Destructive Actions

Before deleting, moving, force-pushing, migrating, dropping data, or changing production state:

- state the target path/resource
- verify the resolved absolute path or resource id
- confirm it is inside the intended scope
- explain rollback or recovery path
- get explicit approval unless already clearly authorized

On Windows, do not enumerate paths in one shell and pass them to another for deletion. Use native PowerShell cmdlets with `-LiteralPath`.

