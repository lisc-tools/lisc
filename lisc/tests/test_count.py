"""Tests for the Count class and related functions from lisc."""

import numpy as np

from lisc.count import Count

###################################################################################################
###################################################################################################

def test_count():

    assert Count()

def test_scrape():
    """Test that Count object successful scrapes data."""

    counts = Count()

    counts.set_terms(['language', 'memory'])
    counts.set_exclusions(['protein', 'protein'])

    #counts.run_scrape(db='pubmed')
    # check_funcs(counts)
    # drop_data(counts)

    assert True

    #assert np.all(counts.dat_numbers)
    #assert np.all(counts.dat_percent)


def check_funcs(counts):
    """Given object with scraped data, test all the check functions."""

    # Check that all check functions run
    counts.check_cooc()
    counts.check_top()
    counts.check_counts()

    assert True

def drop_data(counts):

    counts.drop_data(0)

    assert True
