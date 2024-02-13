import csv
from task_3.model.TaskType import TaskType
from task_3.test.TestCaseTaskManager import TestCaseTaskManager


class TestCaseFileBackedTasksManager(TestCaseTaskManager):
    def test_save_tasks_to_file(self, manager, task, epic_task, sub_tasks, create_tasks):
        manager.header = 'unic_task_id,task_type,name,status,description,epic_task_id,start_time,duration\n'
        manager.save()
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{manager.file_name}',
                  'r', encoding='utf-8') as file:
            task_file_rows = list(csv.DictReader(file, delimiter=','))
            assert len(create_tasks) == len(task_file_rows)
            for row in task_file_rows:
                task = create_tasks[int(row['unic_task_id'])]
                for key, value in row.items():
                    if task.task_type.name in (TaskType.TASK.name, TaskType.EPIC_TASK.name) and key == 'epic_task_id':
                        break
                    task_value = getattr(task, key)
                    if key == 'task_type':
                        task_value = task_value.name
                    if key == 'status':
                        task_value = task_value.name
                    else:
                        assert value == str(task_value)

    def test_save_task_history_to_file(self, manager, sub_tasks):
        for sub_task in sub_tasks:
            manager.get_task_by_id(sub_task.unic_task_id)
        manager.save()
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{manager.file_name}',
                  'r', encoding='utf-8') as file:
            file_lines = file.readlines()
            last_row = file_lines[-1].split(',')
            assert len(manager.created_tasks) == len(file_lines) - 3
            search_history_ids = list(map(lambda x: int(x), last_row))
        assert search_history_ids == manager.search_history.add_history

    def test_save_empty_file(self, manager):
        manager.delete_all_tasks()
        with open(f'C:\\Users\\stein\\PycharmProjects\\techTasks\\task_3\\history\\{manager.file_name}',
                  'r', encoding='utf-8') as file:
            file_lines = ''.join(file.readlines())
            assert file_lines == manager.header

    def test_create_tasks_from_file(self, task, epic_task, sub_tasks, manager):
        tasks_from_memory = manager.created_tasks
        manager.save()
        manager.file_backed_tasks_manager()
        tasks_from_file = manager.created_tasks
        for key, value in tasks_from_memory.items():
            assert vars(value) == vars(tasks_from_file[key])

    def test_create_tasks_from_empty_file(self, manager):
        manager.delete_all_tasks()
        result = manager.file_backed_tasks_manager()
        assert result == "Файл пустой"
