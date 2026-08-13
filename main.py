"""
ARC - Adaptive Responsive Companion

Application entry point.
"""

from core.assistant import ARCAssistant


APP_NAME = "ARC"
APP_VERSION = "1.0.0"


def main() -> None:
    """Start ARC."""

    print("=" * 50)
    print(f"{APP_NAME} v{APP_VERSION}")
    print("Adaptive Responsive Companion")
    print("=" * 50)

    assistant = ARCAssistant()

    print("\nARC is ready.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower().strip() in {"exit", "quit"}:
            print("ARC: Goodbye!")
            break

        response = assistant.respond(user_input)

        print(f"ARC: {response}")


if __name__ == "__main__":
    main()