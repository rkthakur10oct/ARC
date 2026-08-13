"""
ARC Windows Tools.

Safe, bounded Windows operations that can be called
by the ARC execution layer.
"""

import os
import subprocess


SUPPORTED_APPS = {
    "notepad": "notepad.exe",
    "calculator": "calc.exe",
    "paint": "mspaint.exe",
}


CHROME_PATHS = [
    os.path.expandvars(
        r"%PROGRAMFILES%\Google\Chrome\Application\chrome.exe"
    ),
    os.path.expandvars(
        r"%PROGRAMFILES(X86)%\Google\Chrome\Application\chrome.exe"
    ),
    os.path.expandvars(
        r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
    ),
]


def _find_chrome() -> str | None:
    """Find Google Chrome in common Windows installation paths."""

    for path in CHROME_PATHS:
        if os.path.isfile(path):
            return path

    return None


def open_app(app_name: str) -> bool:
    """
    Open a supported Windows application.
    """

    app = app_name.lower().strip()

    if app == "chrome":
        chrome_path = _find_chrome()

        if chrome_path is None:
            return False

        subprocess.Popen(
            [chrome_path],
            shell=False,
        )

        return True

    if app not in SUPPORTED_APPS:
        return False

    subprocess.Popen(
        [SUPPORTED_APPS[app]],
        shell=False,
    )

    return True