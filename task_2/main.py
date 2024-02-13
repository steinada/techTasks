from monthly_report import MonthlyReport
from yearly_report import YearlyReport
from comparison_of_reports import ComparsionOfReports
from datetime import date as d
import locale


class Menu:
    def __init__(self):
        self.yearly_has_been_read = False
        self.monthly_has_been_read = False

    def console_menu(self):
        print("Начало работы приложения для сверки отчетов")
        while True:
            self.print_menu_todo()
            user_input = input()
            if user_input == '1':
                self.monthly_has_been_read = True
                reports_month = MonthlyReport()
                reports_month.read_report_file()
                print("Отчет успешно считан")
            elif user_input == '2':
                self.yearly_has_been_read = True
                reports_year = YearlyReport()
                reports_year.read_report_file()
                print("Отчет успешно считан")
            elif user_input == '3':
                if self.reading_of_reports_check():
                    reports_comparsion = ComparsionOfReports(reports_month, reports_year)
                    self.difference_in_reports(reports_comparsion)
                else:
                    print("Введите 1 или 2 в зависимости от того, какой отчет вам нужно считать")
            elif user_input == '4':
                reports_month.months_stat_info()
            elif user_input == '5':
                reports_year.year_stat_info()
            elif user_input == '1488':
                print("Программа завершена")
                break
            else:
                print("Пожалуйста, введите пункт меню из списка выше")

    @staticmethod
    def print_menu_todo():
        print()
        print("Выберите действие:")
        print("1: Считать все месячные отчёты")
        print("2: Считать годовой отчёт")
        print("3: Сверить отчёты")
        print("4: Вывести информацию обо всех месячных отчётах")
        print("5: Вывести информацию о годовом отчёте")

    def reading_of_reports_check(self):
        if self.monthly_has_been_read:
            if self.yearly_has_been_read:
                return "OK"
            else:
                print("Вначале считайте годовой отчет")
        else:
            print("Вначале считайте месячный отчет")

    @staticmethod
    def difference_in_reports(reports_comparsion):
        is_difference, difference_months = reports_comparsion.make_comparsion_of_reports()
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        if is_difference:
            print("Есть расхождения в данных по месяцам: ", end='')
            months = list(map(lambda x: x.strftime("%B"), map(lambda y: d(2023, int(y), 1), difference_months)))
            print(', '.join(months))
        else:
            print("Сверка прошла без расхождений!")


program = Menu()
program.console_menu()