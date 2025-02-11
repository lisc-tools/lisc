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

    Examples
    --------
    >>> from lisc.data.term import Term

    Create a search term from a simple term definition:

    >>> term1 = Term(label='term1', search=['term1'], inclusions=['incl1'], exclusions=['excl1'])
    >>> make_term(term1)
    '("term1")AND("incl1")NOT("excl1")'

    Create a search term from a more complicated term definition:

    >>> term2 = Term(label='term2',
    ...              search=['term2', 'term2b'],
    ...              inclusions=['incl2', 'incl2b'],
    ...              exclusions=['excl2', 'excl2b'])
    >>> make_term(term2)
    '("term2"OR"term2b")AND("incl2"OR"incl2b")NOT("excl2"OR"excl2b")'
    """

    return join(join(make_comp(term.search), make_comp(term.inclusions, incl_joiner), 'AND'),
                make_comp(term.exclusions), 'NOT')


def make_comp(terms, joiner='OR'):
    """Make a search term component.

    Parameters
    ----------
    terms : list of str
        List of words to connect together with 'OR'.
    joiner : {'OR', 'AND', 'NOT'}
        The string to join together the inputs with.

    Returns
    -------
    comp : str
        Search term component.

    Notes
    -----
    - This function deals with empty list inputs.
    - This function adds "" to terms to make them exact search only.
    - This function replaces any spaces in terms with '+'.

    Examples
    --------
    Make a search component for a single term:

    >>> make_comp(['term1'])
    '("term1")'

    Make a search component for multiple terms together:

    >>> make_comp(['term1a', 'term1b'])
    '("term1a"OR"term1b")'

    Make a search component for multiple terms together, specifying the joiner:

    >>> make_comp(['term1a', 'term1b'], joiner='AND')
    '("term1a"AND"term1b")'
    """

    comp = ''
    if terms and terms[0]:
        terms = ['"'+ item + '"' for item in terms]
        comp = '(' + joiner.join(terms) + ')'
        comp = comp.replace(' ', '+')

    return comp


def join(front, back, joiner='AND'):
    """Join search term components together with a specified joiner.

    Parameters
    ----------
    front, back : str
        Strings to join together.
        Should be valid search term components (outputs of `make_comp`).
    joiner : {'OR', 'AND', 'NOT'}
        The string to join together the inputs with.

    Returns
    -------
    str
        Concatenated string.

    Notes
    -----
    This function only adds the join if both strings are non-empty.

    Examples
    --------
    Join single-term search term components together:

    >>> join('("term1")', '("incl1")')
    '("term1")AND("incl1")'

    Join multi-term search term components together:

    >>> join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")')
    '("term1a"OR"term1b")AND("incl1a"OR"incl1b")'

    Join multi-term search term components together, specifying the joiner:

    >>> join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")', joiner='OR')
    '("term1a"OR"term1b")OR("incl1a"OR"incl1b")'
    """

    return front + joiner + back if (front and back) else front + back
