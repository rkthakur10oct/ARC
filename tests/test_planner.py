from core.planner import ARCPlanner, ActionType


planner = ARCPlanner()


plan = planner.create_plan(
    "Desktop par ARC naam ka folder banao."
)

print("Action:", plan.action)
print("Target:", plan.target)
print("Confirmation:", plan.requires_confirmation)