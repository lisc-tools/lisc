"""Tests for the Words() class and related functions from lisc."""

from py.test import raises

import requests
#import bs4
from bs4 import BeautifulSoup

from lisc.data import Data
from lisc.words import Words

###################################################################################################
###################################### TESTS - ERPSC - WORDS ######################################
###################################################################################################

def test_words():
    """Test the Words object."""

    assert Words()

def test_get_item():
    """   """

    words = Words()

    # Test error for empty object
    with raises(IndexError):
        words['not a thing']

    words.add_results(Data('test', ['test']))

    # Test error for wrong key
    with raises(IndexError):
        words['wrong']

    # Test properly extracting item
    assert words['test']

def test_add_results():
    """Test the add_results method."""

    words = Words()

    words.add_results(Data(['test']))

    assert words.results





# def test_scrape_data_hist():
#     """Test the scrape_data method, using HTTP Post method."""

#     words = Words()

#     # Add ERPs and terms
#     #words.set_erps(['N180', 'P600'])
#     words.set_terms(['language', 'memory'])
#     words.set_exclusions(['protein', ''])

#     #words.scrape_data(db='pubmed', retmax='5', use_hist=True)

#     assert True
