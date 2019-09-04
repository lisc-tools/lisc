"""Tests for the module utilities from lisc.core."""

###################################################################################################
###################################################################################################

def test_dependency():

    dep = Dependency('test_module')

    with raises(ImporttError):
        dep.method_call
