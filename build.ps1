$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
$versionFile = Join-Path $root "VERSION"
$yamlFile = Join-Path $root "maubot.yaml"
$version = (Get-Content $versionFile -Raw).Trim()
$outDir = Join-Path $root "build"
$artifact = Join-Path $outDir "NEXT-Maubot-helper-v$version.mbp"
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
$python = if (Test-Path $venvPython) { $venvPython } else { "python" }

function Set-MaubotYamlVersion([string]$ver) {
    $lines = Get-Content $yamlFile
    $lines = $lines | ForEach-Object {
        if ($_ -match '^\s*version:\s*') { "version: $ver" } else { $_ }
    }
    Set-Content -Path $yamlFile -Value $lines -Encoding utf8
}

function Get-NextPatchVersion([string]$ver) {
    if ($ver -match '^(\d+)\.(\d+)\.(\d+)$') {
        $patch = [int]$Matches[3] + 1
        return "$($Matches[1]).$($Matches[2]).$patch"
    }
    throw "VERSION must be semver X.Y.Z, got: $ver"
}

if (-not $env:HOME) {
    $env:HOME = $env:USERPROFILE
}
if (-not $env:XDG_CONFIG_HOME) {
    $env:XDG_CONFIG_HOME = Join-Path $env:USERPROFILE ".config"
}

Set-MaubotYamlVersion $version

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

    $nextVersion = Get-NextPatchVersion $version
    Set-Content -Path $versionFile -Value $nextVersion -NoNewline -Encoding utf8
    Set-MaubotYamlVersion $nextVersion
    Write-Host "Next build version: $nextVersion (VERSION + maubot.yaml)"
}
finally {
    Pop-Location
}
