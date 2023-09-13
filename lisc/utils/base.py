"""Base level utilities - for working with standard library data types."""

from itertools import chain

###################################################################################################
###################################################################################################

def wrap(string, char="'"):
    """Wrap a string in a specified character.

    Parameters
    ----------
    string : str
        Input string.
    char : str
        The character to wrap around the string.

    Returns
    -------
    str
        The input string wrapped in single quotes.
    """

    return char + string + char


def get_max_length(lst, add=0):
    """Get the length of the longest element in a list.

    Parameters
    ----------
    lst : list
        A list of element to check the length of.
    add : int, optional
        Amount to add to max length, to add as a buffer.

    Returns
    -------
    max_len : int
        The length of the longest element in lst.

    Notes
    -----
    - The longest element is in terms of the length of the element as a string.
    - If the first list element is not a string, all elements are typecast to str.
    """

    if not isinstance(lst[0], str):
        lst = map(str, lst)

    max_len = len(max(lst, key=len))

    return max_len + add


def flatten(lst):
    """Flatten embedded lists.

    Parameters
    ----------
    lst : list of list
        List of embedded lists, to flatten.

    Returns
    -------
    list
        Flattened list.
    """

    return list(chain.from_iterable(lst))
