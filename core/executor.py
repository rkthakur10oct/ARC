"""
ARC Executor.

Takes an approved plan and executes the corresponding
bounded tool operation.
"""

from core.planner import ActionType, Plan
from tools.windows import open_app


class ARCExecutor:
    """Execute approved ARC plans."""

    def execute(self, plan: Plan) -> str:
        """Execute a plan using approved tools."""

        if plan.action == ActionType.OPEN_APP:
            if not plan.target:
                return "I don't know which application to open."

            success = open_app(plan.target)

            if success:
                return f"{plan.target} opened successfully."

            return f"I cannot open '{plan.target}'. It is not a supported application."

        return "This action is not implemented yet."