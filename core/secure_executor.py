"""
ARC Secure Executor.

Connects planning, security, execution, and verification
into a single controlled execution pipeline.
"""

from core.executor import ARCExecutor
from core.planner import ActionType, Plan
from security.policy import ARCSecurity, Permission
from verification.windows import is_app_running


class ARCSecureExecutor:
    """Security-gated and verification-aware executor."""

    def __init__(self) -> None:
        self.security = ARCSecurity()
        self.executor = ARCExecutor()

    def execute(self, plan: Plan) -> str:
        """Securely execute and verify an ARC plan."""

        # Step 1: Security check
        permission = self.security.check(plan)

        if permission == Permission.RESTRICTED:
            return "This action is restricted and cannot be executed."

        if permission == Permission.CONFIRM:
            return "Confirmation required before executing this action."

        # Step 2: Execute
        result = self.executor.execute(plan)

        # Step 3: Verify
        if plan.action == ActionType.OPEN_APP:
            if not plan.target:
                return "Application target is missing."

            verified = is_app_running(plan.target)

            if verified:
                return f"Verified: {plan.target} is running."

            return (
                f"Execution was attempted, but I could not verify "
                f"that {plan.target} is running."
            )

        # Other action types will receive their own
        # verification logic as we implement them.
        return result