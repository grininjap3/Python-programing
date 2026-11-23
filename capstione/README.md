# StudySync AI — Downloader launcher

This folder contains the lightweight Windows downloader/installer for StudySync AI.

## What it does

1. Checks the latest published GitHub Release in this repository.
2. Downloads `StudySyncAI-Windows.zip` and its SHA-256 checksum.
3. Verifies the archive before extracting it.
4. Installs the app under `%LOCALAPPDATA%\Programs\StudySyncAI`.
5. Creates a Desktop and Start Menu shortcut.
6. Starts StudySync AI. Running the launcher again installs the newest release.

## Repository and visibility

The launcher is configured for `grininjap3/Python-programing`.

**This repository is currently public.** Anyone can view this folder and download release assets published here. Do not upload passwords, API keys, OAuth token files, `credentials.json`, databases, personal information or student data. This is not private distribution; use a private repository if download access must be restricted.

## Files

- `Install-StudySyncAI.cmd` — double-click entry point.
- `Install-StudySyncAI.ps1` — downloads, verifies, installs and creates shortcuts.
- `launcher-config.json` — release repository and asset names.
- `Prepare-GitHub-Release.ps1` — packages the Windows `dist` folder and generates SHA-256.
- `RELEASE_NOTES_TEMPLATE.txt` — suggested release description.

## Publish a Windows app release

On the Windows build computer:

1. Build the desktop application so `dist` contains `StudySyncAI.exe` and all required runtime files.
2. Open PowerShell in the folder containing `Prepare-GitHub-Release.ps1`.
3. Run the packaging helper, giving it the actual dist path:

   ```powershell
   .\Prepare-GitHub-Release.ps1 -DistFolder "C:\full\path\to\dist"
   ```

4. The helper creates `ReleaseAssets\StudySyncAI-Windows.zip` and `ReleaseAssets\StudySyncAI-Windows.zip.sha256`.
5. In this repository, open **Releases → Draft a new release**. Create a tag such as `v1.0.0`.
6. Upload both generated files and publish the release. The asset names must match `launcher-config.json` exactly.

The Windows application ZIP and its SHA-256 checksum are now published in the `v1.0.0` GitHub Release. The installer checks the latest release and downloads the matching assets automatically.

## Install on another Windows PC

Copy the three launcher files to the tester, then double-click `Install-StudySyncAI.cmd`. Internet access is required.

The app's local database, Google sign-in token and API key are separate from the downloaded program and are not overwritten by the installer. Each tester must use their own Google authorization and their own OpenAI API key.

## Windows security

This launcher source and the current app executable are not digitally signed. GitHub hosting does not make unsigned files trusted. Smart App Control may block unsigned scripts or executables. Do not disable Smart App Control or bypass Windows security. For distribution, sign the launcher scripts and application binaries with a code-signing certificate trusted by Windows before sharing them.
