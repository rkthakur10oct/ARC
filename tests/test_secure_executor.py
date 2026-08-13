from core.planner import ARCPlanner
from core.secure_executor import ARCSecureExecutor


planner = ARCPlanner()
executor = ARCSecureExecutor()


plan = planner.create_plan("Notepad kholo")

print("Action:", plan.action)
print("Target:", plan.target)

result = executor.execute(plan)

print("Result:", result)