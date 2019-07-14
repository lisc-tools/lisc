"""Tests for Requestor functions and classes."""

import time

from lisc.requester import Requester

###################################################################################################
###################################################################################################

def test_requester():

    assert Requester()

def test_as_dict(treq):

    req_dict = treq.as_dict()
    assert isinstance(req_dict, dict)

def test_set_wait_time(treq):

    treq.set_wait_time(1)
    assert treq.wait_time == 1

def test_check(treq):

    treq.check()
    assert True

def test_throttle(treq):

    treq.time_last_req = time.time()

    treq.throttle()
    assert True

def test_wait(treq):

    treq.wait(0.01)
    assert True

def test_request_url(treq):

    web_page = treq.request_url('http://www.google.com')
    assert web_page

def test_get_time(treq):

    assert treq.get_time()

def test_open(treq):

    treq.open()
    assert treq.is_active

def test_close(treq):

    treq.open()
    treq.close()
    assert not treq.is_active
