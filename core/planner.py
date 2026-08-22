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
    location: str | None = None
    requires_confirmation: bool = False


class ARCPlanner:
    """Creates structured plans from user requests."""

    def create_plan(self, user_input: str) -> Plan:
        """
        Convert natural-language input into a structured plan.

        The current planner intentionally uses deterministic
        rules. LLM-based planning will be added later.
        """

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

            app_detected = any(alias in text for alias in aliases)

            open_requested = any(phrase in text for phrase in open_words)

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

        folder_request = any(keyword in text for keyword in folder_keywords)

        if folder_request:

            folder_name = self._extract_folder_name(user_input)
            location = self._extract_location(user_input)

            return Plan(
                action=ActionType.CREATE_FOLDER,
                target=folder_name,
                location=location,
            )

        # =================================================
        # CREATE FILE
        # =================================================

        file_keywords = [
            "file banao",
            "file bana do",
            "file create",
            "file banana",
            "create file",
            "make file",
        ]

        file_request = any(keyword in text for keyword in file_keywords)

        if file_request:

            file_name = self._extract_file_name(user_input)
            location = self._extract_location(user_input)

            return Plan(
                action=ActionType.CREATE_FILE,
                target=file_name,
                location=location,
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

    # =====================================================
    # LOCATION EXTRACTION
    # =====================================================

    @staticmethod
    def _extract_location(
        user_input: str,
    ) -> str | None:
        """
        Extract a requested location from a natural-language command.

        Examples:

            Desktop par notes.txt file banao
                -> Desktop

            Documents mein report.pdf file banao
                -> Documents

            Downloads mein data.csv file banao
                -> Downloads

            D:\\Projects mein main.py file banao
                -> D:\\Projects

            notes.txt file banao
                -> None
        """

        text = user_input.strip()

        if not text:
            return None

        lower_text = text.lower()

        # -------------------------------------------------
        # Known Windows/user locations
        # -------------------------------------------------

        location_patterns = [
            ("desktop par", "Desktop"),
            ("desktop pe", "Desktop"),
            ("desktop mein", "Desktop"),
            ("desktop me", "Desktop"),
            ("documents mein", "Documents"),
            ("documents me", "Documents"),
            ("documents par", "Documents"),
            ("documents pe", "Documents"),
            ("downloads mein", "Downloads"),
            ("downloads me", "Downloads"),
            ("downloads par", "Downloads"),
            ("downloads pe", "Downloads"),
        ]

        for phrase, location in location_patterns:

            if phrase in lower_text:
                return location

        # -------------------------------------------------
        # Absolute Windows path
        # -------------------------------------------------

        if len(text) >= 3 and text[1:3] == ":\\":
            path_endings = [
                " file banao",
                " file bana do",
                " file create",
                " folder banao",
                " folder bana do",
                " folder create",
            ]

            for ending in path_endings:

                index = lower_text.find(ending)

                if index != -1:
                    path = text[:index].strip()

                    if path:
                        return path

        return None

    # =====================================================
    # FOLDER NAME EXTRACTION
    # =====================================================

    @staticmethod
    def _extract_folder_name(
        user_input: str,
    ) -> str | None:
        """
        Extract a folder name from common English/Hinglish commands.

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

        # -------------------------------------------------
        # Remove location prefix
        # -------------------------------------------------

        location_prefixes = [
            "desktop par",
            "desktop pe",
            "desktop mein",
            "desktop me",
            "documents mein",
            "documents me",
            "documents par",
            "documents pe",
            "downloads mein",
            "downloads me",
            "downloads par",
            "downloads pe",
        ]

        for prefix in location_prefixes:

            if lower_text.startswith(prefix):

                text = text[len(prefix) :].strip()
                lower_text = text.lower()

                break

        # -------------------------------------------------
        # Remove "ek"
        # -------------------------------------------------

        if lower_text.startswith("ek "):

            text = text[3:].strip()
            lower_text = text.lower()

        # -------------------------------------------------
        # "ARC naam ka folder banao"
        # -------------------------------------------------

        marker = " naam ka folder"

        if marker in lower_text:

            index = lower_text.index(marker)

            folder_name = text[:index].strip()

            if folder_name:
                return folder_name

        # -------------------------------------------------
        # "tech naam se folder banao"
        # -------------------------------------------------

        marker = " naam se folder"

        if marker in lower_text:

            index = lower_text.index(marker)

            folder_name = text[:index].strip()

            if folder_name:
                return folder_name

        # -------------------------------------------------
        # "tech folder banao"
        # -------------------------------------------------

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

        # -------------------------------------------------
        # "create folder Projects"
        # -------------------------------------------------

        command_prefixes = [
            "create folder ",
            "make folder ",
        ]

        for prefix in command_prefixes:

            if lower_text.startswith(prefix):

                folder_name = text[len(prefix) :].strip()

                if folder_name:
                    return folder_name

        return None

    # =====================================================
    # FILE NAME EXTRACTION
    # =====================================================

    @staticmethod
    def _extract_file_name(
        user_input: str,
    ) -> str | None:
        """
        Extract a file name from common English/Hinglish commands.

        Examples:

            Desktop par notes.txt file banao
                -> notes.txt

            hello.txt naam ki file banao
                -> hello.txt

            report.txt naam se file banao
                -> report.txt

            create file project.txt
                -> project.txt

            file banao
                -> None
        """

        text = user_input.strip()

        if not text:
            return None

        lower_text = text.lower()

        # -------------------------------------------------
        # Remove location prefix
        # -------------------------------------------------

        location_prefixes = [
            "desktop par",
            "desktop pe",
            "desktop mein",
            "desktop me",
            "documents mein",
            "documents me",
            "documents par",
            "documents pe",
            "downloads mein",
            "downloads me",
            "downloads par",
            "downloads pe",
        ]

        for prefix in location_prefixes:

            if lower_text.startswith(prefix):

                text = text[len(prefix) :].strip()
                lower_text = text.lower()

                break

        # -------------------------------------------------
        # Remove "ek"
        # -------------------------------------------------

        if lower_text.startswith("ek "):

            text = text[3:].strip()
            lower_text = text.lower()

        # -------------------------------------------------
        # "notes.txt naam ki file banao"
        # -------------------------------------------------

        marker = " naam ki file"

        if marker in lower_text:

            index = lower_text.index(marker)

            file_name = text[:index].strip()

            if file_name:
                return file_name

        # -------------------------------------------------
        # "notes.txt naam se file banao"
        # -------------------------------------------------

        marker = " naam se file"

        if marker in lower_text:

            index = lower_text.index(marker)

            file_name = text[:index].strip()

            if file_name:
                return file_name

        # -------------------------------------------------
        # "notes.txt file banao"
        # -------------------------------------------------

        file_markers = [
            " file banao",
            " file bana do",
            " file bana",
            " file banana",
            " file create",
        ]

        for marker in file_markers:

            if marker in lower_text:

                index = lower_text.index(marker)

                file_name = text[:index].strip()

                if file_name:
                    return file_name

        # -------------------------------------------------
        # "create file notes.txt"
        # -------------------------------------------------

        command_prefixes = [
            "create file ",
            "make file ",
        ]

        for prefix in command_prefixes:

            if lower_text.startswith(prefix):

                file_name = text[len(prefix) :].strip()

                if file_name:
                    return file_name

        return None
