from monthly_report import MonthlyReport
from yearly_report import YearlyReport


class ComparsionOfReports:
    def __init__(self, monthly_report_obj=MonthlyReport(), yearly_report_obj=YearlyReport()):
        self.monthly_report_obj = monthly_report_obj
        self.yearly_report_obj = yearly_report_obj

    def make_comparsion_of_reports(self):
        summary_months_info = self.monthly_report_obj.sum_per_month_info()
        year_info = self.yearly_report_obj.read_report_file()
        is_difference = False
        difference_months = list()
        for year, value in summary_months_info.items():
            for month, info in value.items():
                if year not in year_info:
                    print(f"Нет данных для сверки по дате {year}.{month}")
                elif month not in year_info[year]:
                    print(f"Нет данных для сверки по дате {year}.{month}")
                else:
                    if summary_months_info[year][month]['expense'] != year_info[year][month]['expense']:
                        is_difference = True
                        difference_months.append(month)
        return is_difference, difference_months


