"""
ARC Windows Verification.

Verifies whether requested Windows applications
are actually running after an execution attempt.
"""

import subprocess


PROCESS_NAMES = {
    "notepad": "notepad.exe",
    "chrome": "chrome.exe",
    "calculator": "CalculatorApp.exe",
    "paint": "mspaint.exe",
}


def is_app_running(app_name: str) -> bool:
    """
    Check whether an application process is currently running.
    """

    app = app_name.lower().strip()

    process_name = PROCESS_NAMES.get(app)

    if process_name is None:
        return False

    result = subprocess.run(
        [
            "tasklist",
            "/FI",
            f"IMAGENAME eq {process_name}",
        ],
        capture_output=True,
        text=True,
        shell=False,
    )

    return process_name.lower() in result.stdout.lower()