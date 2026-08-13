from core.planner import ARCPlanner
from security.policy import ARCSecurity


planner = ARCPlanner()
security = ARCSecurity()


commands = [
    "Notepad kholo",
    "Desktop par ARC folder banao",
    "internet par search karo Python",
]


for command in commands:
    plan = planner.create_plan(command)
    permission = security.check(plan)

    print()
    print("Command:", command)
    print("Action:", plan.action)
    print("Permission:", permission)