"""Scrape citations from OpenCitations."""

from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.urls.open_citations import OpenCitations

###################################################################################################
###################################################################################################

def scrape_citations(dois, logging=None, folder=None, verbose=False):
    """   """

    urls = OpenCitations()
    #urls.build_url('info', ['db'])

    # Wait time??
    req = Requester(wait_time=0.1, logging=logging, folder=folder)

    if verbose:
        print('Collecting citation data.')

    for doi in dois:
        get_citation_data(req, citation_url)

    return None


def get_citation_data(req, citation_url):
    """Calls EInfo to get info and status of db to be used for scraping.

    Parameters
    ----------
    req : Requester object
        Requester object to launch requests from.
    citation_url : str
        URL to collect citation data from.

    Returns
    -------
    xx
        xx
    """

    # Get the info page and parse with BeautifulSoup
    citation_page = req.request_url(citation_url)


    # info_page_soup = BeautifulSoup(info_page.content, 'lxml')

    # # Set list of fields to extract from EInfo
    # fields = ['dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate']

    # # Extract basic infomation into a dictionary
    # db_info = dict()
    # for field in fields:
    #     db_info[field] = extract(info_page_soup, field, 'str')

    # return db_info
