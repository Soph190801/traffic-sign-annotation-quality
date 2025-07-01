import scaleapi
from typing import List, Tuple

apiKey = "live_b1c5a645ea7e418a969b42b134e2d2d6"
client = scaleapi.ScaleClient(apiKey)

def getMultipleTasks(filters: dict) -> List[dict]:
    try:
        tasks = client.get_tasks(**filters)
        return [task.as_dict() for task in tasks]
    except Exception as e:
        raise RuntimeError(f"Failed to fetch multiple tasks with filters {filters}: {e}")

def getSingleTask(task_id: str) -> dict:
    try:
        task = client.get_task(task_id)
        return task.as_dict()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch task {task_id}: {e}")


def getTaskInfo(task: dict)  -> Tuple[str, dict, List[dict]]:
    if "response" not in task:
        raise ValueError(f"Task {task.get('task_id')} has no response")

    task_id = task.get("task_id")
    params = task.get("params")
    annotations = task.get("response", {}).get("annotations", [])


    return task_id, params, annotations
