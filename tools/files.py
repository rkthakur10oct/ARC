"""
ARC File Tools.

Provides bounded file and folder operations for ARC.
"""

from pathlib import Path


def get_desktop_path() -> Path:
    """Return the current user's Windows Desktop path."""

    return Path.home() / "Desktop"


def create_folder(folder_name: str) -> Path:
    """
    Create a folder on the user's Desktop.

    Returns:
        Path of the created/existing folder.
    """

    folder_name = folder_name.strip()

    if not folder_name:
        raise ValueError("Folder name cannot be empty.")

    folder_path = get_desktop_path() / folder_name

    folder_path.mkdir(
        parents=False,
        exist_ok=True,
    )

    return folder_path