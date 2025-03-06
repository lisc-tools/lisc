"""Tests for the lisc.modutils.decorators."""

from lisc.modutils.decorators import *

###################################################################################################
###################################################################################################

def test_catch_none_one():

    @catch_none(1)
    def test_1(inp):
        return inp + 1

    assert test_1(1) == 2
    assert test_1(None) is None

def test_catch_none_two():

    @catch_none(2)
    def test_2(inp):
        return inp + 1

    assert test_2(1) == 2
    assert test_2(None) == (None, None)
