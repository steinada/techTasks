from task_3.model.StatusType import StatusType
from task_3.model.TaskType import TaskType


class Task:
    def __init__(self, name: str, description: str, unic_task_id, duration=0, start_time=None, status=StatusType.NEW):
        self.unic_task_id = unic_task_id
        self.name = name
        self.description = description
        self.status = status
        self.task_type = TaskType.TASK
        self.duration = duration
        self.start_time = start_time
