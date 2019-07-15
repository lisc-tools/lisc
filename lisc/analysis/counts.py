"""Analysis functions for counts and co-occurence data."""

import numpy as np

###################################################################################################
###################################################################################################

def compute_normalization(data, counts, dim='A'):
    """Compute a normalization of the co-occurence matrix by the counst

    Parameters
    ----------
    data : 2d array
        Counts of co-occurence of terms.
    counts : 1d array
        Counts for each individual search term.

    Returns
    -------
    out : 2d array
        The normalized co-occurence data.

    Notes
    -----
    - This computes a data matrix matrix as a percent of papers expressing co-occurence.
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
    """Compute the association index from the co-occurence data.

    Parameters
    ----------
    data : 2d array
        Counts of co-occurence of terms.
    counts_a, counts_b : 1d array
        Counts for each individual search term.

    Returns
    -------
    out : 2d array
        The association score of the co-occurence data.

    Notes
    -----
    - This computes a the jaccard similarity, as AI_ij = |c_ij N d_ij| / |c_ij U d_ij|
    """

    n_a = len(counts_a)
    n_b = len(counts_b)

    if not n_a == data.shape[0] and n_b == data.shape[1]:
        raise ValueError('Data shapes are inconsistent.')

    combined_counts = np.tile(counts_a, [n_b, 1]).T + np.tile(counts_b, [n_a, 1])
    out = data / combined_counts

    return out
