import os
import pytest
from datetime import datetime
from payrolldates.calc import *


def test_known(capsys):
    date = datetime(2024, 5, 2)
    print_pay_period(date)
    captured = capsys.readouterr()
    assert captured.out == f"Pay Period for {date.strftime('%Y-%m-%d')}:\nStart: 2024-04-28\nEnd: 2024-05-11\n"


def test_known2(capsys):
    date = datetime(2024, 1, 12)
    print_pay_period(date)
    captured = capsys.readouterr()
    assert captured.out == f"Pay Period for {date.strftime('%Y-%m-%d')}:\nStart: 2024-01-07\nEnd: 2024-01-20\n"


def test_get_pay_period():
    date = datetime(2024, 5, 2)
    start_date, end_date = get_pay_period(date)
    assert start_date == datetime(2024, 4, 28)
    assert end_date == datetime(2024, 5, 11)


def test_is_date_in_first_week():
    date = datetime(2024, 5, 2)
    assert is_date_in_first_week(date) == True
    date = datetime(2024, 4, 28)
    assert is_date_in_first_week(date) == True
    date = datetime(2024, 4, 19)
    assert is_date_in_first_week(date) == True
    date = datetime(2024, 5, 7)
    assert is_date_in_first_week(date) == False
    date = datetime(2024, 5, 5)
    assert is_date_in_first_week(date) == False
    date = datetime(2024, 4, 27)
    assert is_date_in_first_week(date) == False
