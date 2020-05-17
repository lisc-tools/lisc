"""Analysis functions for counts and co-occurrence data."""

import numpy as np

###################################################################################################
###################################################################################################

def compute_normalization(data, counts, dim='A'):
    """Compute a normalization of the co-occurrence data.

    Parameters
    ----------
    data : 2d array
        Counts of co-occurrence of terms.
    counts : 1d array
        Counts for each individual search term.
    dim : {'A', 'B'}, optional
        Which set of terms to operate upon.

    Returns
    -------
    out : 2d array
        The normalized co-occurrence data.

    Notes
    -----
    This computes a normalized data matrix as a percent of articles expressing co-occurrence.

    Examples
    --------
    Compute normalized co-occurrences between two lists of terms:

    >>> from lisc.collect import collect_counts
    >>> terms_a = [['frontal lobe'], ['parietal lobe']]
    >>> terms_b = [['decision making'], ['sensory']]
    >>> coocs, counts, meta_dat = collect_counts(terms_a=terms_a, terms_b=terms_b) # doctest:+SKIP
    >>> normed_coocs = compute_normalization(coocs, counts[0]) # doctest:+SKIP
    """

    if dim == 'A':

        if not len(counts) == data.shape[0]:
            raise ValueError('Data shapes are inconsistent.')

        counts_2d = np.tile(counts, [data.shape[1], 1]).T

    elif dim == 'B':

        if not len(counts) == data.shape[1]:
            raise ValueError('Data shapes are inconsistent.')

        counts_2d = np.tile(counts, [data.shape[0], 1])

    else:
        raise ValueError('Specified dimension not understood.')

    out = data / counts_2d

    return out


def compute_association_index(data, counts_a, counts_b):
    """Compute the association index from the co-occurrence data.

    Parameters
    ----------
    data : 2d array
        Counts of co-occurrence of terms.
    counts_a, counts_b : 1d array
        Counts for each individual search term.

    Returns
    -------
    index : 2d array
        The association score of the co-occurrence data.

    Notes
    -----
    This computes a the Jaccard index, as :math:`AI_{ij} = |c_{ij} N d_{ij}| / |c_{ij} U d_{ij}|`.

    The denominator, :math:`|c_{ij} U d_{ij}|`, is equivalent to
    :math:`|c_{ij}| + |d_{ij}| - |c_{ij} N d_{ij}|`.

    Examples
    --------
    Compute the association index between two lists of terms:

    >>> from lisc.collect import collect_counts
    >>> terms_a = [['frontal lobe'], ['parietal lobe']]
    >>> terms_b = [['decision making'], ['sensory']]
    >>> coocs, counts, meta_dat = collect_counts(terms_a=terms_a, terms_b=terms_b) # doctest:+SKIP
    >>> index = compute_association_index(coocs, counts[0], counts[1]) # doctest:+SKIP
    """

    n_a = len(counts_a)
    n_b = len(counts_b)

    if not n_a == data.shape[0] and n_b == data.shape[1]:
        raise ValueError('Data shapes are inconsistent.')

    denominator = np.tile(counts_a, [n_b, 1]).T + np.tile(counts_b, [n_a, 1]) - data
    index = data / denominator

    return index
