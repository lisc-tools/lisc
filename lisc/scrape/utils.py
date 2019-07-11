"""Basic utility functions for LISC."""

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


def extract(dat, tag, how):
    """Extract data from HTML tag.

    Parameters
    ----------
    dat : bs4.element.Tag
        HTML data to pull specific tag out of.
    tag : str
        Label of the tag to extract.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to extract the data.
            raw - extract an embedded tag
            str - extract text and convert to string
            all - extract all embedded tags

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    # Check how spec if valid
    if how not in ['raw', 'str', 'all']:
        raise ValueError('Value for how is not understood.')

    # Use try to be robust to missing tag
    try:
        if how == 'raw':
            return dat.find(tag)
        elif how == 'str':
            return dat.find(tag).text
        elif how == 'all':
            return dat.findAll(tag)

    except AttributeError:
        return None
