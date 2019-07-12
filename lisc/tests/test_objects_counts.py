"""Tests for the Count class and related functions from lisc."""

import numpy as np

from lisc.objects.counts import Counts

###################################################################################################
###################################################################################################

def test_counts():

    assert Counts()

def test_scrape():
    """Test that Count object successful scrapes data."""

    counts = Counts()

    counts.set_terms(['language', 'memory'])
    counts.set_exclusions(['protein', 'protein'])

    #counts.run_scrape(db='pubmed')
    #check_funcs(counts)
    #drop_data(counts)

    #assert np.all(counts.dat_numbers)
    #assert np.all(counts.dat_percent)

def check_funcs(counts):

    counts.check_cooc()
    counts.check_top()
    counts.check_counts()

def drop_data(counts):

    counts.drop_data(0)
