from datetime import date


def clean_boolean(value, default=None):
    try:
        return bool(int(value))
    except ValueError:
        return 0


def clean_integer(value, default=None):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def clean_date(value, default=None):
    try:
        year = int(value[:4])
        month = int(value[4:6])
        day = int(value[6:])
        return date(year, month, day)
    except ValueError:
        return default


clean_map = {
    'INTEGER': clean_integer,
    'BOOLEAN': clean_boolean,
    'DATE': clean_date,
}


def get_cleaner(type):
    return clean_map.get(type)
