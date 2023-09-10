"""Tests for lisc.objects.utils."""

from lisc.objects.utils import *

###################################################################################################
###################################################################################################

def test_check_object_type(tcounts1d, tcounts, twords):

    assert check_object_type(tcounts1d) == 'counts'
    assert check_object_type(tcounts) == 'counts'
    assert check_object_type(twords) == 'words'
