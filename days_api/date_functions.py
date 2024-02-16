"""Functions for working with dates."""

from datetime import datetime


def convert_to_datetime(date: str) -> datetime:
    '''returns date in a datetime object'''
    if not isinstance(date, str):
        raise TypeError('Input is not string')
    try:
        return (datetime.strptime(
                date, '%d.%m.%Y'))
    except(ValueError):
        raise ValueError("Unable to convert value to datetime.")
    


def get_days_between(first: datetime, last: datetime) -> int:
    '''returns the difference in days between two datetimes'''
    if not isinstance(first, datetime) or not isinstance(last, datetime):
        raise TypeError('Datetimes required.')
    return (last - first).days


def get_day_of_week_on(date: datetime) -> str:
    '''returns the day of the week of a given datetime'''
    if not isinstance(date, datetime):
        raise TypeError('Datetime required.')
    return date.strftime('%A')
