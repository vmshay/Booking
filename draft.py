import calendar
import datetime

today = datetime.date.today()
month = today.month
days_in_month = calendar.monthrange(today.year, month)[1]


print(f"Дата сегодня {today}")
print(f"Месяц {month}")
print(f"Дней в месяце {days_in_month}")

