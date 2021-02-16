"""Tests for lisc.data.term."""

from lisc.data.term import *

###################################################################################################
###################################################################################################

def test_term():

    label = 'label'
    search = ['test', 'synonym']
    inclusions = ['incl', 'incl_synonym']
    exclusions = ['excl', 'excl_synonym']

    term1 = Term(label, search, inclusions, exclusions)
    assert term1.label == label
    assert term1.search == search
    assert term1.inclusions == inclusions
    assert term1.exclusions == exclusions

    term2 = Term(label, search, [], [])
    assert term2.inclusions == []
    assert term2.exclusions == []
