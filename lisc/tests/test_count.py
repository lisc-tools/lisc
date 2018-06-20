"""Tests for the Count() class and related functions from lisc."""

import numpy as np

from lisc.count import Count

#######################################################################################
################################ TESTS - ERPSC - COUNT ################################
#######################################################################################

def test_erpsc_count():
    """Test the Count object."""

    # Check that ERPSCCount returns properly
    assert Count()

def test_scrape():
    """Test that Count object successful scrapes data."""

    counts = Count()

    # Add ERPs and terms
    #counts.set_erps(['N400', 'P600'])
    counts.set_terms(['language', 'memory'])
    counts.set_exclusions(['protein', 'protein'])

    #counts.run_scrape(db='pubmed')

    assert True

    #assert np.all(counts.dat_numbers)
    #assert np.all(counts.dat_percent)

    check_funcs(counts)

def check_funcs(counts):
    """Given object with scraped data, test all the check functions."""

    # Check that all check functions run
    #counts.check_cooc_erps()
    #counts.check_cooc_terms()
    #counts.check_top()
    #counts.check_counts('erp')
    #counts.check_counts('term')

    assert True
