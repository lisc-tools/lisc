"""Tests for citations collections."""

from lisc.collect.citations import *

###################################################################################################
###################################################################################################

def test_collect_citations():

    dois = ['10.1007/s00228-017-2226-2', '10.1186/1756-8722-6-59']

    citations = collect_citations(dois, 'citations')
    assert citations

    references = collect_citations(dois, 'references')
    assert references
