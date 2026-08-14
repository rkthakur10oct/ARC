"""
ARC Assistant.

Central orchestration layer for ARC v1.

Responsible for:
- Receiving user input
- Creating an action plan
- Handling missing action targets
- Sending actions to the secure executor
- Managing normal LLM conversation
- Maintaining short-term conversation context
"""

from core.llm import ask_llm
from core.planner import ARCPlanner, ActionType
from core.secure_executor import ARCSecureExecutor


class ARCAssistant:
    """Main orchestration layer for ARC."""

    def __init__(self) -> None:
        """Initialize ARC assistant components."""

        self.name = "ARC"

        # -------------------------------------------------
        # Short-term conversation history
        # -------------------------------------------------

        self.conversation: list[dict[str, str]] = []

        # -------------------------------------------------
        # Core ARC components
        # -------------------------------------------------

        self.planner = ARCPlanner()
        self.executor = ARCSecureExecutor()

    def respond(self, user_input: str) -> str:
        """
        Process a single user request.

        Flow:

            User Input
                ↓
            Planner
                ↓
            Target Validation
                ↓
            Secure Executor
                ↓
            Verification

        Normal conversation follows:

            User Input
                ↓
            LLM
                ↓
            Conversation Memory
        """

        # -------------------------------------------------
        # Validate input
        # -------------------------------------------------

        if not user_input.strip():
            return "Please tell me what you want me to do."

        # -------------------------------------------------
        # Create action plan
        # -------------------------------------------------

        plan = self.planner.create_plan(user_input)

        # -------------------------------------------------
        # Handle missing folder name
        # -------------------------------------------------

        if plan.action == ActionType.CREATE_FOLDER and not plan.target:
            return "Kaunsa folder banana hai?"

        # -------------------------------------------------
        # Handle missing file name
        # -------------------------------------------------

        if plan.action == ActionType.CREATE_FILE and not plan.target:
            return "Kaunsi file banani hai?"

        # -------------------------------------------------
        # Execute non-chat actions
        # -------------------------------------------------

        if plan.action != ActionType.CHAT:
            return self.executor.execute(plan)

        # -------------------------------------------------
        # Normal conversation
        # -------------------------------------------------

        self.conversation.append(
            {
                "role": "user",
                "content": user_input,
            }
        )

        # Ask local LLM.
        response = ask_llm(self.conversation)

        # Store assistant response.
        self.conversation.append(
            {
                "role": "assistant",
                "content": response,
            }
        )

        return response

    def clear_conversation(self) -> None:
        """Clear the current short-term conversation context."""

        self.conversation.clear()
