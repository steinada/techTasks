from task_3.InMemoryTaskManager import InMemoryTaskManager
from task_3.model.TaskType import TaskType


class FileBackedTasksManager(InMemoryTaskManager):
    def __init__(self, file='history_file.csv'):
        super().__init__()
        self.file_name = file
        self.header = 'id,type,name,status,description,epic,start_time,duration\n'

    def save(self):
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{self.file_name}', 'w',  encoding='utf-8') as file:
            file.write(self.header)
            for task in self.created_tasks.values():
                file.write(self.make_task_string(task))
            add_history = list(map(lambda x: str(x), self.search_history.add_history))
            if add_history:
                file.write(f'\n{",".join(add_history)}')

    @staticmethod
    def make_task_string(task):
        string_to_write = (f'{task.unic_task_id},{task.task_type.name},{task.name},{task.status.name},'
                           f'{task.description}')
        if task.task_type.name == TaskType.SUB_TASK.name:
            string_to_write += f',{str(task.epic_task_id)}'
        string_to_write += f',{task.start_time},{task.duration}'
        return string_to_write + '\n'

    def create_any_task(self, name=None, description=None, task_type=None, epic_task_id=None, duration=0,
                        start_time=None):
        task = super().create_any_task(name, description, task_type, epic_task_id, duration, start_time)
        self.save()
        return task

    def update_any_task(self, task_id=None, name=None, description=None, status=None, sub_checked=None,
                        duration=0, start_time=None):
        task = super().update_any_task(task_id, name, description, status, sub_checked, start_time, duration)
        self.save()
        return task

    def delete_all_tasks(self):
        super().delete_all_tasks()
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{self.file_name}', 'w', encoding='utf-8') as file:
            file.write(self.header)

    def delete_task_by_id(self, task_id=None):
        result = super().delete_task_by_id(task_id)
        self.save()
        return result

    def get_task_by_id(self, task_id=None):
        result = super().get_task_by_id(task_id)
        self.save()
        return result

    def file_backed_tasks_manager(self):
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{self.file_name}', 'r',  encoding='utf-8') as file:
            file.readline()
            for line in file.readlines():
                if line == '\n':
                    break
                task_data = line.strip().split(',')
                if task_data[1] == "SUB_TASK":
                    task_id, task_type, name, status, description, epic, start_time, duration = task_data
                    task_id, epic = int(task_id), int(epic)
                    epic_task = self.created_tasks[epic]
                    epic_task.add_sub_task(task_id)
                else:
                    task_id, task_type, name, status, description, start_time, duration = task_data
                    task_id, epic = int(task_id), None
                InMemoryTaskManager.unic_task_id = task_id
                self.create_any_task(name, description, task_type, epic)
                if status != "NEW":
                    self.update_any_task(task_id=task_id, status=status, sub_checked=True)
            if self.created_tasks == {}:
                return "Файл пустой"
            InMemoryTaskManager.unic_task_id = max(self.created_tasks) + 1
            history_line = file.readline()
            history = history_line.strip().split(',')
            if history_line:
                for task_id in history:
                    self.get_task_by_id(int(task_id))
