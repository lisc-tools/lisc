"""Tests for Requestor functions and classes."""

import time

from lisc.requester import Requester

###################################################################################################
###################################################################################################

# TODO: UPDATE TO USE A TEST OBJECT REQUESTOR

def test_requester():

    assert Requester()

def test_set_wait_time():

    req = Requester()

    req.set_wait_time(1)
    assert req.wait_time == 1

def test_check():

    req = Requester()
    req.check()

    assert True

def test_throttle():

    req = Requester()
    req.time_last_req = time.time()

    req.throttle()
    assert True

def test_wait():

    req = Requester()

    req.wait(0.01)
    assert True

def test_request_url():

    req = Requester()

    web_page = req.request_url('http://www.google.com')
    assert web_page

def test_open():

    req = Requester()

    req.open()
    assert req.is_active

def test_close():

    req = Requester()

    req.open()
    req.close()
    assert not req.is_active
