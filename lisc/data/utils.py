"""Utilities for data management and data object for LISC."""

###################################################################################################
###################################################################################################

def combine_lists(in_lst):
    """Combine list of lists into one large list.

    Parameters
    ----------
    in_lst : list of list of str
        Embedded lists to combine.

    Returns
    -------
    out : list of str
        Combined list.
    """

    out = []

    for el in in_lst:
        if el:
            out.extend(el)

    return out


def count_occurences(data_lst):
    """Count occurences of each item in a list.

    Parameters
    ----------
    data_lst : list of str
        List of items to count occurences of.

    Returns
    -------
    counts : list of tuple of (count, item_label)
        Counts for how often each item occurs in the input list.
    """

    counts = [(data_lst.count(element), element) for element in set(data_lst)]
    counts.sort(reverse=True)

    return counts
