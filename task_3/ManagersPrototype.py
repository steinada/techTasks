from task_3.FileBackedTasksManager import FileBackedTasksManager


class ManagersPrototype:
    default_manager = FileBackedTasksManager()

    @classmethod
    def get_manager(cls):
        return cls.default_manager
