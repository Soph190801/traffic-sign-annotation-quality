from runChecks import runChecks
from taskRetrieval import getMultipleTasks, getSingleTask

class ErrorGenerator:
    def __init__(self, mode: str, task_id: str = None, filters: dict = None):
        if mode not in ["single", "multiple"]:
            raise ValueError("mode must be 'single' or 'multiple'")
        
        self.mode = mode
        self.task_id = task_id
        self.filters = filters or {}

        if mode == "single" and not task_id:
            raise ValueError("task_id is required for single-task mode")
        if mode == "multiple" and not filters:
            raise ValueError("filters are required for multi-task mode")

    def getErrorsByTask(self) -> dict:
        errors_by_task = {}
        if self.mode == "single":
            task = getSingleTask(self.task_id)
            task_id, task_errors = runChecks(task)

            errors_by_task[task_id] = task_errors
        else:
            tasks = getMultipleTasks(self.filters)
            for task in tasks:
                task_id, task_errors = runChecks(task)
                errors_by_task[task_id] = task_errors
        return errors_by_task