import json
import re
from datetime import timedelta
from types import SimpleNamespace

from janny.config import API_HOST
from janny.auth import SESSION


def get(path: str) -> SimpleNamespace:
    """Convert a JSON response into a Python object"""
    s = SESSION
    data = s.get(API_HOST + path).content
    obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return obj


timedelta_regex = (
    r"((?P<days>-?\d+)d)?" r"((?P<hours>-?\d+)h)?" r"((?P<minutes>-?\d+)m)?"
)

timedelta_pattern = re.compile(timedelta_regex, re.IGNORECASE)


def parse_delta(delta: str) -> timedelta:
    """Parses a human readable timedelta (3d5h19m) into a datetime.timedelta.
    Delta includes:
    * Xd days
    * Xh hours
    * Xm minutes
    Values can be negative following timedelta's rules. Eg: -5h-30m
    """
    match = timedelta_pattern.match(delta)
    if match:
        parts = {k: int(v) for k, v in match.groupdict().items() if v}
        return timedelta(**parts)
    return timedelta(0)


# List of running threads. Storing it here to prevent circular imports.
RUNNING = list()
