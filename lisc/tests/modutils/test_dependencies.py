"""Tests for the lisc.modutils.dependencies."""

from inspect import ismodule

from pytest import raises

from lisc.modutils.dependencies import *

###################################################################################################
###################################################################################################

def test_dependency():

    dep = Dependency('test_module')

    with raises(ImportError):
        dep.method_call

def test_safe_import():

	# Check an import that should work
	imp = safe_import('numpy')
	assert ismodule(imp)

	# Check an import that should fail
	imp = safe_import('bad')
	assert not ismodule(imp)
	assert isinstance(imp, Dependency)
