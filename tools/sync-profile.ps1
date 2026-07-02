param(
    [ValidateSet("DryRun", "Sync", "Status")]
    [string]$Action = "Status",

    [string]$Profile = "engineer",

    [string]$TargetRoot = (Join-Path $env:USERPROFILE ".codex\skills"),

    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$pythonAction = switch ($Action) {
    "DryRun" { "dry-run" }
    "Sync" { "sync" }
    "Status" { "status" }
}

$argsList = @(
    (Join-Path $PSScriptRoot "sync_profile.py"),
    "--action", $pythonAction,
    "--profile", $Profile,
    "--target-root", $TargetRoot
)

if ($Clean) {
    $argsList += "--clean"
}

python @argsList
