from datetime import datetime


def format_datetime(date: datetime | str) -> datetime:
    if isinstance(date, datetime):
        return date.strftime('%d.%m.%Y %H:%M')
    date_str = date.replace('T', ' ')
    return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')