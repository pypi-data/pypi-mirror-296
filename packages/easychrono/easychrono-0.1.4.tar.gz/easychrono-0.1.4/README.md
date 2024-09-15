# EasyChrono

`EasyChrono` is a python package for working with `Timedelta` objects, including parsing, formatting, manipulations of time intervals, parsing relative dates, and integration with databases.

## Installation

You can install `EasyChrono` using pip:

```bash
pip install easychrono
```

## Parsing Timedelta

```py
from easychrono.parser import parse_delta

td = parse_delta("5h3h19m45s")
print(td) # Outputs: 5 days, 3:19:45
```

## Formatting Timedelta

```py
from easychrono.formatter import format_timedelta

formatted_td = format_timedelta(timedelta(days=5, hours=3, minutes=19, seconds=45))
print(formatted_td)  # Outputs: 5 days, 3 hours, 19 minutes, 45 seconds
```

## Adding and Subtracting Timedeltas

```py
from easychrono.operations import add_timedelta, subtract_timedelta

td1 = timedelta(days=5)
td2 = timedelta(days=3)
result = add_timedelta(td1, td2)
print(result)  # Outputs: 8 days, 0:00:00

result = subtract_timedelta(td1, td2)
print(result)  # Outputs: 2 days, 0:00:00
```

## Parsing Relative Dates

```py
from easychrono.utils import parse_relative_date

date = parse_relative_date("next Monday")
print(date)  # Outputs: Date of next Monday
```

# Database Integration

## Setting Up the Database

```py
from easychrono.database import setup_database

setup_database("MyDatabase.db")
```

## Storing a Timedelta

```py
from datetime import timedelta
from easychrono import save_timedelta

my_timedelta = timedelta(hours=5, minutes=19, seconds=45)
description = "Work Hours"

save_timedelta(description, my_timedelta)
```

## Retriving a Timedelta

```py
from easychrono import load_timedelta
try:
    stored_timedelta, description = load_timedelta(1)
    print(f"Loaded timedelta: {stored_timedelta}")
    print(f"Description: {description}")
except ValueError as e:
    print(e)
```

# Contributing

We welcome contributions to EasyChrono. If you'd like to contribute, please follow the guidelines in our [CONTRIBUTING.md](https://github.com/Legendofpokemon/EasyChrono/blob/master/CONTRIBUTING.md) file.

# License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Legendofpokemon/EasyChrono/blob/master/LICENSE) file for details.
