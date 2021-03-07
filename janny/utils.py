import logging
import json
from types import SimpleNamespace

from janny.config import API_HOST
from janny.auth import SESSION


def get(path):
    """Convert a JSON response into a Python object"""
    s = SESSION
    data = s.get(API_HOST + path).content
    obj = json.loads(data, object_hook=lambda d: SimpleNamespace(**d))
    return obj
