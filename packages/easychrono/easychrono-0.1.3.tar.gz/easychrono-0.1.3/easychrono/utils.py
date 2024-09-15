from datetime import datetime
from easychrono.formatter import format_timedelta
from easychrono.parser import TIMEDELTA_PATTERN

def duration_from_now(target_time: datetime) -> str:
    """Calculates the duration from the current time to a specific target time"""
    now = datetime.now()
    delta = target_time - now
    return format_timedelta(delta)

def validate_timedelta_input(delta: str) -> bool:
    """Validates the format of the input string."""
    return bool(TIMEDELTA_PATTERN.fullmatch(delta))
