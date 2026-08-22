"""
ARC File Tools.

Provides controlled file and folder operations for ARC.
"""

from pathlib import Path
import os


def get_desktop_path() -> Path:
    """
    Return the current user's Desktop directory.
    """

    return Path.home() / "Desktop"


def get_documents_path() -> Path:
    """
    Return the current user's Documents directory.
    """

    return Path.home() / "Documents"


def get_downloads_path() -> Path:
    """
    Return the current user's Downloads directory.
    """

    return Path.home() / "Downloads"


def resolve_location(location: str | None) -> Path:
    """
    Resolve a user-requested location.

    Supported locations:

        None
        Desktop
        Documents
        Downloads
        Absolute Windows paths
        Relative paths

    If no location is provided, Desktop is used.
    """

    # ---------------------------------------------
    # Default location
    # ---------------------------------------------

    if not location:
        return get_desktop_path()

    location = location.strip()

    if not location:
        return get_desktop_path()

    # ---------------------------------------------
    # Known user directories
    # ---------------------------------------------

    normalized = location.lower()

    known_locations = {
        "desktop": get_desktop_path(),
        "documents": get_documents_path(),
        "downloads": get_downloads_path(),
    }

    if normalized in known_locations:
        return known_locations[normalized]

    # ---------------------------------------------
    # Absolute path
    # ---------------------------------------------

    path = Path(location)

    if path.is_absolute():
        return path

    # ---------------------------------------------
    # Relative path
    #
    # Relative locations are resolved from Desktop.
    #
    # Example:
    #
    # Projects
    # → Desktop\Projects
    # ---------------------------------------------

    return get_desktop_path() / path


def create_folder(
    folder_name: str,
    location: str | None = None,
) -> Path:
    """
    Create a folder inside the requested location.

    Examples:

        create_folder("ARC")
        → Desktop\\ARC

        create_folder("ARC", "Documents")
        → Documents\\ARC

        create_folder("ARC", "D:\\Projects")
        → D:\\Projects\\ARC
    """

    if not folder_name:
        raise ValueError("Folder name cannot be empty.")

    base_path = resolve_location(location)

    folder_path = base_path / folder_name

    folder_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    return folder_path


def create_file(
    file_name: str,
    location: str | None = None,
) -> Path:
    """
    Create an empty file inside the requested location.

    Examples:

        create_file("notes.txt")
        → Desktop\\notes.txt

        create_file("data.csv", "Documents")
        → Documents\\data.csv

        create_file("main.py", "D:\\Projects")
        → D:\\Projects\\main.py
    """

    if not file_name:
        raise ValueError("File name cannot be empty.")

    base_path = resolve_location(location)

    file_path = base_path / file_name

    # Create parent directories if necessary.
    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Create the file without modifying existing content.
    file_path.touch(
        exist_ok=True,
    )

    return file_path
