"""Tests for info collections."""

from lisc.collect.info import *

###################################################################################################
###################################################################################################

def test_collect_info():

    info = collect_info(db='pubmed')
    assert info
