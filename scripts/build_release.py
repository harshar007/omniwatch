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


def build_executable() -> Path:
    """Build standalone executable using PyInstaller."""
    print("=" * 65)
    print(f"BUILDING OMNITRIX WATCH STANDALONE EXECUTABLE (v{VERSION})")
    print("=" * 65)

    pyinstaller_exe = PROJECT_ROOT / ".venv" / "Scripts" / "pyinstaller.exe"
    if not pyinstaller_exe.exists():
        pyinstaller_exe = Path(sys.executable).parent / "pyinstaller.exe"

    if not pyinstaller_exe.exists():
        raise FileNotFoundError("PyInstaller not found. Run: pip install pyinstaller")

    # Command arguments for PyInstaller
    cmd = [
        str(pyinstaller_exe),
        "--noconfirm",
        "--clean",
        "--name",
        "OmnitrixWatch",
        "--onedir",
        "--windowed",
        "--collect-all",
        "bleak",
        "--hidden-import",
        "tkinter",
        "--hidden-import",
        "omnitrix_watch",
        "--paths",
        str(PROJECT_ROOT / "src"),
        str(PROJECT_ROOT / "src" / "omnitrix_watch" / "main.py"),
    ]

    print(f"Running: {' '.join(cmd)}\n")
    result = subprocess.run(cmd, cwd=str(PROJECT_ROOT))
    if result.returncode != 0:
        raise RuntimeError(f"PyInstaller build failed with exit code {result.returncode}")

    output_dir = DIST_DIR / "OmnitrixWatch"
    if not output_dir.exists():
        raise FileNotFoundError(f"Expected output folder {output_dir} was not created.")

    print(f"\n[+] Standalone executable folder created at: {output_dir}")
    return output_dir


def package_release(output_dir: Path) -> Path:
    """Bundle executable folder into release zip archive."""
    print("\n" + "=" * 65)
    print("PACKAGING RELEASE ARTIFACTS")
    print("=" * 65)

    RELEASE_DIR.mkdir(parents=True, exist_ok=True)
    zip_name = f"OmnitrixWatch-v{VERSION}-windows-x64.zip"
    zip_path = RELEASE_DIR / zip_name

    # Copy ancillary files into the distribution folder
    shutil.copy2(PROJECT_ROOT / "LICENSE", output_dir / "LICENSE")
    shutil.copy2(PROJECT_ROOT / "README.md", output_dir / "README.md")
    
    docs_dest = output_dir / "docs"
    if docs_dest.exists():
        shutil.rmtree(docs_dest)
    shutil.copytree(PROJECT_ROOT / "docs", docs_dest)

    config_dest = output_dir / "config"
    if config_dest.exists():
        shutil.rmtree(config_dest)
    shutil.copytree(PROJECT_ROOT / "config", config_dest)

    # Create root launcher inside the release zip
    launcher_content = """@echo off
start "" "%~dp0OmnitrixWatch\\OmnitrixWatch.exe"
"""
    launcher_path = RELEASE_DIR / "Run-Omnitrix.bat"
    launcher_path.write_text(launcher_content, encoding="utf-8")

    print(f"Compressing into {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add root runner
        zipf.write(launcher_path, arcname="Run-Omnitrix.bat")
        
        # Add all files in output_dir
        for root, _, files in os.walk(output_dir):
            for file in files:
                abs_path = Path(root) / file
                rel_path = abs_path.relative_to(DIST_DIR)
                zipf.write(abs_path, arcname=str(rel_path))

    if launcher_path.exists():
        launcher_path.unlink()

    # Generate checksum
    checksum = compute_sha256(zip_path)
    checksum_file = RELEASE_DIR / f"{zip_name}.sha256"
    checksum_file.write_text(f"{checksum}  {zip_name}\n", encoding="utf-8")

    print(f"[+] Release archive: {zip_path}")
    print(f"[+] SHA-256 Checksum: {checksum}")
    print(f"[+] Checksum file: {checksum_file}")

    return zip_path


def main() -> None:
    """Main build sequence."""
    try:
        output_dir = build_executable()
        zip_path = package_release(output_dir)
        print("\n" + "=" * 65)
        print("RELEASE BUILD COMPLETE AND READY FOR DISTRIBUTION!")
        print("=" * 65)
    except Exception as e:
        print(f"\n[-] Build failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
