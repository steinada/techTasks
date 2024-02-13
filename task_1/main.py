from steps_counter import StepsTracker


class Main:
    def menu_printer(self):
        steps_tracker = StepsTracker()
        print("Добро пожаловать в трекер шагов и калорий")
        self.print_menu()
        while True:
            user_input = input()
            if user_input == '1':
                print("Введите номер месяца")
                user_month = self.validation_month()
                print("Введите число дня")
                user_day = self.validation_day()
                print("Введите количество шагов")
                user_steps = self.validation_steps()
                steps_tracker.add_steps(user_day, user_month, user_steps)
                self.print_menu()
            elif user_input == '2':
                print("Введите цель по количеству шагов в день")
                steps_plan = self.validation_steps()
                steps_tracker.change_steps_plan(steps_plan)
                self.print_menu()
            elif user_input == '3':
                print("Введите месяц, за который хотите получить статистику")
                month = self.validation_month()
                steps_tracker.print_statistics(month)
                self.print_menu()
            elif user_input == '4':
                print("До свидания!")
                break
            else:
                print("Выберите значение из списка выше")

    def validation_month(self):
        month = input()
        if month.isnumeric():
            if int(month) > 12 or int(month) < 1:
                print("Введен некорретный месяц")
                return self.validation_month()
            else:
                return month
        else:
            print("Введите месяц числовыми значениями")
            return self.validation_month()

    def validation_day(self):
        day = input()
        if day.isnumeric():
            if int(day) > 30 or int(day) < 1:
                print("Введен некорретный день")
                return self.validation_day()
            else:
                return day
        else:
            print("Введите день числовыми значениями")
            return self.validation_day()

    def validation_steps(self):
        steps = input()
        if steps.isnumeric():
            if int(steps) > 0:
                return steps
            else:
                print("Введите число, большее 0 числовыми значениями")
                return self.validation_steps()
        else:
            print("Введите шаги числовыми значениями")
            return self.validation_steps()

    def print_menu(self):
        print(f"Выберите действие:")
        print(f"1 - ввести количество шагов за определённый день")
        print(f"2 - изменить цель по количеству шагов в день")
        print(f"3 - напечатать статистику за определённый месяц")
        print(f"4 - выйти из приложения")


app = Main()
app.menu_printer()
