param(
    [string]$DistFolder = 'C:\Users\RAMAMOHAN&KAMAKSHI\Downloads\StudySyncAI_Windows_Release_Kit_FIXED\StudySyncAI_Windows_Release_Fixed\dist',
    [string]$Tag = 'v1.0.0'
)

$ErrorActionPreference = 'Stop'

$exe = Join-Path $DistFolder 'StudySyncAI.exe'
if (-not (Test-Path -LiteralPath $exe)) {
    throw "StudySyncAI.exe not found at: $exe. Pass the actual dist folder with -DistFolder."
}

$gh = Get-Command gh -ErrorAction SilentlyContinue
if (-not $gh) {
    throw "GitHub CLI (gh) is not installed. Install it from https://cli.github.com/, then run 'gh auth login' once."
}

& gh auth status
if ($LASTEXITCODE -ne 0) {
    throw "GitHub CLI is not authenticated. Run 'gh auth login' and try again."
}

$repo = 'grininjap3/Python-programing'
$assetsDir = Join-Path $PSScriptRoot 'ReleaseAssets'
New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null

$zipPath = Join-Path $assetsDir 'StudySyncAI-Windows.zip'
$hashPath = Join-Path $assetsDir 'StudySyncAI-Windows.zip.sha256'
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
if (Test-Path -LiteralPath $hashPath) { Remove-Item -LiteralPath $hashPath -Force }

Compress-Archive -Path (Join-Path $DistFolder '*') -DestinationPath $zipPath -CompressionLevel Optimal
$hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
Set-Content -LiteralPath $hashPath -Value "$hash  StudySyncAI-Windows.zip" -Encoding ASCII

Write-Host "Prepared app bundle and SHA-256 checksum." -ForegroundColor Green

$releaseExists = $false
& gh release view $Tag --repo $repo *> $null
if ($LASTEXITCODE -eq 0) { $releaseExists = $true }

if ($releaseExists) {
    & gh release upload $Tag $zipPath $hashPath --repo $repo --clobber
    if ($LASTEXITCODE -ne 0) { throw 'Could not upload assets to the existing release.' }
} else {
    & gh release create $Tag $zipPath $hashPath --repo $repo --title "StudySync AI $Tag" --notes "StudySync AI Windows desktop release. Each user must configure their own Google OAuth credentials and OpenAI API key. Do not share personal tokens or keys."
    if ($LASTEXITCODE -ne 0) { throw 'Could not create the GitHub release.' }
}

Write-Host ""
Write-Host "Release published: https://github.com/$repo/releases/tag/$Tag" -ForegroundColor Green
Write-Host "Release asset: StudySyncAI-Windows.zip"
Write-Host "Checksum: StudySyncAI-Windows.zip.sha256"
