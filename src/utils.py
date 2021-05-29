import datetime

def seconds_to_human(seconds: int) -> str:
    return str(datetime.timedelta(seconds=round(seconds)))
