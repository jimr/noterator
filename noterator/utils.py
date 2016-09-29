# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps


def enum(*listed, **named):
    enums = dict(zip(listed, range(len(listed))), **named)
    return type('Enum', (), enums)


def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def catch_all(func):
    """Simple decorator that wraps a function in a silent tr/except.

    Useful for wrapping functions that might fail but shouldn't propagate that
    failure to the caller. For example, notifications might break, but we don't
    want that to interrupt the iteration.

    """
    @wraps(func)
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            pass
    return _inner
