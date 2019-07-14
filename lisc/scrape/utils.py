"""Utility functions for scraping with LISC."""

###################################################################################################
###################################################################################################

def join(front, back, joiner='AND'):
    """Join strings together with a specified joiner.

    Parameters
    ----------
    front, back : str
        Strings to join together.
    joiner : {'AND' or 'NOT'}
        The string to join together the inputs with.

    Returns
    -------
    str
        Concatenated string.

    Notes
    -----
    - This function only adds the join if both strings are non-empty.
    """

    return front + joiner + back if (front and back) else front + back


def mk_term(terms):
    """Create search term component.

    Parameters
    ----------
    terms : list of str
        List of words to connect together with 'OR'.

    Returns
    -------
    str
        Search term.

    Notes
    -----
    - This function deals with empty list inputs.
    - This function adds "" to terms to make them exact search only.
    """

    out = ''

    if terms and terms[0]:
        terms = ['"'+ item + '"' for item in terms]
        out = '(' + 'OR'.join(terms) + ')'

    return out
