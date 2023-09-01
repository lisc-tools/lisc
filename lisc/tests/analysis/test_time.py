"""Tests for lisc.analysis.time."""

from lisc.analysis.time import *

###################################################################################################
###################################################################################################

def test_get_counts_across_years(tcounts1d_data):

    results = {
        2000 : tcounts1d_data,
        2005 : tcounts1d_data,
    }

    labels, years, data = get_counts_across_years(results)
    assert isinstance(labels, list)
    assert isinstance(years, list)
    assert years == list(results.keys())
    assert isinstance(data, np.ndarray)
    assert data.shape == (tcounts1d_data.n_terms, len(years))
