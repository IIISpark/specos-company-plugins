param(
    [ValidateSet("install", "update", "status")]
    [string]$Action = "install",

    [string]$Source = "IIISpark/specos-company-plugins",

    [string]$Ref = "main",

    [string]$Marketplace = "ispark-company",

    [string]$Plugin = "ispark-company"
)

$ErrorActionPreference = "Stop"

python (Join-Path $PSScriptRoot "install_or_update.py") `
    --action $Action `
    --source $Source `
    --ref $Ref `
    --marketplace $Marketplace `
    --plugin $Plugin
