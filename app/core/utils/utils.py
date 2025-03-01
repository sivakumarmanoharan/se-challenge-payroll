from datetime import date, timedelta

from app.schemas.csv_upload_schemas import PayPeriod


def get_pay_period(date_worked: date):
    if date_worked.day <= 15:
        start = date(date_worked.year, date_worked.month, 1)
        end = date(date_worked.year, date_worked.month, 15)
    else:
        start = date(date_worked.year, date_worked.month, 16)
        # Determine last day of month:
        if date_worked.month == 12:
            next_month = date(date_worked.year + 1, 1, 1)
        else:
            next_month = date(date_worked.year, date_worked.month + 1, 1)
        end = next_month - timedelta(days=1)
    return PayPeriod(startDate=start, endDate=end)
