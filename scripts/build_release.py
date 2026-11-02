"""Release builder and packager for Omnitrix Watch."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = PROJECT_ROOT / "dist"
BUILD_DIR = PROJECT_ROOT / "build"
RELEASE_DIR = PROJECT_ROOT / "release"
VERSION = "0.1.0"


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    return sha256.hexdigest()


def build_single_exe() -> Path:
    """Build single standalone .exe file using PyInstaller."""
    print("=" * 65)
    print(f"BUILDING SINGLE-FILE STANDALONE EXECUTABLE (v{VERSION})")
    print("=" * 65)

    pyinstaller_exe = PROJECT_ROOT / ".venv" / "Scripts" / "pyinstaller.exe"
    if not pyinstaller_exe.exists():
        pyinstaller_exe = Path(sys.executable).parent / "pyinstaller.exe"

    if not pyinstaller_exe.exists():
        raise FileNotFoundError("PyInstaller not found. Run: pip install pyinstaller")

    ico_path = PROJECT_ROOT / "assets" / "omnitrix.ico"
    assets_dir = PROJECT_ROOT / "assets"

    # Command arguments for PyInstaller single-file build
    cmd = [
        str(pyinstaller_exe),
        "--noconfirm",
        "--clean",
        "--name",
        "OmnitrixWatch",
        "--onefile",
        "--windowed",
        "--collect-all",
        "bleak",
        "--add-data",
        f"{assets_dir}{os.pathsep}assets",
        "--hidden-import",
        "tkinter",
        "--hidden-import",
        "omnitrix_watch",
        "--paths",
        str(PROJECT_ROOT / "src"),
    ]

    if ico_path.exists():
        cmd.extend(["--icon", str(ico_path)])

    cmd.append(str(PROJECT_ROOT / "src" / "omnitrix_watch" / "main.py"))

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        raise RuntimeError(f"PyInstaller build failed with exit code {result.returncode}")

    single_exe = DIST_DIR / "OmnitrixWatch.exe"
    if not single_exe.exists():
        raise FileNotFoundError(f"Expected single executable {single_exe} was not found.")

    print(f"\n[+] Standalone single-file executable created at: {single_exe}")
    return single_exe


def package_release(single_exe: Path) -> Path:
    """Bundle standalone executable and ancillary files into release/."""
    print("\n" + "=" * 65)
    print("PACKAGING RELEASE ARTIFACTS")
    print("=" * 65)

    RELEASE_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Copy standalone single-click OmnitrixWatch.exe directly into release/
    rel_exe = RELEASE_DIR / "OmnitrixWatch.exe"
    shutil.copy2(single_exe, rel_exe)
    exe_checksum = compute_sha256(rel_exe)
    (RELEASE_DIR / "OmnitrixWatch.exe.sha256").write_text(
        f"{exe_checksum}  OmnitrixWatch.exe\n", encoding="utf-8"
    )
    print(f"[+] Standalone single-click EXE: {rel_exe}")
    print(f"[+] EXE SHA-256: {exe_checksum}")

    # 2. Package complete release bundle zip
    zip_name = f"OmnitrixWatch-v{VERSION}-windows-x64.zip"
    zip_path = RELEASE_DIR / zip_name

    staging_dir = RELEASE_DIR / "staging"
    if staging_dir.exists():
        shutil.rmtree(staging_dir)
    staging_dir.mkdir(parents=True, exist_ok=True)

    shutil.copy2(single_exe, staging_dir / "OmnitrixWatch.exe")
    shutil.copy2(PROJECT_ROOT / "LICENSE", staging_dir / "LICENSE")
    shutil.copy2(PROJECT_ROOT / "README.md", staging_dir / "README.md")
    shutil.copytree(PROJECT_ROOT / "docs", staging_dir / "docs")
    shutil.copytree(PROJECT_ROOT / "config", staging_dir / "config")
    shutil.copytree(PROJECT_ROOT / "assets", staging_dir / "assets")

    # Add quick launcher bat inside zip
    launcher_bat = staging_dir / "Run-Omnitrix.bat"
    launcher_bat.write_text('@echo off\nstart "" "%~dp0OmnitrixWatch.exe"\n', encoding="utf-8")

    print(f"Compressing into {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(staging_dir):
            for file in files:
                abs_p = Path(root) / file
                rel_p = abs_p.relative_to(staging_dir)
                zipf.write(abs_p, arcname=str(rel_p))

    shutil.rmtree(staging_dir)

    zip_checksum = compute_sha256(zip_path)
    (RELEASE_DIR / f"{zip_name}.sha256").write_text(
        f"{zip_checksum}  {zip_name}\n", encoding="utf-8"
    )
    print(f"[+] Release Zip Archive: {zip_path}")
    print(f"[+] Zip SHA-256: {zip_checksum}")

    return rel_exe


def main() -> None:
    """Main build sequence."""
    try:
        single_exe = build_single_exe()
        package_release(single_exe)
        print("\n" + "=" * 65)
        print("ALL RELEASE ARTIFACTS BUILT SUCCESSFULLY!")
        print("=" * 65)
    except Exception as e:
        print(f"\n[-] Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
