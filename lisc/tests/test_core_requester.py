"""Tests for Requestor functions and classes from lisc.core."""

import time

from lisc.core.requester import Requester

##################################################################################
##################################################################################
##################################################################################

def test_requester():
    """Test the Requester object returns properly."""

    assert Requester()

def test_check():
    """Test the check method."""

    req = Requester()
    req.check()

    assert True

def test_throttle():
    """Test the throttle method."""

    req = Requester()
    req.time_last_req = time.time()

    req.throttle()

    assert True

def test_wait():
    """Test the wait method."""

    req = Requester()

    req.wait(0.01)

    assert True

def test_get_url():
    """Test the get_url method."""

    req = Requester()

    web_page = req.get_url('http://www.google.com')

    assert web_page

def test_open():
    """Test the open method."""

    req = Requester()

    req.open()

    assert req.is_active

def test_close():
    """Test the close method."""

    req = Requester()

    req.open()
    req.close()

    assert not req.is_active
