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
        String
    """

    # Add quotes to list items for exact search
    lst = ['"'+ item + '"' for item in lst]

    # Join together using requested join term
    if joiner == 'or':
        out = '(' + 'OR'.join(lst) + ')'
    elif joiner == 'not':
        out = 'NOT' + 'NOT'.join(lst)
    else:
        raise ValueError('Join term not understood.')

    return out


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

###################################################################################################
###################################################################################################

def CatchNone(func):
    """Decorator function to catch and return None, if given as first argument."""

    def wrapper(*args):

        if args[0] is not None:
            return func(*args)
        else:
            return None

    return wrapper


def CatchNone2(func):
    """Decorator function to catch and return None, None if given as argument."""

    def wrapper(*args):

        if args[0] is not None:
            return func(*args)
        else:
            return None, None

    return wrapper
