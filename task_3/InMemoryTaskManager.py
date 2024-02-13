from task_3.model.Task import Task
from task_3.model.StatusType import StatusType
from task_3.model.TaskType import TaskType
from task_3.model.SubTask import SubTask
from task_3.model.EpicTask import EpicTask
from task_3.TaskManager import TaskManager
from task_3.InMemoryHistoryManager import LinkedList
from datetime import date, timedelta
from copy import deepcopy


class InMemoryTaskManager(TaskManager):
    unic_task_id = 0

    def __init__(self):
        self.created_tasks = dict()
        self.search_history = LinkedList(10)

    @staticmethod
    def check_entry_id(func):
        def wrapper(obj, entry_id=None):
            self = obj
            if entry_id is None:
                return "Empty id"
            if entry_id in self.created_tasks:
                return func(obj, entry_id)
            else:
                return "No task by id"
        return wrapper

    def create_any_task(
            self, name=None, description=None, task_type=None, epic_task_id=None, duration=0, start_time=None):
        if start_time is not None:
            find_intersections = self.check_intersections(start_time, duration)
            if find_intersections[0]:
                return f"Task intersections with: {', '.join(find_intersections[1])}"
        if task_type == "TASK":
            new_task = Task(name, description, self.unic_task_id, duration, start_time)
        elif task_type == "SUB_TASK":
            new_task = SubTask(name, description, epic_task_id, self.unic_task_id, duration, start_time)
            if epic_task_id not in self.created_tasks:
                return "Epic task not found"
            epic_task = self.created_tasks[epic_task_id]
            epic_task.add_sub_task(new_task.unic_task_id)
            self.created_tasks[new_task.unic_task_id] = new_task
            self.change_epic_task_duration(new_task.unic_task_id)
        elif task_type == "EPIC_TASK":
            new_task = EpicTask(name, description, self.unic_task_id)
        else:
            return "Unknown parameter"
        self.created_tasks[new_task.unic_task_id] = new_task
        self.unic_task_id += 1
        return new_task

    @staticmethod
    def update_task(obj, new_name, new_description, status=None, start_time=None, duration=0):
        if new_name and new_name != obj.name:
            obj.name = new_name
        if new_description and new_description != obj.description:
            obj.description = new_description
        if status and status != obj.status:
            obj.status = StatusType[status]
        if duration and duration != obj.duration:
            obj.duration = duration
        if start_time and start_time != obj.start_time:
            obj.start_time = start_time

    def update_any_task(self, task_id=None, name=None, description=None, status=None, sub_checked=False,
                        start_time=None, duration=0):
        if start_time is not None:
            find_intersections = self.check_intersections(start_time, duration)
            if find_intersections[0]:
                return f"Task intersections with: {', '.join(find_intersections[1])}"
        if task_id == None:
            return "Task id not found"
        if status:
            try:
                StatusType.__contains__(StatusType[status])
            except KeyError:
                return "Incorrect argument"
        if task_id in self.created_tasks:
            task_for_update = self.created_tasks[task_id]
            if task_for_update.task_type.value == TaskType.TASK.value:
                self.update_task(task_for_update, name, description, status, start_time, duration)  # обновление полностью
            elif task_for_update.task_type.value == TaskType.EPIC_TASK.value:
                if sub_checked:
                    self.update_task(task_for_update, name, description, status)  # обновление со статусом
                else:
                    self.update_task(task_for_update, name, description)  # обновление без статуса
            elif task_for_update.task_type.value == TaskType.SUB_TASK.value:
                self.update_task(task_for_update, name, description, status, start_time, duration)  # обновление полностью
                if status:
                    self.check_and_update_epic_status(task_id)
                if any([start_time, duration]):
                    self.change_epic_task_duration(task_id)
            self.created_tasks[task_id] = task_for_update
            return task_for_update
        else:
            return "Incorrect task id"

    def check_and_update_epic_status(self, sub_task_id=None, case_of_delete=False, deleted_task_id=None):
        if sub_task_id is None:
            return "Task id not found"
        elif sub_task_id not in self.created_tasks:
            return "Incorrect task id"
        sub_task = self.created_tasks[sub_task_id]  # обновленная в прошлом шаге подзадача
        epic_task = self.created_tasks[sub_task.epic_task_id]  # эпик подзадачи выше
        epic_sub_tasks = epic_task.sub_tasks_id  # список всех id подзадач эпика
        if case_of_delete:
            epic_sub_tasks.remove(deleted_task_id)
        if epic_sub_tasks:
            are_all_subtasks_new = all(list(map(lambda x: self.created_tasks[x].status.value == 1, epic_sub_tasks)))
            are_all_subtasks_done = all(list(map(lambda x: self.created_tasks[x].status.value == 3, epic_sub_tasks)))
            if are_all_subtasks_new:
                self.update_any_task(sub_task.epic_task_id, status="NEW", sub_checked=True)
            elif are_all_subtasks_done:
                self.update_any_task(sub_task.epic_task_id, status="DONE", sub_checked=True)
            else:
                self.update_any_task(sub_task.epic_task_id, status="IN_PROGRESS", sub_checked=True)
        else:
            self.update_any_task(sub_task.epic_task_id, status="NEW", sub_checked=True)

    def get_list_of_tasks(self):
        return list(self.created_tasks.values())

    def delete_all_tasks(self):
        self.created_tasks.clear()
        self.search_history.head, self.search_history.tail = None, None
        self.search_history.current_length = 0
        self.search_history.add_history = list()
        self.search_history.node_dict = dict()

    @check_entry_id
    def delete_task_by_id(self, task_id=None):
        task_for_delete = self.created_tasks[task_id]
        if task_for_delete.task_type.value == TaskType.EPIC_TASK.value:
            list_of_subtasks = task_for_delete.sub_tasks_id
            for task in list_of_subtasks:
                if self.search_history.current_length > 0:
                    self.search_history.delete(self.created_tasks[task])
                del self.created_tasks[task]
            if self.search_history.current_length > 0:
                self.search_history.delete(self.created_tasks[task_id])
            del self.created_tasks[task_id]
        elif task_for_delete.task_type.value == TaskType.TASK.value:
            if self.search_history.current_length > 0:
                self.search_history.delete(self.created_tasks[task_id])
            del self.created_tasks[task_id]
        else:
            self.check_and_update_epic_status(
                task_for_delete.unic_task_id, case_of_delete=True, deleted_task_id=task_id)
            if self.search_history.current_length > 0:
                self.search_history.delete(self.created_tasks[task_id])
            del self.created_tasks[task_id]

    @check_entry_id
    def get_task_by_id(self, task_id=None):
        if task_id in self.search_history.add_history:
            self.search_history.delete(self.created_tasks[task_id])
        self.search_history.add_to_end(self.created_tasks[task_id])
        return self.created_tasks[task_id]

    @check_entry_id
    def get_all_subtasks_of_epic(self, epic_task_id=None):
        if self.created_tasks[epic_task_id].task_type.name != TaskType.EPIC_TASK.name:
            return "Task type is not Epic"
        epic_task = self.created_tasks[epic_task_id]
        list_of_subtasks = list()
        for sub_task_id in epic_task.sub_tasks_id:
            list_of_subtasks.append(self.created_tasks[sub_task_id])
        return list_of_subtasks

    def get_history(self):
        return self.search_history.get_history()

    @check_entry_id
    def change_epic_task_duration(self, sub_task_id=None):
        sub_task = self.created_tasks[sub_task_id]
        epic_task = self.created_tasks[sub_task.epic_task_id]
        epic_task.duration += sub_task.duration
        if sub_task.start_time is not None:
            if epic_task.start_time is None:
                epic_task.start_time = date(2099, 12, 12)
            if (epic_task.start_time is None) or (sub_task.start_time < epic_task.start_time):
                epic_task.start_time = sub_task.start_time
                self.created_tasks[sub_task.epic_task_id] = epic_task

    @check_entry_id
    def get_end_time(self, task_id=None):
        task = self.created_tasks[task_id]
        end_time = task.start_time + timedelta(days=task.duration)
        return end_time

    def get_prioritized_tasks(self):
        tasks_without_time = list(filter(lambda x: x.start_time is None, self.created_tasks.values()))
        tasks_with_time = list(filter(lambda x: x.start_time is not None, self.created_tasks.values()))
        sorted_tasks = sorted(tasks_with_time, key=lambda x: x.start_time)
        return sorted_tasks, tasks_without_time

    def check_intersections(self, start_time, duration):
        intersection, intersections = False, []
        sorted_tasks = self.get_prioritized_tasks()[0]
        if sorted_tasks:
            end_time = start_time + timedelta(days=duration)
            for task in sorted_tasks:
                case_1 = task.start_time < start_time < self.get_end_time(task.unic_task_id)
                case_2 = task.start_time < end_time < self.get_end_time(task.unic_task_id)
                case_3 = start_time <= task.start_time and self.get_end_time(task.unic_task_id) <= end_time
                if any([case_1, case_2, case_3]):
                    intersection = True
                    intersections.append(str(task.unic_task_id))
        return intersection, intersections
