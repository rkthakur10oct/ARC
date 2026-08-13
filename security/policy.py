"""
ARC Security Policy.

Determines whether an action can execute directly,
requires confirmation, or is restricted.
"""

from enum import Enum

from core.planner import ActionType, Plan


class Permission(Enum):
    DIRECT = "direct"
    CONFIRM = "confirm"
    RESTRICTED = "restricted"


class ARCSecurity:
    """Security policy enforcement for ARC actions."""

    def check(self, plan: Plan) -> Permission:
        """
        Determine the permission level required for a plan.
        """

        if plan.action in {
            ActionType.OPEN_APP,
            ActionType.SYSTEM_INFO,
            ActionType.CHAT,
        }:
            return Permission.DIRECT

        if plan.action in {
            ActionType.CREATE_FOLDER,
            ActionType.CREATE_FILE,
            ActionType.SEARCH_WEB,
        }:
            return Permission.DIRECT

        return Permission.RESTRICTED