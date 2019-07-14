"""Decorators for LISC."""

from functools import wraps

###################################################################################################
###################################################################################################

def CatchNone(func):
    """Decorator function to catch and return None, if given as first argument."""

    @wraps(func)
    def wrapper(*args):

        if args[0] is not None:
            return func(*args)
        else:
            return None

    return wrapper


def CatchNone2(func):
    """Decorator function to catch and return None, None if given as argument."""

    @wraps(func)
    def wrapper(*args):

        if args[0] is not None:
            return func(*args)
        else:
            return None, None

    return wrapper
