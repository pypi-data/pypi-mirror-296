from datetime import timedelta

def format_timedelta(td: timedelta) -> str:
    """Formats a timedelta object into a human-readable string (e.g., 5d3h30m45s in 5 days, 3 hours, 30 minutes, 45 seconds)."""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    parts = []

    if days:
        parts.append(f"{days} days")
    if hours:
        parts.append(f"{hours} hours")
    if minutes:
        parts.append(f"{minutes} minutes")
    if seconds:
        parts.append(f"{seconds} seconds")

    return ", ".join(parts)

def format_timedelta_custom(td: timedelta, include_weeks=False, include_days=True, include_hours=True, include_minutes=True, include_seconds=True, separator=', ') -> str:
    """Format a timedelta object with customizable options."""
    total_seconds = int(td.total_seconds())
    weeks, remainder = divmod(total_seconds, 604800)  # 1 week = 604800 seconds
    days, remainder = divmod(remainder, 86400)        # 1 day = 86400 seconds
    hours, remainder = divmod(remainder, 3600)        # 1 hour = 3600 seconds
    minutes, seconds = divmod(remainder, 60)          # 1 minute = 60 seconds
    
    parts = []
    if include_weeks and weeks:
        parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
    if include_days and days:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if include_hours and hours:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if include_minutes and minutes:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if include_seconds and seconds:
        parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    
    return separator.join(parts) if parts else "0 seconds"