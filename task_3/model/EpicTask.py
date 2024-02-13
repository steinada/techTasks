from task_3.model.StatusType import StatusType
from task_3.model.Task import Task
from task_3.model.TaskType import TaskType


class EpicTask(Task):
    def __init__(self, name: str, description: str, unic_task_id, duration=0, start_time=None, status=StatusType.NEW,
                 sub_tasks_id=None):
        super().__init__(name, description, unic_task_id, duration, start_time, status)
        if sub_tasks_id is None:
            self.sub_tasks_id = list()
        self.task_type = TaskType.EPIC_TASK

    def add_sub_task(self, sub_task_id):
        if sub_task_id not in self.sub_tasks_id:
            self.sub_tasks_id.append(sub_task_id)
