# 🚀 Omnitrix Watch — Release & Distribution Guide

This guide explains how to release new versions of **Omnitrix Watch** on GitHub and distribute the one-click package to users.

---

## 🎯 Option A: Instant One-Click for End Users

When distributing to friends or community members, they have two one-click options:

### 1. Standalone Portable Package (No Python Required)
1. Download `OmnitrixWatch-v0.1.0-windows-x64.zip` from the GitHub Release.
2. Extract the folder.
3. Double-click **`Run-Omnitrix.bat`** (or `OmnitrixWatch\OmnitrixWatch.exe`).
4. That's it! The Omnitrix dashboard opens immediately.

### 2. Source Repository Users (With Python)
1. Double-click **`Launch-Omnitrix.bat`** in the repository root.
   - It automatically checks for Python, sets up `.venv`, installs requirements if missing, and boots the application.
2. (Optional) Double-click **`Create-Desktop-Shortcut.bat`** to pin Omnitrix Watch to your Windows Desktop with one click!

---

## 📦 Option B: Building New Release Artifacts Locally

To compile and package the standalone distribution bundle locally:

```powershell
# 1. Activate the environment
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& p:\omniwatch\.venv\Scripts\Activate.ps1)

# 2. Run the release build pipeline
python scripts\build_release.py
```

This automated script will:
- Run PyInstaller to build `dist/OmnitrixWatch/OmnitrixWatch.exe`.
- Inject `README.md`, `LICENSE`, `docs/`, and `config/`.
- Compress into `release/OmnitrixWatch-v<version>-windows-x64.zip`.
- Generate the cryptographic `SHA-256` checksum file.

---

## 🌐 Option C: Publishing the Release on GitHub

### Method 1: Using Git Tags (Triggers Automated GitHub Actions CI/CD)

1. Create and push a version tag:
   ```powershell
   git tag -a v0.1.0 -m "Release v0.1.0: Galvan Prime Protocol"
   git push origin v0.1.0
   ```
2. The GitHub Actions workflow in `.github/workflows/release.yml` will automatically build the Windows binary and publish the release with the zip attached!

---

### Method 2: Using GitHub CLI (`gh`)

If you have GitHub CLI installed:
```powershell
gh release create v0.1.0 release/OmnitrixWatch-v0.1.0-windows-x64.zip release/OmnitrixWatch-v0.1.0-windows-x64.zip.sha256 --title "Omnitrix Watch v0.1.0 — Galvan Prime Protocol" --notes-file RELEASE_NOTES.md
```

---

### Method 3: Via GitHub Web Interface

1. Open your repository on GitHub (`https://github.com/<your-username>/omniwatch`).
2. On the right-hand sidebar, click **Releases** -> **Draft a new release**.
3. Tag version: `v0.1.0` (Select target `main`).
4. Release title: `Omnitrix Watch v0.1.0 — Galvan Prime Protocol`.
5. Copy & paste the contents of [`RELEASE_NOTES.md`](../RELEASE_NOTES.md) into the description.
6. Drag and drop the binary files from `release/`:
   - `OmnitrixWatch-v0.1.0-windows-x64.zip`
   - `OmnitrixWatch-v0.1.0-windows-x64.zip.sha256`
7. Click **Publish release**!
