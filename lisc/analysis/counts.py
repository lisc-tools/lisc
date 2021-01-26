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
        Which set of terms to normalize by.
        'A' is equivalent to normalizing by rows values, 'B' to column values.

    Returns
    -------
    out : 2d array
        The normalized co-occurrence data.

    Notes
    -----
    This computes a normalized data matrix as a percent of articles expressing co-occurrence.
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
    This computes the Jaccard index, as :math:`AI_{ij} = |c_{ij} N d_{ij}| / |c_{ij} U d_{ij}|`.

    The denominator, :math:`|c_{ij} U d_{ij}|`, is equivalent to
    :math:`|c_{ij}| + |d_{ij}| - |c_{ij} N d_{ij}|`.
    """

    n_a = len(counts_a)
    n_b = len(counts_b)

    if not n_a == data.shape[0] and n_b == data.shape[1]:
        raise ValueError('Data shapes are inconsistent.')

    denominator = np.tile(counts_a, [n_b, 1]).T + np.tile(counts_b, [n_a, 1]) - data
    index = data / denominator

    return index


def compute_similarity(data, dim='A'):
    """Calculate the similarity across the co-occurrence data.

    Parameters
    ----------
    data : 2d array
        Counts of co-occurrence of terms.
    dim : {'A', 'B'}, optional
        Which set of terms to compute similarity across.
        'A' is equivalent to across rows, 'B' to across columns.

    Returns
    -------
    cosine : 2d array
        The cosine similarity of the co-occurrence data.

    Notes
    -----
    This function computes the cosine similarity.

    Cosine similarity is normalized, so this function will give the same
    result if computed on raw counts, or normalized data.

    The implementation is adapted from here: https://stackoverflow.com/a/20687984
    """

    # If computing across columns, transpose data
    data = data.T if dim == 'B' else data

    # Calculate similarity
    similarity = np.dot(data, data.T)

    # Calculate inverse squared magnitude & replace infs to zero
    inv_square_mag = 1 / np.diag(similarity)
    inv_square_mag[np.isinf(inv_square_mag)] = 0

    # Calculate inverse of the magnitude
    inv_mag = np.sqrt(inv_square_mag)

    # Calculate cosine similarity as element-wise multiplication by inverse magnitude
    cosine = similarity * inv_mag
    cosine = cosine.T * inv_mag

    # If data was transposed for computation, transpose back
    data = data.T if dim == 'B' else data

    return cosine
