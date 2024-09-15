"""
EasyChrono - A Python package for working with timedelta objects.

This package provides utilities for parsing, formatting, manipulations of time intervals,
parsing relative dates, and integration with SQlite3

Modules:
- parser: Functions to parse human-readable time intervals into timedelta objects.
- formatter: Functions to format timedelta objects into human-readable strings.
- operations: Functions to perform arithmetic operations on timedelta objects.
- utils: Utility functions for creating and validating timedelta objects, and calculating durations from now.
- Database: Functions for creating a SQlite3 database, saving and loading timedelta objects to/from a database.

Example usage:
    >>> from easychrono import parse_delta, parse_relative_date, format_timedelta, format_timedelta_custom, add_timedelta, subtract_timedelta, add_timedelta_to_datetime, subtract_timedelta_from_datetime, create_timedelta, validate_timedelta_input, duration_from_now, setup_database, save_timedelta, load_timedelta
    >>> td = parse_delta("5d3h30m45s")
    >>> format_timedelta(td)
    '5 days, 3 hours, 30 minutes, 45 seconds'
    >>> td1 timedelta(days=1, hours=2)
    >>> td2 timedelta(days=2, hours=3)
    >>> add_timedelta(td1, td2)
    datetime.timedelta(days=3, hours=5)
    >>> subtract_timedelta(td2, td1)
    datetime.timedelta(hours=1)
    >>> duration_from_now(datetime(2024, 12, 31, 23, 59))
    'X days, X hours, X minutes'  # Output depends on the current date and time
"""

from .parser import parse_delta, parse_relative_date
from .formatter import format_timedelta, format_timedelta_custom
from .operations import add_timedelta, subtract_timedelta, add_timedelta_to_datetime, subtract_timedelta_from_datetime
from .utils import validate_timedelta_input, duration_from_now
from .database import setup_database, save_timedelta, load_timedelta
