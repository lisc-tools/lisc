"""Analysis functions for words data."""

from lisc import Words

###################################################################################################
###################################################################################################

def get_attribute_counts(words, attribute):
    """Get count of how many articles contain values for a requested attribute.

    Parameters
    ----------
    words : Words or list of Articles
        Literature data.
    attribute : str
        Which attribute to check.

    Returns
    -------
    int
        The number of articles across the object that have the requested attribute.
    """

    return sum([1 if values else 0 for comp in words for values in getattr(comp, attribute)])


def get_all_values(data, attribute, unique=False):
    """Get all values for a field of interest.

    Parameters
    ----------
    data : Words or list of Articles
        Data to extract attribute of interest from.
    attribute : str
        The attribute to extract from the data objects.
    unique : bool, optional, default: False
    	Whether to restrict extracted values to only unique elements.

    Returns
    -------
    values : list
        Extracted values from across all the data objects.
    """

    values = [values for component in data for values in getattr(component, attribute)]

    if unique:
        values = list(set(values))

    return values


def get_all_counts(data, attribute, combine=False):
    """Get all counts for a field of interest.

    Parameters
    ----------
    data : words or list of ArticlesAll
        Article data to extract counts for an attribute of interest.
    attribute : str
        The attribute to extract from the data.
    combine : bool, optional, default: False
    	Whether to combine the counts across all search terms.

    Returns
    -------
    counts : list
        Extracted counts from across all the data objects.
    """

    if isinstance(data, Words):
        data = data.combined_results

    counts = [getattr(datum, attribute) for datum in data]

    if combine:
        counts = sum(counts, type(counts[0])())

    return counts
