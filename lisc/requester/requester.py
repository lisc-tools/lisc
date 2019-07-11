"""Object to handle URL requests."""

import time
import requests

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
    st_time : str
        Time when request session started.
    en_time : str
        Time when request session ended.
    time_last_req : float
        Time at which last request was sent.
    """

    def __init__(self, wait_time=0):

        self.is_active = bool()
        self.n_requests = int()

        self.wait_time = int()

        self.st_time = str()
        self.en_time = str()

        self.time_last_req = float()

        # Set object as active
        self.set_wait_time(wait_time)
        self.open()


    def __repr__(self):
        return str(self.__dict__)


    def as_dict(self):
        """Get the attributes of the Requester object as a dictionary."""

        req_dict = self.__dict__
        req_dict.pop('time_last_req')

        return req_dict

    def set_wait_time(self, wait_time):
        """Set the amount of time to rest between requests."""

        self.wait_time = wait_time


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
        if time_since_req < self.wait_time:
            self.wait(self.wait_time - time_since_req)


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

        # Check if current object is active
        if not self.is_active:
            raise ValueError('Requester object is not active.')

        # Check and throttle, if required
        self.throttle()

        # HACK LOGGING
        #print(url)

        # Get the requested URL
        out = requests.get(url)

        # Update data on requests
        self.time_last_req = time.time()
        self.n_requests += 1

        return out


    @staticmethod
    def get_time():
        """Get the current time."""

        return time.strftime('%H:%M %A %d %B %Y')


    def open(self):
        """Set the current object as active."""

        self.st_time = self.get_time()
        self.is_active = True


    def close(self):
        """Set the current object as inactive."""

        self.en_time = self.get_time()
        self.is_active = False
