import requests


def count_month_work_days(month, year):

    response = requests.get(f'https://isdayoff.ru/api/getdata?year={year}&month={month}')
    count_work_days = 0
    if response.status_code == 200:
        for day in response.text:
            if int(day) == 0:
                count_work_days += 1
    return count_work_days


def count_month_days(month, year):
    response = requests.get(f'https://isdayoff.ru/api/getdata?year={year}&month={month}')
    return int(len(str(response.text)))
