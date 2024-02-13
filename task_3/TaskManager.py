from abc import ABC, abstractmethod


class TaskManager(ABC):
    @abstractmethod
    def create_any_task(self, name, description, task_type, epic_task_id, start_time, duration):
        pass

    @staticmethod
    @abstractmethod
    def update_task(obj, new_name, new_description, status, start_time, duration):
        pass

    @abstractmethod
    def update_any_task(self, task_id, new_name, new_description, status, sub_checked, start_time, duration):
        pass

    @abstractmethod
    def get_list_of_tasks(self):
        pass

    @abstractmethod
    def delete_all_tasks(self):
        pass

    @abstractmethod
    def delete_task_by_id(self, task_id):
        pass

    @abstractmethod
    def get_task_by_id(self, task_id):
        pass

    @abstractmethod
    def get_all_subtasks_of_epic(self, epic_task_id):
        pass
