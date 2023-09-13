"""Analysis functions for data collected across time."""

import numpy as np

###################################################################################################
###################################################################################################

def get_counts_across_years(results):
    """Extract counts from a collection across years.

    Parameters
    ----------
    results : dict
        Results collected across time, reflecting a 'counts' collection.
        Each key should reflect the start year, and each value is a object with search results.

    Returns
    -------
    labels : list of str
        Labels for the search terms.
    years : list of int
        Years the results were collected across.
    data : 2d array
        Data for the counts results across time, with shape [n_labels, n_years].
    """

    labels = list(results.values())[0].labels
    years = list(results.keys())
    data = np.array([el.counts for el in results.values()]).T

    return labels, years, data
