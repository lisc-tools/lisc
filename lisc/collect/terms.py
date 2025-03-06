"""Functionality for creating search terms."""

###################################################################################################
###################################################################################################

# Define list of possible joiners
JOINERS = ['AND', 'OR', 'NOT']

# Default default joiners to use to join individual terms within each type
DEFAULT_TERM_JOINERS = {
    'search' : 'OR',
    'inclusions' : 'OR',
    'exclusions' : 'OR',
}

def check_joiner(joiner):
    """Check if a joiner definition is valid.

    Parameters
    ----------
    joiner : {'OR', 'AND', 'NOT'}
        A string to join together search term elements.

    Raises
    ------
    ValueError
        If an invalid joiner value is given.
    """

    if joiner not in JOINERS:
        raise ValueError('Invalid term joiner.')


def make_term(term, joiners=DEFAULT_TERM_JOINERS):
    """Make a full search term argument.

    Parameters
    ----------
    term : Term
        Term information.
    joiners : dict
        The joiner to use for each of the term types.
        Should have keys ['search', 'inclusions', 'exclusions']
        Each key should be one of {'OR', 'AND', 'NOT'}.

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

    for joiner in joiners.values():
        check_joiner(joiner)

    # Create list of sections - search terms, inclusions, exclusions
    sections = [make_comp(term.search, joiners['search']),
                make_comp(term.inclusions, joiners['inclusions']),
                make_comp(term.exclusions, joiners['exclusions'])]
    # Define joiners to combine - (SEARCH)AND(INCLUSIONS)NOT(EXCLUSIONS)
    section_joiners = ['AND', 'NOT']

    return join_multi(sections, section_joiners)


def make_comp(terms, joiner):
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

    >>> make_comp(['term1'], joiner='OR')
    '("term1")'

    Make a search component for multiple terms together, joining with 'OR':

    >>> make_comp(['term1a', 'term1b'], joiner='OR')
    '("term1a"OR"term1b")'

    Make a search component for multiple terms together, joining with 'AND':

    >>> make_comp(['term1a', 'term1b'], joiner='AND')
    '("term1a"AND"term1b")'
    """

    check_joiner(joiner)

    comp = ''
    if terms and terms[0]:
        terms = ['"'+ item + '"' for item in terms]
        comp = '(' + joiner.join(terms) + ')'
        comp = comp.replace(' ', '+')

    return comp


def join(front, back, joiner):
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

    >>> join('("term1")', '("incl1")', joiner='AND')
    '("term1")AND("incl1")'

    Join multi-term search term components together, with 'AND' joiner:

    >>> join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")', joiner='AND')
    '("term1a"OR"term1b")AND("incl1a"OR"incl1b")'

    Join multi-term search term components together, with 'OR' joiner:

    >>> join('("term1a"OR"term1b")', '("incl1a"OR"incl1b")', joiner='OR')
    '("term1a"OR"term1b")OR("incl1a"OR"incl1b")'
    """

    check_joiner(joiner)

    return front + joiner + back if (front and back) else front + back


def join_multi(sections, joiners):
    """Join multiple sections together into a search string.

    Parameters
    ----------
    sections : list of str
        List of sections to join together.
    joiners : list of str
        Joiners for between sections.
        Should be length of sections - 1.

    Returns
    -------
    joined : str
        Joined search string.

    Examples
    --------
    Create a joined search term from simple inputs (1 term per section):

    >>> join_multi(['("term1")', '("incl1")', '("excl1")'], ['AND', 'NOT'])
    '("term1")AND("incl1")NOT("excl1")'

    Create a joined search term from more complex inputs (2 terms per section):

    >>> sections = ['("term2"OR"term2b")', '("incl2"OR"incl2b")', '("excl2"OR"excl2b")']
    >>> joiners = ['AND', 'NOT']
    >>> join_multi(sections, joiners)
    '("term2"OR"term2b")AND("incl2"OR"incl2b")NOT("excl2"OR"excl2b")'
    """

    assert len(sections) - 1 == len(joiners), 'Inputs do not align'

    joined = sections[0]
    for csec, cjoin in zip(sections[1:], joiners):
        joined = join(joined, csec, cjoin)

    return joined
