# payrolldates

## Install Locally

```sh
pip install -e .
```

## Install from github

```sh
pip install "payrolldates @ git+https://<github_token>@github.com/Davenport-Iowa/cod-py-payroll-dates.git" 
``` 

## Testing

### Install Test Dependancies


```sh
pip install .[test]
```

### Run Tests

```sh
pytest
```

## Usage

### Description

Use the library to determine start and end dates of payroll

You can pass a date to the functions to get the start and end payroll dates for a specific date. 

### Import 

```python
# import functions from the package
from payrolldates.calc import get_pay_period, is_date_in_first_week, print_pay_period
# Use full std lib for dates
from datetime import datetime
```

### Usage

Get payperiod from date

```python
# Get the start and end dates for the current payperiod
start_date, end_date = get_pay_period(datetime.now())
```

Get a historical payperiod from date
```python
start_date, end_date = get_pay_period(datetime(2024, 4, 27))
```

You can also check if it is the first week of the payroll

> [!TIP]
> is_date_in_first_week(date) is helpful if determining when to run an automated job

```python
if is_date_in_first_week(datetime.now()):
    print("First Week!")
else:
    print("Not First Week")
```


