from datetime import date
from converter import Converter


class StepsTracker:
    def __init__(self):
        self.steps_info = dict()
        self.plan_steps_per_day = 10_000

    def add_steps(self, day, month, steps):
        self.steps_info[date(2023, int(month), int(day))] = int(steps)
        print("Шаги записаны")
        return self.steps_info

    def change_steps_plan(self, plan_steps):
        self.plan_steps_per_day = int(plan_steps)
        print("Цель изменена")

    def print_statistics(self, month):
        month_info = MonthData(month, self.steps_info, self.plan_steps_per_day)
        converter = Converter()
        print("Количество шагов в указанном месяце по дням:")
        month_info.print_steps_and_days_per_month()
        print(f"Всего пройдено шагов: {month_info.sum_steps_from_month()}")
        print(f"Максимальное количество шагов в день: {month_info.max_steps()}")
        print(f"Среднее количество шагов в день: {month_info.sum_steps_from_month()/len(month_info.month_steps)}")
        print(f"Пройдено километров: {converter.convert_to_km(month_info.sum_steps_from_month())}")
        print(f"Сожжено килокалорий: {converter.convert_steps_to_kilokalories(month_info.sum_steps_from_month())}")
        print(f"Лучшая серия шагов: {month_info.best_series()}")


class MonthData:
    def __init__(self, month, steps_info, plan_steps_per_day):
        self.steps_info = steps_info
        self.month_steps = list()
        self.month = month
        self.plan_steps_per_day = plan_steps_per_day

    def print_steps_and_days_per_month(self):
        if int(self.month) == 2:
            max_day_month = 29
        else:
            max_day_month = 31
        for day in range(1, max_day_month):
            self.month_steps.append(
                self.steps_info.get(date(2023, int(self.month), day), 0)
            )
        for day, steps in enumerate(self.month_steps):
            if int(steps) > 0:
                print(f"{day+1} день: {steps} шагов")

    def sum_steps_from_month(self):
        return sum(self.month_steps)

    def max_steps(self):
        return max(self.month_steps)

    def best_series(self):
        goal_steps_per_day = self.plan_steps_per_day
        count_goals, group = dict(), 1
        for step in self.month_steps:
            if step >= goal_steps_per_day:
                count_goals[group] = count_goals.get(group, 0) + 1
            else:
                group += 1
        if count_goals:
            return max(count_goals.values())
        else:
            return 0
