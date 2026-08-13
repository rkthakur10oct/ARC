from core.executor import ARCExecutor
from core.planner import ARCPlanner


planner = ARCPlanner()
executor = ARCExecutor()

plan = planner.create_plan("opera kholo")

print("Planned action:", plan.action)
print("Target:", plan.target)

result = executor.execute(plan)

print("Execution result:", result)