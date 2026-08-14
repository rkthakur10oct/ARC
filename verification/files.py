"""
ARC File Verification.

Verifies file and folder operations performed by ARC.
"""

from pathlib import Path


def folder_exists(folder_path: Path) -> bool:
    """
    Verify that a folder exists and is actually a directory.
    """

    return folder_path.exists() and folder_path.is_dir()