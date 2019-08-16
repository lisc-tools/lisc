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
    - This computes a normalized data matrix as a percent of articles expressing co-occurrence.
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
    - This computes a the Jaccard index, as AI_ij = |c_ij N d_ij| / |c_ij U d_ij|
    - The denominator, |c_ij U d_ij|, is equivalent to |c_ij| + |d_ij| - |c_ij N d_ij|
    """

    n_a = len(counts_a)
    n_b = len(counts_b)

    if not n_a == data.shape[0] and n_b == data.shape[1]:
        raise ValueError('Data shapes are inconsistent.')

    denominator = np.tile(counts_a, [n_b, 1]).T + np.tile(counts_b, [n_a, 1]) - data
    index = data / denominator

    return index
