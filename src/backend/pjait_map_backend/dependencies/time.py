MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR


def to_seconds(weekday: int, time: str) -> int:
    hours, minutes = map(int, time.split(":"))
    return weekday * DAY + hours * HOUR + minutes * MINUTE


def get_weekday(seconds: int) -> int:
    return seconds // DAY


def get_time(seconds: int) -> str:
    hours = (seconds % DAY) // HOUR
    minutes = (seconds % DAY % HOUR) // MINUTE

    return f"{hours:02}:{minutes:02}"
