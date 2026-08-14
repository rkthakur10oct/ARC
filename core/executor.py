"""
ARC Executor.

Executes approved ARC plans using bounded tools.
"""

from core.planner import ActionType, Plan
from tools.files import create_folder
from tools.windows import open_app


class ARCExecutor:
    """Execute approved ARC plans."""

    def execute(self, plan: Plan) -> str:
        """Execute a planned action."""

        # ==============================================
        # OPEN APPLICATION
        # ==============================================

        if plan.action == ActionType.OPEN_APP:

            if not plan.target:
                return "I don't know which application to open."

            success = open_app(plan.target)

            if success:
                return f"{plan.target} opened successfully."

            return (
                f"I cannot open '{plan.target}'. "
                "It is not a supported application."
            )

        # ==============================================
        # CREATE FOLDER
        # ==============================================

        if plan.action == ActionType.CREATE_FOLDER:

            if not plan.target:
                return "I couldn't determine the folder name."

            try:
                folder_path = create_folder(plan.target)

                return str(folder_path)

            except Exception as exc:
                return f"Folder creation failed: {exc}"

        # ==============================================
        # OTHER ACTIONS
        # ==============================================

        return "This action is not implemented yet."