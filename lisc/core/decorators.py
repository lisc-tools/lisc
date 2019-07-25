"""Decorators for LISC."""

from functools import wraps

###################################################################################################
###################################################################################################

def catch_none(n_return=1):
    """Decorator function to catch and return None, if given as first argument.

    Parameters
    ----------
    n_return : {1, 2}
        The number of Nones to return as input, if input is None.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            if args[0] is not None:
                return func(*args, **kwargs)

            else:

                if n_return == 1:
                    return None
                elif n_return == 2:
                    return None, None

        return wrapper

    return decorator
