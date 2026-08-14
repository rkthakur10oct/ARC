from core.planner import ARCPlanner
from core.secure_executor import ARCSecureExecutor


planner = ARCPlanner()
executor = ARCSecureExecutor()


command = "Desktop par ARC_PIPELINE_TEST folder banao"

plan = planner.create_plan(command)

print("Command:", command)
print("Action:", plan.action)
print("Target:", plan.target)

result = executor.execute(plan)

print("Result:", result)