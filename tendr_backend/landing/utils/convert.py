from datetime import datetime


def convert_to_datetime(item):
    return datetime.strptime(item, "%a %b %d %H:%M:%S %Z %Y")
