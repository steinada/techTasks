import pytest
from datetime import date
from task_3.model.Task import Task
from task_3.model.SubTask import SubTask
from task_3.model.EpicTask import EpicTask
from task_3.FileBackedTasksManager import FileBackedTasksManager


class TestCaseTaskManager:
    @staticmethod
    @pytest.fixture()
    def create_tasks():
        task = Task("Task 1", "Description 1", 0)
        epic_task = EpicTask("Task 1", "Description 1", 1)
        epic_task.sub_tasks_id = [2, 3, 4]
        sub_task_1 = SubTask("Subtask 1", "Description 1", 1, 2)
        sub_task_2 = SubTask("Subtask 1", "Description 1", 1, 3)
        sub_task_3 = SubTask("Subtask 1", "Description 1", 1, 4)
        created_tasks = {0: task, 1: epic_task, 2: sub_task_1, 3: sub_task_2, 4: sub_task_3}
        return created_tasks

    @staticmethod
    @pytest.fixture()
    def create_tasks_dated():
        task = Task("N1", "D1", 0, start_time=date(1998, 5, 5), duration=3)
        epic_task = EpicTask("N2", "D2", 1, start_time=date(2025, 7, 7), duration=7)
        epic_task.sub_tasks_id = [2, 3, 4]
        sub_task_1 = SubTask("N3", "D3", 1, 2, start_time=date(1998, 8, 8), duration=11)
        sub_task_2 = SubTask("N4", "D4", 1, 3, start_time=date(1995, 9, 9), duration=5)
        sub_task_3 = SubTask("N5", "D5", 1, 4, start_time=date(1993, 3, 3), duration=21)
        created_tasks = {0: task, 1: epic_task, 2: sub_task_1, 3: sub_task_2, 4: sub_task_3}
        return created_tasks

    @staticmethod
    @pytest.fixture()
    def task(create_tasks):
        return create_tasks[0]

    @staticmethod
    @pytest.fixture()
    def task_date(create_tasks_dated):
        return create_tasks_dated[0]

    @staticmethod
    @pytest.fixture()
    def epic_task(create_tasks):
        return create_tasks[1]

    @staticmethod
    @pytest.fixture()
    def epic_task_date(create_tasks_dated):
        return create_tasks_dated[1]

    @staticmethod
    @pytest.fixture()
    def sub_tasks(create_tasks):
        return create_tasks[2], create_tasks[3], create_tasks[4]

    @staticmethod
    @pytest.fixture()
    def sub_tasks_date(create_tasks_dated):
        return create_tasks_dated[2], create_tasks_dated[3], create_tasks_dated[4]

    @staticmethod
    @pytest.fixture()
    def manager(create_tasks):
        manager_create = FileBackedTasksManager()
        manager_create.created_tasks = create_tasks
        return manager_create

    @staticmethod
    @pytest.fixture()
    def manager_date(create_tasks_dated):
        manager_date = FileBackedTasksManager()
        manager_date.created_tasks = create_tasks_dated
        return manager_date

    @staticmethod
    @pytest.fixture()
    def create_sub_and_epic():
        manager = FileBackedTasksManager()
        test_name = "Test"
        test_description = "Test_Description"
        epic_task_task = manager.create_any_task(test_name, test_description, "EPIC_TASK")
        sub_task_1 = manager.create_any_task(test_name, test_description, "SUB_TASK", epic_task_task.unic_task_id)
        sub_task_2 = manager.create_any_task(test_name, test_description, "SUB_TASK", epic_task_task.unic_task_id)
        sub_task_3 = manager.create_any_task(test_name, test_description, "SUB_TASK", epic_task_task.unic_task_id)
        return epic_task_task, sub_task_1, sub_task_2, sub_task_3, manager, test_name, test_description

    def test_status_epic_all_subtasks_new(self, epic_task, sub_tasks, create_tasks, manager):
        for sub_task in sub_tasks:
            manager.update_any_task(sub_task.unic_task_id, status="NEW")
        assert epic_task.status.name == "NEW"

    def test_status_epic_all_subtasks_done(self, epic_task, sub_tasks, create_tasks, manager):
        for sub_task in sub_tasks:
            manager.update_any_task(sub_task.unic_task_id, status="DONE")
        assert epic_task.status.name == "DONE"

    def test_status_epic_all_subtasks_in_progress(self, epic_task, sub_tasks, create_tasks, manager):
        for sub_task in sub_tasks:
            manager.update_any_task(sub_task.unic_task_id, status="IN_PROGRESS")
        assert epic_task.status.name == "IN_PROGRESS"

    def test_status_epic_subtasks_are_new_and_done(self, epic_task, sub_tasks, create_tasks, manager):
        for sub_task in sub_tasks:
            manager.update_any_task(sub_task.unic_task_id, status="DONE")
        manager.update_any_task(sub_tasks[1].unic_task_id, status="NEW")
        assert epic_task.status.name == "IN_PROGRESS"

    def test_status_epic_update_without_subtask(self, epic_task, sub_tasks, create_tasks, manager):
        for sub_task in sub_tasks:
            manager.update_any_task(sub_task.unic_task_id, status="NEW")
        manager.update_any_task(epic_task.unic_task_id, status="DONE")
        assert epic_task.status.name == "NEW"

    def test_status_task_new(self, task, manager):
        manager.update_any_task(task.unic_task_id, status="NEW")
        assert task.status.name == "NEW"

    def test_status_task_done(self, task, manager):
        manager.update_any_task(task.unic_task_id, status="DONE")
        assert task.status.name == "DONE"

    def test_status_task_in_progress(self, task, manager):
        manager.update_any_task(task.unic_task_id, status="IN_PROGRESS")
        assert task.status.name == "IN_PROGRESS"

    def test_update_name_and_description(self, task, manager):
        manager.update_any_task(task.unic_task_id, 'test', 'test')
        assert task.name == "test"
        assert task.description == "test"

    def test_update_with_empty_filled(self, task, manager):
        manager.update_any_task(task.unic_task_id)
        assert task == task

    def test_update_with_incorrect_id(self, manager, create_tasks):
        id = max(create_tasks) + 1
        updated_task = manager.update_any_task(id, status="IN_PROGRESS")
        assert updated_task == "Incorrect task id"

    def test_update_with_incorrect_data(self, task, manager):
        task_updated = manager.update_any_task(task.unic_task_id, status="TEST")
        assert task_updated, "Unknown parameter"

    def test_change_id_after_updating(self, task, manager):
        old_id = task.unic_task_id
        manager.update_any_task(old_id, name="123456789")
        assert manager.created_tasks[old_id].name == "123456789"

    def test_create_correct_task(self, manager):
        test_name = "Test"
        test_description = "Test_Description"
        task_task = manager.create_any_task(test_name, test_description, "TASK")
        assert task_task.name == test_name
        assert task_task.description == test_description
        assert task_task.task_type.name == "TASK"
        assert task_task.status.name == "NEW"
        assert manager.created_tasks[0] == task_task

    def test_create_correct_epic(self, manager):
        test_name = "Test"
        test_description = "Test_Description"
        epic_task_task = manager.create_any_task(test_name, test_description, "EPIC_TASK")
        assert epic_task_task.name == test_name
        assert epic_task_task.description == test_description
        assert epic_task_task.task_type.name == "EPIC_TASK"
        assert epic_task_task.status.name == "NEW"
        assert manager.created_tasks[epic_task_task.unic_task_id] == epic_task_task

    def test_create_correct_name_and_description(self, create_sub_and_epic):
        epic_task_task, sub_task_1, sub_task_2, sub_task_3, manager, test_name, test_description = create_sub_and_epic
        assert sub_task_1.name == test_name
        assert sub_task_2.description == test_description

    def test_create_correct_ids(self, create_sub_and_epic):
        epic_task_task, sub_task_1, sub_task_2, sub_task_3, manager, test_name, test_description = create_sub_and_epic
        assert manager.created_tasks[epic_task_task.unic_task_id] == epic_task_task
        assert manager.created_tasks[sub_task_1.unic_task_id] == sub_task_1
        assert manager.created_tasks[sub_task_2.unic_task_id] == sub_task_2
        assert manager.created_tasks[sub_task_3.unic_task_id] == sub_task_3

    def test_create_correct_dependencies(self, create_sub_and_epic):
        epic_task_task, sub_task_1, sub_task_2, sub_task_3, manager, test_name, test_description = create_sub_and_epic
        assert sub_task_2.epic_task_id == epic_task_task.unic_task_id
        assert epic_task_task.sub_tasks_id == [sub_task_1.unic_task_id, sub_task_2.unic_task_id, sub_task_3.unic_task_id]

    def test_create_task_incorrect_type(self, manager):
        test_task = manager.create_any_task('test', 'desc', "TEST")
        assert test_task == "Unknown parameter"

    def test_create_empty_task(self, manager):
        result = manager.create_any_task()
        assert result == "Unknown parameter"

    def test_update_empty_task(self, manager):
        result = manager.update_any_task()
        assert result == "Task id not found"

    def test_empty_check_and_update_epic_status(self, manager):
        result = manager.check_and_update_epic_status()
        assert result == "Task id not found"

    def test_incorrect_id_check_and_update_epic_status(self, manager):
        task_id = max(manager.created_tasks) + 1
        result = manager.check_and_update_epic_status(task_id)
        assert result == "Incorrect task id"

    def test_empty_get_list_of_tasks(self, manager):
        manager.created_tasks = {}
        result = manager.get_list_of_tasks()
        assert result == []

    def test_get_list_of_tasks(self, manager):
        result = manager.get_list_of_tasks()
        assert result == list(manager.created_tasks.values())

    def test_not_empty_delete_all_tasks(self, manager):
        manager.delete_all_tasks()
        assert manager.created_tasks == {}

    def test_empty_delete_all_tasks(self, manager):
        manager.created_tasks = {}
        manager.delete_all_tasks()
        assert manager.created_tasks == {}

    def test_delete_task_by_correct_id(self, manager, task):
        length_before = len(manager.created_tasks)
        id_to_delete = task.unic_task_id
        manager.delete_task_by_id(id_to_delete)
        length_after = len(manager.created_tasks)
        assert id_to_delete not in manager.created_tasks
        assert length_before == length_after + 1

    def test_delete_subtask_by_correct_id(self, manager, sub_tasks):
        length_before = len(manager.created_tasks)
        id_to_delete = sub_tasks[2].unic_task_id
        manager.delete_task_by_id(id_to_delete)
        length_after = len(manager.created_tasks)
        assert id_to_delete not in manager.created_tasks
        assert length_before == length_after + 1

    def test_delete_epic_by_correct_id(self, manager, epic_task):
        length_before = len(manager.created_tasks)
        id_to_delete = epic_task.unic_task_id
        subtasks_count = len(epic_task.sub_tasks_id)
        manager.delete_task_by_id(id_to_delete)
        length_after = len(manager.created_tasks)
        assert id_to_delete not in manager.created_tasks
        assert length_before == length_after + subtasks_count + 1

    def test_delete_task_by_incorrect_id(self, manager):
        inc_id = max(manager.created_tasks) + 1
        result = manager.delete_task_by_id(inc_id)
        assert result == "No task by id"

    def test_delete_task_by_empty_id(self, manager):
        result = manager.delete_task_by_id()
        assert result == "Empty id"

    def test_get_task_by_correct_id(self, manager, epic_task):
        assert manager.get_task_by_id(epic_task.unic_task_id) == epic_task
        assert manager.search_history.tail.data.unic_task_id == epic_task.unic_task_id

    def test_get_task_by_incorrect_id(self, manager):
        inc_id = max(manager.created_tasks) + 1
        result = manager.get_task_by_id(inc_id)
        assert result == "No task by id"
        if manager.search_history.tail:
            assert manager.search_history.tail.data.unic_task_id != inc_id

    def test_correct_get_subtasks(self, manager, epic_task, sub_tasks):
        subtasks_list_test = manager.get_all_subtasks_of_epic(epic_task.unic_task_id)
        assert list(sub_tasks) == subtasks_list_test

    def test_get_subtasks_of_non_epic(self, manager, task):
        result = manager.get_all_subtasks_of_epic(task.unic_task_id)
        assert result == "Task type is not Epic"

    def test_get_subtasks_incorrect_id(self, manager):
        id = max(manager.created_tasks) + 1
        result = manager.get_all_subtasks_of_epic(id)
        assert result == "No task by id"

    def test_get_subtasks_empty_id(self, manager):
        result = manager.get_all_subtasks_of_epic()
        assert result == "Empty id"

    def test_get_history_with_several_elements(self, manager, task, sub_tasks, epic_task, create_tasks):
        calls = list()
        for sub_task in sub_tasks:
            manager.get_task_by_id(sub_task.unic_task_id)
            calls.append(sub_task)
        manager.get_task_by_id(epic_task.unic_task_id)
        calls.append(epic_task)
        manager.get_task_by_id(task.unic_task_id)
        calls.append(task)
        tasks_history = list(map(lambda x: x.data, manager.get_history()))
        assert tasks_history == calls

    def test_get_history_with_one_element(self, manager, task):
        calls = list()
        manager.get_task_by_id(task.unic_task_id)
        calls.append(task)
        tasks_history = list(map(lambda x: x.data, manager.get_history()))
        assert tasks_history == calls

    def test_get_history_duplicates(self, manager, sub_tasks):
        for _ in range(3):
            for sub_task in sub_tasks:
                manager.get_task_by_id(sub_task.unic_task_id)
        tasks_history = list(map(lambda x: x.data, manager.get_history()))
        assert tasks_history == list(sub_tasks)

    def test_get_empty_history(self, manager):
        assert manager.get_history() == list()

    def test_get_history_after_task_delete(self, manager, task, epic_task):
        calls = list()
        manager.get_task_by_id(task.unic_task_id)
        calls.append(task)
        manager.get_task_by_id(epic_task.unic_task_id)
        calls.append(epic_task)
        manager.delete_task_by_id(task.unic_task_id)
        calls.remove(task)
        tasks_history = list(map(lambda x: x.data, manager.get_history()))
        assert tasks_history == calls

    def test_create_tasks_with_start_dates(self, manager):
        manager.created_tasks = {}
        task_task_1 = manager.create_any_task(name="NAME1", task_type="TASK", start_time=date(2012, 9, 9))
        epic_task_1 = manager.create_any_task(name="NAME2", task_type="EPIC_TASK", start_time=date(1999, 9, 9))
        sub_task_1 = manager.create_any_task(name="NAME3", task_type="SUB_TASK", start_time=date(2011, 9, 9),
                                             epic_task_id=epic_task_1.unic_task_id)
        sub_task_2 = manager.create_any_task(name="NAME4", task_type="SUB_TASK", start_time=date(2011, 1, 9),
                                             epic_task_id=epic_task_1.unic_task_id)
        assert manager.created_tasks[task_task_1.unic_task_id].start_time.isoformat() == date(2012, 9, 9).isoformat()
        assert manager.created_tasks[epic_task_1.unic_task_id].start_time.isoformat() == date(2011, 1, 9).isoformat()
        assert manager.created_tasks[sub_task_1.unic_task_id].start_time.isoformat() == date(2011, 9, 9).isoformat()
        assert manager.created_tasks[sub_task_2.unic_task_id].start_time.isoformat() == date(2011, 1, 9).isoformat()

    def test_create_tasks_with_duration(self, manager):
        task_task_1 = manager.create_any_task(name="NAME1", task_type="TASK", duration=10)
        epic_task_1 = manager.create_any_task(name="NAME2", task_type="EPIC_TASK", duration=20)
        sub_task_1 = manager.create_any_task(name="NAME3", task_type="SUB_TASK", duration=30,
                                             epic_task_id=epic_task_1.unic_task_id)
        sub_task_2 = manager.create_any_task(name="NAME4", task_type="SUB_TASK", duration=40,
                                             epic_task_id=epic_task_1.unic_task_id)
        assert manager.created_tasks[task_task_1.unic_task_id].duration == 10
        assert manager.created_tasks[epic_task_1.unic_task_id].duration == 70
        assert manager.created_tasks[sub_task_1.unic_task_id].duration == 30
        assert manager.created_tasks[sub_task_2.unic_task_id].duration == 40

    def test_epic_with_start_time_and_duration(self, manager):
        epic_task_1 = (manager.create_any_task
                       (name="NAME2", task_type="EPIC_TASK", duration=9999, start_time=date(2007, 1, 1)))
        sub_task_1 = manager.create_any_task(name="NAME3", task_type="SUB_TASK", duration=11,
                                             epic_task_id=epic_task_1.unic_task_id, start_time=date(2005, 1, 1))
        sub_task_2 = manager.create_any_task(name="NAME4", task_type="SUB_TASK", duration=55,
                                             epic_task_id=epic_task_1.unic_task_id, start_time=date(2008, 1, 1))
        assert manager.created_tasks[epic_task_1.unic_task_id].duration == 66
        assert manager.created_tasks[sub_task_1.unic_task_id].duration == 11
        assert manager.created_tasks[sub_task_2.unic_task_id].duration == 55
        assert (manager.created_tasks[epic_task_1.unic_task_id].start_time.isoformat()
                == date(2005, 1, 1).isoformat())
        assert (manager.created_tasks[sub_task_1.unic_task_id].start_time.isoformat()
                == date(2005, 1, 1).isoformat())
        assert (manager.created_tasks[sub_task_2.unic_task_id].start_time.isoformat()
                == date(2008, 1, 1).isoformat())

    def test_update_start_date(self, manager_date, task_date, epic_task_date, sub_tasks_date, create_tasks_dated):
        manager_date.update_any_task(task_date.unic_task_id, start_time=date(2011, 11, 11), duration=11)
        manager_date.update_any_task(epic_task_date.unic_task_id, start_time=date(2010, 11, 11), duration=11)
        manager_date.update_any_task(sub_tasks_date[0].unic_task_id, start_time=date(2009, 11, 11), duration=11)
        manager_date.update_any_task(sub_tasks_date[1].unic_task_id, start_time=date(2008, 11, 11), duration=11)
        assert task_date.start_time.isoformat() == date(2011, 11, 11).isoformat()
        assert task_date.duration == 11
        assert epic_task_date.start_time.isoformat() == date(2008, 11, 11).isoformat()
        assert epic_task_date.duration == 29
        assert sub_tasks_date[1].start_time.isoformat() == date(2008, 11, 11).isoformat()
        assert sub_tasks_date[1].duration == 11

    def test_intersection_tasks(self, manager_date):
        manager_date.created_tasks = {}
        task_1 = manager_date.create_any_task(name="N", task_type="TASK", start_time=date(2023, 1, 1), duration=10)
        task_2 = manager_date.create_any_task(name="N", task_type="TASK", start_time=date(2023, 1, 1), duration=10)
        task_3 = manager_date.create_any_task(name="N", task_type="TASK", start_time=date(2023, 1, 2), duration=10)
        task_4 = manager_date.create_any_task(name="N", task_type="TASK", start_time=date(2022, 12, 31), duration=10)
        assert task_2 == task_3 == task_4 == f'Task intersections with: {task_1.unic_task_id}'
