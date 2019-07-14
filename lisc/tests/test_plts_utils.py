"""Tests for the plot utilities from lisc."""

from py.test import raises

from lisc.tests.utils import optional_test

from lisc.plts.utils import *

###################################################################################################
###################################################################################################

@optional_test('seaborn')
def test_get_cmap():

    assert get_cmap('purple')
    assert get_cmap('blue')

    with raises(ValueError):
        get_cmap('Not a thing.')
