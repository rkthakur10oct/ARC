"""
ARC Planner.

Converts natural-language user requests into structured
actions that ARC can later execute through approved tools.
"""

from dataclasses import dataclass
from enum import Enum


class ActionType(Enum):
    """Supported ARC action types."""

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
        """Convert natural-language input into a structured plan."""

        text = user_input.lower().strip()

        # =================================================
        # APPLICATION ALIASES
        # =================================================

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

        # =================================================
        # OPEN APPLICATION
        # =================================================

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

        # =================================================
        # CREATE FOLDER
        # =================================================

        folder_keywords = [
            "folder banao",
            "folder create",
            "folder banana",
            "folder bana do",
            "folder bana",
            "create folder",
            "make folder",
        ]

        folder_request = any(
            keyword in text
            for keyword in folder_keywords
        )

        if folder_request:

            folder_name = self._extract_folder_name(user_input)

            return Plan(
                action=ActionType.CREATE_FOLDER,
                target=folder_name,
            )

        # =================================================
        # WEB SEARCH
        # =================================================

        if (
            "web search" in text
            or "internet par search" in text
            or "internet search" in text
            or "web par search" in text
        ):
            return Plan(
                action=ActionType.SEARCH_WEB,
                target=user_input,
            )

        # =================================================
        # SYSTEM INFORMATION
        # =================================================

        if (
            "system information" in text
            or "system info" in text
            or "computer information" in text
        ):
            return Plan(
                action=ActionType.SYSTEM_INFO,
            )

        # =================================================
        # DEFAULT → CHAT
        # =================================================

        return Plan(
            action=ActionType.CHAT,
        )

    @staticmethod
    def _extract_folder_name(user_input: str) -> str | None:
        """
        Extract folder name from common English/Hinglish commands.

        Examples:

            Desktop par ARC_TEST folder banao
                -> ARC_TEST

            Desktop par ARC naam ka folder banao
                -> ARC

            tech naam se folder banao
                -> tech

            tech folder banao
                -> tech

            ek Notes folder bana do
                -> Notes

            folder banao
                -> None
        """

        text = user_input.strip()

        if not text:
            return None

        lower_text = text.lower()

        # =================================================
        # REMOVE LOCATION PREFIX
        # =================================================

        location_prefixes = [
            "desktop par",
            "desktop pe",
            "desktop mein",
            "desktop me",
        ]

        for prefix in location_prefixes:

            if lower_text.startswith(prefix):

                text = text[len(prefix):].strip()
                lower_text = text.lower()

                break

        # =================================================
        # REMOVE "EK"
        # =================================================

        if lower_text.startswith("ek "):

            text = text[3:].strip()
            lower_text = text.lower()

        # =================================================
        # "ARC NAAM KA FOLDER BANAO"
        # =================================================

        marker = " naam ka folder"

        if marker in lower_text:

            index = lower_text.index(marker)

            folder_name = text[:index].strip()

            if folder_name:
                return folder_name

        # =================================================
        # "TECH NAAM SE FOLDER BANAO"
        # =================================================

        marker = " naam se folder"

        if marker in lower_text:

            index = lower_text.index(marker)

            folder_name = text[:index].strip()

            if folder_name:
                return folder_name

        # =================================================
        # "TECH FOLDER BANAO"
        # =================================================

        folder_markers = [
            " folder banao",
            " folder bana do",
            " folder bana",
            " folder banana",
            " folder create",
        ]

        for marker in folder_markers:

            if marker in lower_text:

                index = lower_text.index(marker)

                folder_name = text[:index].strip()

                if folder_name:
                    return folder_name

        # =================================================
        # "CREATE FOLDER PROJECTS"
        # =================================================

        command_prefixes = [
            "create folder ",
            "make folder ",
        ]

        lower_text = text.lower()

        for prefix in command_prefixes:

            if lower_text.startswith(prefix):

                folder_name = text[len(prefix):].strip()

                if folder_name:
                    return folder_name

        # =================================================
        # NO FOLDER NAME
        # =================================================

        return None