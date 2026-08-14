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

def file_exists(file_path: Path) -> bool:
    """
    Verify that a file exists and is actually a file.
    """

    return file_path.exists() and file_path.is_file()