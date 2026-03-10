import datetime

def now():

    return datetime.datetime.utcnow()

def format_time(seconds):

    m, s = divmod(seconds,60)

    return f"{m}:{s:02}"