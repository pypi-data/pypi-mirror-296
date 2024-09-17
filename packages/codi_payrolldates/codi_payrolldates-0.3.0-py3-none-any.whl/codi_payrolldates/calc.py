from datetime import datetime, timedelta
from typing import Tuple


def calculate_pay_period(date):
    initial_start_date = datetime(2024, 1, 7)
    days_since_start = (date - initial_start_date).days
    days_into_cycle = days_since_start % 14
    start_date = date - timedelta(days=days_into_cycle)
    end_date = start_date + timedelta(days=13)
    return start_date, end_date


def print_pay_period(date):
    start_date, end_date = calculate_pay_period(date)
    print(f'Pay Period for {date.strftime("%Y-%m-%d")}:')
    print('Start:', start_date.strftime('%Y-%m-%d'))
    print('End:', end_date.strftime('%Y-%m-%d'))


def get_pay_period(date) -> Tuple[datetime, datetime]:
    start_date, end_date = calculate_pay_period(date)
    return start_date, end_date


def is_date_in_first_week(date):
    start_date, _ = calculate_pay_period(date)
    return date < start_date + timedelta(days=7)
