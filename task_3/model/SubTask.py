from task_3.model.StatusType import StatusType
from task_3.model.Task import Task
from task_3.model.TaskType import TaskType


class SubTask(Task):
    def __init__(self, name: str, description: str, epic_task_id: int, unic_task_id, duration=0, start_time=None,
                 status=StatusType.NEW):
        super().__init__(name, description, unic_task_id, duration, start_time, status)
        self.task_type = TaskType.SUB_TASK
        self.epic_task_id = epic_task_id
