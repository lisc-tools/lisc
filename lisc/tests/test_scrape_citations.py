"""Tests for scrape citations."""

from lisc.scrape.citations import *

###################################################################################################
###################################################################################################

def test_scrape_citations():

    dois = ['10.1007/s00228-017-2226-2', '10.1186/1756-8722-6-59']
    citations = scrape_citations(dois)

    assert citations
