"""Utility functions for data collection with LISC."""

###################################################################################################
###################################################################################################

def make_term(term, incl_joiner='OR'):
    """Make a full search term argument.

    Parameters
    ----------
    term : Term
        Term information.
    incl_joiner : {'OR', 'AND'}
        The joiner to use to combine the inclusion words.

    Returns
    -------
    str
        The complete search term.
    """

    return join(join(make_comp(term.search), make_comp(term.inclusions, incl_joiner), 'AND'),
                make_comp(term.exclusions), 'NOT')


def make_comp(terms, joiner='OR'):
    """Make a search term component.

    Parameters
    ----------
    terms : list of str
        List of words to connect together with 'OR'.
    joiner : {'OR', AND', 'NOT'}
        The string to join together the inputs with.

    Returns
    -------
    comp : str
        Search term component.

    Notes
    -----
    - This function deals with empty list inputs.
    - This function adds "" to terms to make them exact search only.
    """

    comp = ''
    if terms and terms[0]:
        terms = ['"'+ item + '"' for item in terms]
        comp = '(' + joiner.join(terms) + ')'

    return comp


def join(front, back, joiner='AND'):
    """Join strings together with a specified joiner.

    Parameters
    ----------
    front, back : str
        Strings to join together.
    joiner : {'AND', 'OR', 'NOT'}
        The string to join together the inputs with.

    Returns
    -------
    str
        Concatenated string.

    Notes
    -----
    This function only adds the join if both strings are non-empty.
    """

    return front + joiner + back if (front and back) else front + back
