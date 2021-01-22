"""Tests for lisc.urls.open_citations."""

from lisc.urls.open_citations import *

###################################################################################################
###################################################################################################

def test_open_citations():

    assert OpenCitations()

def test_build_url():

    urls = OpenCitations()

    urls.build_url('citations')
    assert urls.utils['citations']

    urls.build_url('references')
    assert urls.utils['references']

    urls.build_url('metadata')
    assert urls.utils['metadata']

def test_get_url():

    urls = OpenCitations()

    urls.build_url('citations')
    citations = urls.get_url('citations', ['10.1007/s00228-017-2226-2'])

    assert '10.1007' in citations
