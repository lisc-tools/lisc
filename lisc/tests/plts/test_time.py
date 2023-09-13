"""Tests for the lisc.plts.time."""

from lisc.tests.tutils import plot_test, optional_test

from lisc.plts.time import *

###################################################################################################
###################################################################################################

@optional_test('matplotlib')
@plot_test
def test_plot_results_across_years(tcounts1d_data, tdb):

    results = {
        2000 : tcounts1d_data,
        2005 : tcounts1d_data,
    }

    plot_results_across_years(results,
                              file_name='test_results_across_years.pdf', directory=tdb)
