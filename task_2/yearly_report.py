import os
from datetime import date as d
import locale


class YearlyReport:
    def __init__(self, reports_dir_name="reports"):
        self.report_info = dict()
        self.reports_dir_name = reports_dir_name
        self.yearly_report_mark = 'y'

    def read_report_file(self):
        reports_dir_path = os.getcwd() + "\\" + self.reports_dir_name
        for file_name in os.listdir(reports_dir_path):
            if file_name[0] == self.yearly_report_mark:
                report_year = file_name.split('.')[1]
                self.report_info[report_year] = {}
                with open(self.reports_dir_name + "\\" + file_name) as report_file:
                    file_data = report_file.read()
                    for line in file_data.splitlines()[1:]:
                        month, amount, is_expense = line.split(',')
                        self.report_info[report_year][month] = self.report_info[report_year].get(month, {})
                        if is_expense == "true":
                            type_of_operation = "expense"
                        else:
                            type_of_operation = "profit"
                        self.report_info[report_year][month][type_of_operation] = self.report_info[report_year][month].get(
                            type_of_operation, 0) + int(amount)
        return self.report_info

    def year_stat_info(self):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        year_report_info = self.read_report_file()
        all_profits = list()
        all_expenses = list()
        for year in year_report_info:
            print(f"Отчет за год {year}")
            for month in year_report_info[year]:
                date = d(2023, int(month), 1)
                print(f'{date.strftime("%B")}:')
                all_profits.append(year_report_info[year][month]["profit"])
                all_expenses.append(year_report_info[year][month]["expense"])
                print(f'Прибыль - {year_report_info[year][month]["profit"] - year_report_info[year][month]["expense"]:,}')
                print()
            print(f"Средний расход по году {sum(all_profits)/len(all_profits):,}")
            print(f"Средний доход по году {sum(all_expenses)/len(all_expenses):,}")


# a = YearlyReport()
# print(a.read_report_file())