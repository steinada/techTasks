import os
from datetime import date as d
import locale


class MonthlyReport:
    def __init__(self, reports_dir_name="reports"):
        self.report_info = dict()
        self.reports_dir_name = reports_dir_name
        self.monthly_report_mark = 'm'

    def read_report_file(self):
        reports_dir_path = os.getcwd() + "\\" + self.reports_dir_name
        for file_name in os.listdir(reports_dir_path):
            if file_name[0] == self.monthly_report_mark:
                report_period = file_name.split('.')[1]
                report_year, report_month = report_period[:4], report_period[4:]
                self.report_info[report_year, report_month] = dict()
                with open(self.reports_dir_name + "\\"+file_name) as report_file:
                    file_data = report_file.read()
                    for line in file_data.splitlines()[1:]:
                        item_name, is_expense, quantity, unit_price = line.split(',')
                        if is_expense == "TRUE":
                            type_of_operation = "expense"
                        else:
                            type_of_operation = "profit"
                        self.report_info[report_year, report_month][type_of_operation] = self.report_info[report_year,
                        report_month].get(type_of_operation, {})
                        self.report_info[report_year, report_month][type_of_operation][item_name] = self.report_info[
                        report_year, report_month][type_of_operation].get(item_name, 0) + int(quantity) * int(unit_price)
        return self.report_info

    def months_stat_info(self):
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        most_profit_item, most_expense_item = self.get_most_profit_or_expense_item()
        for year in most_profit_item:
            print(year)
            for month in most_profit_item[year]:
                date = d(int(year), int(month), 1)
                print(date.strftime("%B"))
                print(f"Самый прибыльный товар: {most_profit_item[year][month][0]} на сумму {most_profit_item[year][month][1]:,}")
                print(f"Самый убыточный товар: {most_expense_item[year][month][0]} на сумму {most_expense_item[year][month][1]:,}")
                print()

    def sum_per_month_info(self):
        sum_per_month = dict()
        for date, info in self.read_report_file().items():
            year, month = date
            sum_per_month[year] = sum_per_month.get(year, {})
            sum_per_month[year][month] = sum_per_month[year].get(month, {})
            for op_type, op in info.items():
                sum_per_month[year][month][op_type] = sum_per_month[year][month].get(op_type, 0) + sum(op.values())
        return sum_per_month

    def get_most_profit_or_expense_item(self):
        most_profit_item = dict()
        most_expense_item = dict()
        for date, operations in self.read_report_file().items():
            year, month = date
            for op_type, operation in operations.items():
                max_operation = max(operation.items(), key=lambda x: x[1])
                if op_type == "expense":
                    if year in most_expense_item:
                        if month in most_expense_item[year]:
                            most_expense_op = most_expense_item[year][month][1]
                        else:
                            most_expense_op = 0
                    else:
                        most_expense_op = 0
                    if most_expense_op < max_operation[1]:
                        most_expense_item[year] = most_expense_item.get(year, {})
                        most_expense_item[year][month] = (max_operation[0], max_operation[1])
                else:
                    if year in most_profit_item:
                        if month in most_profit_item[year]:
                            most_profit_op = most_profit_item[year][month][1]
                        else:
                            most_profit_op = 0
                    else:
                        most_profit_op = 0
                    if most_profit_op < max_operation[1]:
                        most_profit_item[year] = most_profit_item.get(year, {})
                        most_profit_item[year][month] = (max_operation[0], max_operation[1])
        return most_profit_item, most_expense_item


# a = MonthlyReport()
# a.months_stat_info()