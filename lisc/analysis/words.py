"""Analysis functions for words data."""

###################################################################################################
###################################################################################################

def get_all_values(all_data, attribute, unique=False):
    """Get all values for a field of interest.

    Parameters
    ----------
    all_data : list of lisc.ArticlesAll
        A list of data objects to extract data from.
    attribute : str
        The attribute to extract from the data objects.
    unique : bool, optional, default: False
    	Whether to restrict extracted values to only unique elements.

    Returns
    -------
    values : list
        Extracted values from across all the data objects.
    """

    values = [val for attrs in [getattr(data, attribute) for data in all_data] for val in attrs]

    if unique:
        values = list(set(values))

    return values


def get_all_counts(all_data, attribute, combine=False):
    """Get all counts for a field of interest.

    Parameters
    ----------
    all_data : list of lisc.ArticlesAll
        A list of data objects to extract data from.
    attribute : str
        The attribute to extract from the data objects.
    combine : bool, optional, default: False
    	Whether to combine the counts.

    Returns
    -------
    counts : list
        Extracted counts from across all the data objects.

    Notes
    -----
    This function works for 'counts' stored in different objects, including `Counter` & `FreqDist`.
    If combining values, the return type is the same as the object in the requested attribute.
    """

    counts = [getattr(data, attribute) for data in all_data]

    if combine:
        counts = sum(counts, type(counts[0])())

    return counts
