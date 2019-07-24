"""Tests for info collections."""

from lisc.collect.info import *

###################################################################################################
###################################################################################################

def test_collect_info():

    out = collect_info(db='pubmed')
    assert out
