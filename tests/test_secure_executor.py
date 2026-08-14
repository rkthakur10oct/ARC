"""
Tests for ARC Secure Executor.
"""

from core.planner import ActionType, Plan
from core.secure_executor import ARCSecureExecutor


def test_create_file() -> None:
    """Test secure file creation and verification."""

    executor = ARCSecureExecutor()

    plan = Plan(
        action=ActionType.CREATE_FILE,
        target="ARC_PIPELINE_TEST.txt",
    )

    result = executor.execute(plan)

    print("Action:", plan.action)
    print("Target:", plan.target)
    print("Result:", result)


if __name__ == "__main__":
    test_create_file()
