"""Utility functions for scraping with LISC."""

###################################################################################################
###################################################################################################

def comb_terms(lst, joiner):
    """Combine a list of terms to use as search arguments.

    Parameters
    ----------
    lst : list of str
        List of terms to combine together.
    joiner : {'or', 'not'}
        Term to use to join together terms.

    Returns
    -------
    out : str
        String created by combining the inputs.
    """

    # Add quotes to list items for exact search
    lst = ['"'+ item + '"' for item in lst]

    # Join together using requested join term
    if joiner.lower() == 'or':
        out = '(' + 'OR'.join(lst) + ')'
    elif joiner.lower() == 'not':
        out = 'NOT' + 'NOT'.join(lst)
    else:
        raise ValueError('Join term not understood.')

    return out


def mk_term(t_lst, cm=''):
    """Create search term component.

    Parameters
    ----------
    t_lst : list of str
        List of words to connect together.
    cm : str
        Connector word to append to front of search term.

    Returns
    -------
    str
        Search term.
    """

    if t_lst and t_lst[0]:
        return cm + comb_terms(t_lst, 'or')
    else:
        return ''
