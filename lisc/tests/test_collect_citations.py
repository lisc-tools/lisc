"""Tests for citations collections."""

from lisc.collect.citations import *

###################################################################################################
###################################################################################################

def test_collect_citations():

    dois = ['10.1007/s00228-017-2226-2', '10.1186/1756-8722-6-59']

    # Test 'citations' collection
    n_citations, cite_dois, meta_data = collect_citations(dois, 'citations', collect_dois=True)
    assert len(n_citations) == len(cite_dois) == len(dois)
    assert isinstance(list(n_citations.values())[0], int)
    assert isinstance(list(cite_dois.values())[0][0], str)

    # Test 'references' collection
    n_references, ref_dois, meta_data = collect_citations(dois, 'references', collect_dois=True)
    assert len(n_references) == len(ref_dois) == len(dois)
    assert isinstance(list(n_references.values())[0], int)
    assert isinstance(list(ref_dois.values())[0][0], str)
