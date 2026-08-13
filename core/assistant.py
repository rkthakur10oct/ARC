"""
ARC Assistant.

Central orchestration layer for ARC v1.
"""

from core.llm import ask_llm
from core.planner import ARCPlanner, ActionType
from core.secure_executor import ARCSecureExecutor


class ARCAssistant:
    """Main orchestration layer for ARC."""

    def __init__(self) -> None:
        self.name = "ARC"

        # Short-term conversation history.
        self.conversation: list[dict] = []

        # Core components.
        self.planner = ARCPlanner()
        self.executor = ARCSecureExecutor()

    def respond(self, user_input: str) -> str:
        """
        Process user input.

        Chat requests go to the LLM.
        Action requests go through:

        Planner → Security → Executor → Verification
        """

        if not user_input.strip():
            return "Please tell me what you want me to do."

        # Create a plan first.
        plan = self.planner.create_plan(user_input)

        # Action request.
        if plan.action != ActionType.CHAT:
            return self.executor.execute(plan)

        # Normal conversation.
        self.conversation.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        response = ask_llm(self.conversation)

        self.conversation.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def clear_conversation(self) -> None:
        """Clear current session context."""

        self.conversation.clear()