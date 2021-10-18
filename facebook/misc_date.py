from datetime import datetime


def convert_date(date_time_str):
    date_time_object = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
    return date_time_object


def strip_date(date_time_str):
    return date_time_str.split(" ")[0]


def get_time(date):
    time = date.split(" ")[1][0:5]
    return time
