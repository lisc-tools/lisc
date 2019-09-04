"""Tests for the module utilities from lisc.core."""

from py.test import raises

from lisc.core.modutils import *

###################################################################################################
###################################################################################################

def test_dependency():

    dep = Dependency('test_module')

    with raises(ImportError):
        dep.method_call
