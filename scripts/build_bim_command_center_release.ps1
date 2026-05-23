param(
    [Parameter(Mandatory = $true)]
    [string]$AutodeskAppId,

    [string]$Configuration = "Release"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$ProjectDir = Join-Path $RepoRoot "260519 소스 폴더\01_Revit_Addins\Addin Dashboard"
$ProjectFile = Join-Path $ProjectDir "BIMCommandCenter.csproj"
$InstallerProject = Join-Path $ProjectDir "Installer\BIMCommandCenter.Installer.csproj"
$SettingsFile = Join-Path $ProjectDir "license-settings.json"

if (-not (Test-Path $ProjectFile)) {
    throw "Project file not found: $ProjectFile"
}

if ([string]::IsNullOrWhiteSpace($AutodeskAppId) -or $AutodeskAppId -like "*REPLACE_WITH*") {
    throw "A real Autodesk App Store App ID is required."
}

$settings = @{
    appId = $AutodeskAppId
    entitlementUrl = "https://apps.autodesk.com/webservices/checkentitlement"
}
$settings | ConvertTo-Json -Depth 3 | Set-Content -Path $SettingsFile -Encoding UTF8

Write-Host "Cleaning previous build output..."
dotnet clean $ProjectFile --configuration $Configuration
dotnet clean $InstallerProject --configuration $Configuration

Write-Host "Restoring packages..."
dotnet restore $ProjectFile
dotnet restore $InstallerProject

Write-Host "Building BIM Command Center..."
dotnet build $ProjectFile --configuration $Configuration --no-restore

Write-Host "Building installer..."
dotnet build $InstallerProject --configuration $Configuration --no-restore

Write-Host "Scanning source for removed local-license secrets..."
$scanTargets = @(
    (Join-Path $ProjectDir "License"),
    (Join-Path $ProjectDir "Models"),
    $ProjectFile,
    $InstallerProject
)

$patterns = "ActivationPassword|HmacSecret|SecureSign|Jy895"
$scanFiles = foreach ($target in $scanTargets) {
    if (Test-Path $target -PathType Container) {
        Get-ChildItem -Path $target -Recurse -File
    } elseif (Test-Path $target -PathType Leaf) {
        Get-Item $target
    }
}
$matches = $scanFiles | Select-String -Pattern $patterns -ErrorAction SilentlyContinue
if ($matches) {
    $matches | Format-Table Path, LineNumber, Line -AutoSize
    throw "Secret-like local-license strings were found. Do not ship this build."
}

Write-Host "Release build completed. Next: test install/uninstall on clean Revit 2024/2025/2026 machines."
