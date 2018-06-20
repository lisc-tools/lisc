"""Object to handle URL requests."""

import time
import requests

REST_TIME = 1/3

###################################################################################################
###################################################################################################

class Requester(object):
    """Object to handle URL requests.

    Attributes
    ----------
    is_active : bool
        Status of the requester, whether currently being used to make requests.
    n_requests : int
        Number of requests that have been completed.
    st_time : str
        Time when request session started.
    en_time : str
        Time when request session ended.
    time_last_req : float
        Time at which last request was sent.
    """

    def __init__(self):
        """Initialize Requester object."""

        self.is_active = False
        self.n_requests = int()

        self.st_time = time.strftime('%H:%M %A %d %B')
        self.en_time = str()

        self.time_last_req = float()


    def check(self):
        """Print out basic check of requester object."""

        print('Requester object is active: \t', str(self.is_active))
        print('Number of requests sent: \t', str(self.n_requests))
        print('Requester opened: \t\t', str(self.st_time))
        print('Requester closed: \t\t', str(self.en_time))


    def throttle(self):
        """Slow down rate of requests by waiting if a new request is initiated too soon."""

        # Check how long it has been since last request was sent
        time_since_req = time.time() - self.time_last_req

        # If last request was too recent, pause
        if time_since_req < REST_TIME:
            self.wait(REST_TIME - time_since_req)


    @staticmethod
    def wait(wait_time):
        """Pause for specified amount of  time.

        Parameters
        ----------
        wait_time : float
            Time, in seconds, to wait.
        """

        time.sleep(wait_time)


    def get_url(self, url):
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

        # Check if current object is active, and throttle is required
        if self.is_active:
            self.throttle()
        else:
            self.open()

        # Get the requested URL
        out = requests.get(url)

        # Update data on requests
        self.time_last_req = time.time()
        self.n_requests += 1

        return out


    def open(self):
        """Set the current object as active."""

        self.st_time = time.strftime('%H:%M %A %d %B')
        self.is_active = True


    def close(self):
        """Set the current object as inactive."""

        self.en_time = time.strftime('%H:%M %A %d %B')
        self.is_active = False
