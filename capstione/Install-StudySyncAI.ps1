# StudySync AI downloader / installer for Windows PowerShell 5.1+
# Uses public GitHub Releases. Does not alter Windows security settings.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

function Write-Step([string]$Message) {
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

try {
    $configPath = Join-Path $PSScriptRoot 'launcher-config.json'
    if (-not (Test-Path -LiteralPath $configPath)) {
        throw 'launcher-config.json is missing beside the installer.'
    }

    $config = Get-Content -LiteralPath $configPath -Raw | ConvertFrom-Json
    $owner = [string]$config.owner
    $repo = [string]$config.repository
    $assetName = [string]$config.asset_name
    $checksumName = [string]$config.checksum_asset_name
    $installFolderName = [string]$config.install_folder

    if ([string]::IsNullOrWhiteSpace($owner) -or
        [string]::IsNullOrWhiteSpace($repo) -or
        [string]::IsNullOrWhiteSpace($assetName) -or
        [string]::IsNullOrWhiteSpace($checksumName)) {
        throw 'The launcher configuration is incomplete.'
    }

    $headers = @{
        Accept = 'application/vnd.github+json'
        'User-Agent' = 'StudySyncAI-Installer'
        'X-GitHub-Api-Version' = '2022-11-28'
    }

    Write-Step "Checking latest release: $owner/$repo"
    $releaseUrl = "https://api.github.com/repos/$owner/$repo/releases/latest"
    $release = Invoke-RestMethod -Uri $releaseUrl -Headers $headers -Method Get

    $zipAsset = $release.assets | Where-Object { $_.name -eq $assetName } | Select-Object -First 1
    $hashAsset = $release.assets | Where-Object { $_.name -eq $checksumName } | Select-Object -First 1
    if (-not $zipAsset -or -not $hashAsset) {
        throw "The latest published release must contain both $assetName and $checksumName."
    }

    $work = Join-Path $env:TEMP ("StudySyncAI-Setup-" + [guid]::NewGuid().ToString('N'))
    $payload = Join-Path $work 'payload'
    New-Item -ItemType Directory -Path $payload -Force | Out-Null
    $zipPath = Join-Path $work $assetName
    $hashPath = Join-Path $work $checksumName

    Write-Step "Downloading StudySync AI $($release.tag_name)"
    Invoke-WebRequest -Uri $zipAsset.browser_download_url -OutFile $zipPath -UseBasicParsing
    Invoke-WebRequest -Uri $hashAsset.browser_download_url -OutFile $hashPath -UseBasicParsing

    $hashText = Get-Content -LiteralPath $hashPath -Raw
    if ($hashText -notmatch '(?i)\b([0-9a-f]{64})\b') {
        throw 'The release checksum file is missing a valid SHA-256 hash.'
    }
    $expectedHash = $Matches[1].ToLowerInvariant()
    $actualHash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actualHash -ne $expectedHash) {
        throw 'SHA-256 verification failed. The app was not installed.'
    }

    Write-Step 'Verifying and extracting the application'
    Expand-Archive -LiteralPath $zipPath -DestinationPath $payload -Force
    $payloadExe = Join-Path $payload 'StudySyncAI.exe'
    if (-not (Test-Path -LiteralPath $payloadExe)) {
        throw 'The downloaded ZIP must contain StudySyncAI.exe at its top level.'
    }

    $programs = Join-Path $env:LOCALAPPDATA 'Programs'
    New-Item -ItemType Directory -Path $programs -Force | Out-Null
    $installPath = Join-Path $programs $installFolderName
    $backupPath = "$installPath.previous"

    if (Test-Path -LiteralPath $backupPath) {
        Remove-Item -LiteralPath $backupPath -Recurse -Force
    }
    if (Test-Path -LiteralPath $installPath) {
        Move-Item -LiteralPath $installPath -Destination $backupPath
    }
    try {
        Move-Item -LiteralPath $payload -Destination $installPath
    } catch {
        if (Test-Path -LiteralPath $backupPath) {
            Move-Item -LiteralPath $backupPath -Destination $installPath
        }
        throw
    }
    if (Test-Path -LiteralPath $backupPath) {
        Remove-Item -LiteralPath $backupPath -Recurse -Force
    }

    $installedExe = Join-Path $installPath 'StudySyncAI.exe'
    $desktop = [Environment]::GetFolderPath('Desktop')
    $startMenu = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\StudySync AI'
    New-Item -ItemType Directory -Path $startMenu -Force | Out-Null

    $shell = New-Object -ComObject WScript.Shell
    foreach ($shortcutPath in @(
        (Join-Path $desktop 'StudySync AI.lnk'),
        (Join-Path $startMenu 'StudySync AI.lnk')
    )) {
        $shortcut = $shell.CreateShortcut($shortcutPath)
        $shortcut.TargetPath = $installedExe
        $shortcut.WorkingDirectory = $installPath
        $shortcut.IconLocation = "$installedExe,0"
        $shortcut.Description = 'Open StudySync AI'
        $shortcut.Save()
    }

    Write-Step 'Installation completed'
    Write-Host "Installed version: $($release.tag_name)" -ForegroundColor Green
    Write-Host "Desktop shortcut: $(Join-Path $desktop 'StudySync AI.lnk')"
    Write-Host 'Your local database and settings were not overwritten.'
    Write-Host 'Starting StudySync AI...'
    Start-Process -FilePath $installedExe -WorkingDirectory $installPath

    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
} catch {
    Write-Host "`nINSTALLATION FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host 'No Windows security settings were changed.' -ForegroundColor Yellow
    exit 1
}
