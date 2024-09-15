from datetime import timedelta
from datetime import datetime

def add_timedelta(td1: timedelta, td2: timedelta) -> timedelta:
    """Add timedelta to timedelta"""
    return td1 + td2

def subtract_timedelta(td1: timedelta, td2: timedelta) -> timedelta:
    """Subtract timedelta from timedelta"""
    return td1 - td2

def add_timedelta_to_datetime(dt: datetime, td: timedelta) -> datetime:
    """Add timedelta to datetime"""
    return dt + td

def subtract_timedelta_from_datetime(dt: datetime, td: timedelta) -> datetime:
    """Add timedelta to datetime"""
    return dt - td

class CustomTimedelta:
    def __init__(self, weeks=0, days=0, hours=0, minutes=0, seconds=0):
        self.timedelta = timedelta(weeks=weeks, days=days, hours=hours, minutes=minutes, seconds=seconds)
    
    def __eq__(self, other):
        if isinstance(other, CustomTimedelta):
            return self.timedelta == other.timedelta
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, CustomTimedelta):
            return self.timedelta < other.timedelta
    
    def __le__(self, other):
        if isinstance(other, CustomTimedelta):
            return self.timedelta <= other.timedelta
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, CustomTimedelta):
            return self.timedelta > other.timedelta
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, CustomTimedelta):
            return self.timedelta >= other.timedelta
        return NotImplemented

    def __str__(self):
        return str(self.timedelta)