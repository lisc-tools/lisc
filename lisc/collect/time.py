"""Collect data across time."""

import numpy as np

###################################################################################################
###################################################################################################

def collect_across_time(obj, years, **collect_kwargs):
    """Collect data across time epochs.

    Parameters
    ----------
    obj : Counts1D, Counts, Words
        Object to collect data with.
    years : list of int
        Years to collect literature for.

    Returns
    -------
    results : dict
        Results collected across time.
        Each key reflects the start year, and each value is a object with search results.

    Notes
    -----
    Time regions are defined as the set of regions {start of `years[n]` to end of `years[n]-1`}.
    For example, for `years = [1990, 1995, 2000]`, this would search for:
        {01/01/1990 to 12/31/1994; 01/01/1995 to 12/31/1990}
    Similarly, for `years = [2000, 2001, 2002, 2003]`, this would search for:
        {01/01/2000 to 12/31/2000; 01/01/2001 to 12/31/2001; 01/01/2002 to 12/31/2002}
    Note that this means that final element in `years` is not included in the search.
    Also, this function only currently supports contiguous, whole year search times.

    Examples
    --------
    Collect counts for a single set of search terms, across time:

    >>> from lisc.objects.counts import Counts1D
    >>> counts = Counts1D()
    >>> counts.add_terms([['frontal lobe'], ['temporal lobe']])
    >>> years = [1950, 1975, 2000]
    >>> results = collect_across_time(counts, years)
    """

    results = {}
    for start, end in zip(years, np.array(years[1:]) - 1):

        obj.run_collection(mindate=str(start) + '/01/01',
                           maxdate=str(end) + '/12/31',
                           **collect_kwargs)
        results[start] = obj.copy()

    return results
