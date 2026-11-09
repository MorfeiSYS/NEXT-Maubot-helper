$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$version = (Get-Content (Join-Path $root "VERSION") -Raw).Trim()
$outDir = Join-Path $root "build"
$artifact = Join-Path $outDir "NEXT-Maubot-helper-v$version.mbp"
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

if (-not $env:HOME) {
    $env:HOME = $env:USERPROFILE
}
if (-not $env:XDG_CONFIG_HOME) {
    $env:XDG_CONFIG_HOME = Join-Path $env:USERPROFILE ".config"
}

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

if (Test-Path $artifact) {
    Remove-Item -Force $artifact
}

Push-Location $root
try {
    & $python -m maubot.cli build -o $artifact
    if (-not (Test-Path $artifact)) {
        throw "Build failed: $artifact not found"
    }
    Write-Host "Built: $artifact"
}
finally {
    Pop-Location
}
