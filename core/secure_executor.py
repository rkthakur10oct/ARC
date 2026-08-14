"""
ARC Secure Executor.

Connects planning, security, execution, and verification
into a controlled execution pipeline.
"""

from pathlib import Path

from core.executor import ARCExecutor
from core.planner import ActionType, Plan
from security.policy import ARCSecurity, Permission
from verification.files import file_exists, folder_exists
from verification.windows import is_app_running


class ARCSecureExecutor:
    """Security-gated and verification-aware executor."""

    def __init__(self) -> None:
        """Initialize security and execution components."""

        self.security = ARCSecurity()
        self.executor = ARCExecutor()

    def execute(self, plan: Plan) -> str:
        """
        Securely execute and verify an ARC plan.

        Flow:

            Security
                ↓
            Executor
                ↓
            Verification
                ↓
            Result
        """

        # ==============================================
        # SECURITY CHECK
        # ==============================================

        permission = self.security.check(plan)

        if permission == Permission.RESTRICTED:
            return "This action is restricted and cannot be executed."

        if permission == Permission.CONFIRM:
            return "Confirmation required before executing this action."

        # ==============================================
        # OPEN APPLICATION
        # ==============================================

        if plan.action == ActionType.OPEN_APP:

            self.executor.execute(plan)

            if not plan.target:
                return "Application target is missing."

            if is_app_running(plan.target):
                return f"Verified: {plan.target} is running."

            return (
                "Execution was attempted, but I could not verify "
                f"that {plan.target} is running."
            )

        # ==============================================
        # CREATE FOLDER
        # ==============================================

        if plan.action == ActionType.CREATE_FOLDER:

            result = self.executor.execute(plan)

            if result.startswith("Folder creation failed"):
                return result

            folder_path = Path(result)

            if folder_exists(folder_path):
                return f"Verified: folder exists at {folder_path}"

            return (
                "Folder creation was attempted, " "but I could not verify the folder."
            )

        # ==============================================
        # CREATE FILE
        # ==============================================

        if plan.action == ActionType.CREATE_FILE:

            result = self.executor.execute(plan)

            if result.startswith("File creation failed"):
                return result

            file_path = Path(result)

            if file_exists(file_path):
                return f"Verified: file exists at {file_path}"

            return "File creation was attempted, " "but I could not verify the file."

        # ==============================================
        # OTHER ACTIONS
        # ==============================================

        return self.executor.execute(plan)
