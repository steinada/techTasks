from task_3.InMemoryTaskManager import InMemoryTaskManager
from datetime import date


class Main(InMemoryTaskManager):
    @staticmethod
    def main():
        manager = InMemoryTaskManager()
        task1 = (manager.create_any_task
                 ("Погладить вещи", "Быстро", task_type="TASK", start_time=date(2023, 1, 1), duration=40))
        task2 = (manager.create_any_task
                 ("Выгулять кошку", task_type="TASK", start_time=date(2023, 1, 5), duration=12))
        # task3 = (manager.create_any_task
        #          ("Выгулять кошку", task_type="TASK", start_time=date(2023, 1, 10)))
        #
        # tasks = [task1, task2, task3]
        # for task in tasks:
        #     print(task.unic_task_id, task.task_type, task.start_time, task.duration)
        #
        # manager.check_intersections()
        print(vars(task1, task2))

main = Main
main.main()
