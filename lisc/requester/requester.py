"""Object to handle URL requests."""

import os
import time

import requests

from lisc.core.db import check_folder
from lisc.core.io import check_ext

###################################################################################################
###################################################################################################

class Requester():
    """Object to handle URL requests.

    Attributes
    ----------
    is_active : bool
        Status of the requester, whether currently being used to make requests.
    n_requests : int
        Number of requests that have been completed.
    wait_time : float
        Amount of time to wait between requests, in seconds.
    start_time : str
        Time when request session started.
    end_time : str
        Time when request session ended.
    time_last_req : float
        Time at which last request was sent.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    log : None or list or file object
        Object to log requested URLs, format depends on `logging`.
    """

    def __init__(self, wait_time=0., logging=None, folder=None):
        """Initialize a requester object.

        Parameters
        ----------
        wait_time : float, optional, default: 0.
            Amount of time to wait between requests, in seconds.
        logging : {None, 'print', 'store', 'file'}, optional
            What kind of logging, if any, to do for requested URLs.
        folder : SCDB or str or None
            A string or object containing a file path.
        """

        self.is_active = bool()
        self.n_requests = int()

        self.wait_time = int()

        self.start_time = str()
        self.end_time = str()

        self.time_last_req = float()

        # Set object as active
        self.set_wait_time(wait_time)
        self.open()

        # Set up for any logging
        self.logging, self.log = self._set_up_logging(logging, folder)


    def __repr__(self):
        return str(self.__dict__)


    def as_dict(self):
        """Get the attributes of the Requester object as a dictionary."""

        req_dict = self.__dict__
        req_dict.pop('time_last_req')

        return req_dict


    def set_wait_time(self, wait_time):
        """Set the amount of time to rest between requests.

        Parameters
        ----------
        wait_time : float
            Time, in seconds, to wait between launching URL requests.
        """

        self.wait_time = wait_time


    def check(self):
        """Print out basic check of requester object."""

        print('Requester object is active: \t', str(self.is_active))
        print('Number of requests sent: \t', str(self.n_requests))
        print('Requester opened: \t\t', str(self.start_time))
        print('Requester closed: \t\t', str(self.end_time))


    def throttle(self):
        """Slow down rate of requests by waiting if a new request is initiated too soon."""

        # Check how long it has been since last request was sent
        time_since_req = time.time() - self.time_last_req

        # If last request was too recent, pause
        if time_since_req < self.wait_time:
            self.wait(self.wait_time - time_since_req)


    @staticmethod
    def wait(wait_time):
        """Pause for specified amount of  time.

        Parameters
        ----------
        wait_time : float
            Time, in seconds, to wait between launching URL requests.
        """

        time.sleep(wait_time)


    def request_url(self, url):
        """Request a URL.

        Parameters
        ----------
        url : str
            Web address to request.

        Returns
        -------
        out : requests.models.Response() object
            Object containing the requested web page.
        """

        # Check if current object is active
        if not self.is_active:
            raise ValueError('Requester object is not active.')

        # Check and throttle, if required,
        self.throttle()

        # Log and request the URL
        self._log_url(url)
        out = requests.get(url)

        # Update data on requests
        self.time_last_req = time.time()
        self.n_requests += 1

        return out


    def open(self):
        """Set the current object as active."""

        self.start_time = self._get_time()
        self.is_active = True


    def close(self):
        """Set the current object as inactive."""

        self.end_time = self._get_time()
        self.is_active = False

        if self.logging == 'file':
            self.log.write('\nREQUESTER LOG - CLOSED AT:  ' + self.end_time)
            self.log.close()


    def _set_up_logging(self, logging, folder):
        """Set up for URL logging.

        Parameters
        ----------
        logging : {None, 'print', 'store', 'file'}
            What kind of logging, if any, to do for requested URLs.
        folder : SCDB or str or None
            A string or object containing a file path.
        """

        if logging in [None, 'print']:
            log = None

        elif logging == 'store':
            log = []

        elif logging == 'file':
            log = open(os.path.join(check_folder(folder, 'logs'),
                                    check_ext('requester_log', '.txt')), 'w')
            log.write('REQUESTER LOG - STARTED AT:  ' + self.start_time)

        else:
            raise ValueError('Logging type not understood.')

        return logging, log


    def _log_url(self, url):
        """Log a URL that is to be requested.

        Parameters
        ----------
        url : str
            URL to log.
        """

        if self.logging == 'print':
            print(url)

        elif self.logging == 'store':
            self.log.append(url)

        elif self.logging == 'file':
            self.log.write('\n' + url)


    @staticmethod
    def _get_time():
        """Get the current time.

        Returns
        -------
        str
            Current date & time.
        """

        return time.strftime('%H:%M:%S %A %d %B %Y')
