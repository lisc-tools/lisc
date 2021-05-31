"""Tests for lisc.requester.requester."""

import os
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

def test_throttle(treq):

    treq.time_last_req = time.time()
    treq.throttle()

def test_wait(treq):

    treq.wait(0.01)

def test_request_url(treq):

    web_page = treq.request_url('http://www.google.com')

    assert web_page

def test_logging(tdb):

    urls = ['http://www.google.com']

    req_1 = Requester(logging='print')
    req_2 = Requester(logging='store')
    req_3 = Requester(logging='file', directory=tdb)

    for url in urls:
        for req in [req_1, req_2, req_3]:
            req.request_url(url)
            req.close()
            req_dict = req.as_dict()

    assert req_2.log == ['http://www.google.com']
    assert os.path.exists(os.path.join(tdb.get_folder_path('logs'), 'requester_log.txt'))

def test_get_time(treq):

    assert treq._get_time()

def test_open(treq):

    treq.open()

    assert treq.is_active

def test_close(treq):

    treq.open()
    treq.close()

    assert not treq.is_active
