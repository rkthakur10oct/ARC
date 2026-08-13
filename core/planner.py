"""
ARC Planner.

Converts natural-language user requests into structured
actions that ARC can later execute through approved tools.
"""

from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    CHAT = "chat"
    OPEN_APP = "open_app"
    CREATE_FOLDER = "create_folder"
    CREATE_FILE = "create_file"
    SEARCH_WEB = "search_web"
    SYSTEM_INFO = "system_info"


@dataclass
class Plan:
    """Represents a planned ARC action."""

    action: ActionType
    target: str | None = None
    requires_confirmation: bool = False


class ARCPlanner:
    """Creates structured plans from user requests."""

    def create_plan(self, user_input: str) -> Plan:
        """
        Convert user input into a basic action plan.

        This first version intentionally uses simple rules.
        LLM-based planning will be added after the tool layer
        is established.
        """

        text = user_input.lower().strip()

        # -------------------------------------------------
        # Application aliases
        # -------------------------------------------------

        app_aliases = {
            "notepad": [
                "notepad",
                "note pad",
            ],
            "chrome": [
                "chrome",
                "google chrome",
            ],
            "calculator": [
                "calculator",
                "calc",
            ],
            "paint": [
                "paint",
                "ms paint",
            ],
        }

        # -------------------------------------------------
        # Words / phrases indicating an open request
        # -------------------------------------------------

        open_words = [
            "khol",
            "kholo",
            "open",
            "launch",
            "start",
            "chalao",
            "chala",
            "shuru karo",
            "open kro",
        ]

        # -------------------------------------------------
        # Detect application-open requests
        # -------------------------------------------------

        for app_name, aliases in app_aliases.items():

            app_detected = any(
                alias in text
                for alias in aliases
            )

            open_requested = any(
                phrase in text
                for phrase in open_words
            )

            if app_detected and open_requested:
                return Plan(
                    action=ActionType.OPEN_APP,
                    target=app_name,
                )

        # -------------------------------------------------
        # Folder creation
        # -------------------------------------------------

        if (
            "folder banao" in text
            or "folder create" in text
            or "folder banana" in text
        ):
            return Plan(
                action=ActionType.CREATE_FOLDER,
                target=user_input,
            )

        # -------------------------------------------------
        # Web search
        # -------------------------------------------------

        if (
            "web search" in text
            or "internet par search" in text
        ):
            return Plan(
                action=ActionType.SEARCH_WEB,
                target=user_input,
            )

        # -------------------------------------------------
        # System information
        # -------------------------------------------------

        if (
            "system information" in text
            or "system info" in text
        ):
            return Plan(
                action=ActionType.SYSTEM_INFO,
            )

        # -------------------------------------------------
        # Default: normal conversation
        # -------------------------------------------------

        return Plan(
            action=ActionType.CHAT,
        )