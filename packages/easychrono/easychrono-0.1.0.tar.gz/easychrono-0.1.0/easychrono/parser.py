from datetime import timedelta, datetime
import re

TIMEDELTA_REGEX = (
    r'(?:(?P<weeks>-?\d+)\s*(?:w|week|weeks)\s*)?'    # Match weeks
    r'(?:(?P<days>-?\d+)\s*(?:d|day|days)\s*)?'      # Match days
    r'(?:(?P<hours>-?\d+)\s*(?:h|hour|hours)\s*)?'    # Match hours
    r'(?:(?P<minutes>-?\d+)\s*(?:m|min|minute|minutes)\s*)?'  # Match minutes
    r'(?:(?P<seconds>-?\d+)\s*(?:s|sec|second|seconds)\s*)?'  # Match seconds
)

TIMEDELTA_PATTERN = re.compile(TIMEDELTA_REGEX, re.IGNORECASE)

def parse_delta(delta: str) -> timedelta:
    """Parses a human-readable timedelta (e.g., 5d3h30m45s or 1w2d3h4m5s) into a datetime.timedelta."""
    match = TIMEDELTA_PATTERN.match(delta)
    if match:
        parts = match.groupdict()
        weeks = int(parts['weeks']) if parts['weeks'] else 0
        days = int(parts['days']) if parts['days'] else 0
        hours = int(parts['hours']) if parts['hours'] else 0
        minutes = int(parts['minutes']) if parts['minutes'] else 0
        seconds = int(parts['seconds']) if parts['seconds'] else 0

        # Convert all parts to total seconds
        total_seconds = (
            (weeks * 7 * 24 * 3600) +  # weeks to seconds
            (days * 24 * 3600) +      # days to seconds
            (hours * 3600) +          # hours to seconds
            (minutes * 60) +          # minutes to seconds
            seconds                   # add seconds
        )

        # Return timedelta with total seconds
        return timedelta(seconds=total_seconds)
    else:
        raise ValueError(f"Invalid timedelta format: `{delta}`")
    

def parse_relative_date(date_str: str) -> datetime:
    """Parse relative date strings such as "tomorrow", "next monday", or "in 3 weeks" """
    now = datetime.now()

    # Handle specific keywords
    if date_str.lower() == "tomorrow":
        return now + timedelta(days=1)
    
    if date_str.lower() == "yesterday":
        return now - timedelta(days=1)
    
    # Handle "next <weekday>"
    match = re.match(r"next (\w+)", date_str.lower())
    if match:
        weekday = match.group(1)
        weekdays =["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        if weekday in weekdays:
            today_weekday = now.weekday()
            target_weekday = weekdays.index(weekday)
            days_until_next = (target_weekday - today_weekday + 7) % 7 or 7
            return now + timedelta(days=days_until_next)
    
    # Handle " in X hours/days/weeks"
    match = re.match(r"in (\d+) (days|weeks|hours|minutes|seconds)", date_str.lower())
    if match:
        quantity = int(match.group(1))
        unit = match.group(2)
        if unit == "days":
            return now + timedelta(days=quantity)
        elif unit == "weeks":
            return now + timedelta(weeks=quantity)
        elif unit == "hours":
            return now + timedelta(hours=quantity)
        elif unit == "minutes":
            return now + timedelta(minutes=quantity)
        elif unit == "seconds":
            return now + timedelta(seconds=quantity)
    
    raise ValueError("Unsupported relative date format")