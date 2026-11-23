param(
    [Parameter(Mandatory = $true)]
    [string]$DistFolder,
    [string]$OutputFolder = (Join-Path $PSScriptRoot 'ReleaseAssets')
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $DistFolder -PathType Container)) {
    throw "Distribution folder not found: $DistFolder"
}

$exe = Get-ChildItem -LiteralPath $DistFolder -Filter 'StudySyncAI.exe' -File -Recurse |
    Select-Object -First 1
if (-not $exe) {
    throw "StudySyncAI.exe was not found under: $DistFolder"
}

$sourceRoot = $exe.Directory.FullName
$stage = Join-Path $env:TEMP ('StudySyncAI-Release-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage -Force | Out-Null

$excludedDirs = @('.venv', '.git', '__pycache__', 'data', 'uploads', 'tokens')
$excludedFiles = @('credentials.json', 'google_classroom_token.json',
                   'token_google_classroom.json', '.env')

try {
    Get-ChildItem -LiteralPath $sourceRoot -Force -Recurse | ForEach-Object {
        $item = $_
        $relative = $item.FullName.Substring($sourceRoot.Length).TrimStart([char]92, [char]47)
        $parts = $relative -split '[\\/]'
        if ($parts | Where-Object { $excludedDirs -contains $_ }) { return }
        if (-not $item.PSIsContainer) {
            if ($excludedFiles -contains $item.Name) { return }
            if ($item.Name -match '(?i)^(token.*\.json|.*\.(db|sqlite|sqlite3))$') { return }
        }

        $target = Join-Path $stage $relative
        if ($item.PSIsContainer) {
            New-Item -ItemType Directory -Path $target -Force | Out-Null
        } else {
            $targetParent = Split-Path -Parent $target
            New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
            Copy-Item -LiteralPath $item.FullName -Destination $target -Force
        }
    }

    if (-not (Test-Path -LiteralPath (Join-Path $stage 'StudySyncAI.exe'))) {
        throw 'StudySyncAI.exe must be at the root of the packaged application folder.'
    }

    New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
    $zip = Join-Path $OutputFolder 'StudySyncAI-Windows.zip'
    $sha = Join-Path $OutputFolder 'StudySyncAI-Windows.zip.sha256'
    if (Test-Path $zip) { Remove-Item $zip -Force }
    if (Test-Path $sha) { Remove-Item $sha -Force }

    Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal
    $hash = (Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant()
    Set-Content -LiteralPath $sha -Value "$hash  StudySyncAI-Windows.zip" -Encoding ASCII

    Write-Host 'Upload BOTH files to a published GitHub Release:' -ForegroundColor Green
    Write-Host $zip
    Write-Host $sha
    Write-Host "SHA-256: $hash"
} finally {
    if (Test-Path $stage) {
        Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
    }
}
