"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    '''returns date in a datetime object'''
    if not isinstance(date, str):
        raise TypeError('Input is not string')
    return (datetime.strptime(
                date, '%d.%m.%Y'))


def get_days_between(first: datetime, last: datetime) -> int:
    pass


def get_day_of_week_on(date: datetime) -> str:
    pass
