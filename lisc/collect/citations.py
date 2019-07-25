"""Collect citation data from OpenCitations."""

import json

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.urls.open_citations import OpenCitations

###################################################################################################
###################################################################################################

def collect_citations(dois, util='citations', logging=None, folder=None, verbose=False):
    """Scape OpenCitations for citation data.

    Parameters
    ----------
    dois : list of str
        DOIs to collect citation data for.
    util : {'citations', 'references'}
        Which utility to collect citation data with.
        The 'citations' utility collects the number of citations citing the specified DOI.
        The 'references' utility collects the number of references cited by the specified DOI.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    citations : dict
        The number of citations for each DOI.
    meta_data : MetaData() object
        Meta data about the data collection.
    """

    urls = OpenCitations()
    urls.build_url(util)

    meta_data = MetaData()
    req = Requester(wait_time=0.1, logging=logging, folder=folder)

    if verbose:
        print('Collecting citation data.')

    citations = {doi : get_citation_data(req, urls.get_url(util, [doi])) for doi in dois}

    meta_data.add_requester(req)

    return citations, meta_data


def get_citation_data(req, citation_url):
    """Extract the number of citations from a citations call.

    Parameters
    ----------
    req : Requester object
        Requester object to launch requests from.
    citation_url : str
        URL to collect citation data from.

    Returns
    -------
    n_citations : int
        The number of citations the article has received.
    """

    page = req.request_url(citation_url)
    n_citations = len(json.loads(page.content.decode('utf-8')))

    # If the return is empty, encode as None instead of zero
    #   This is because we don't want to treat missing data as 0 citations
    if n_citations == 0:
        n_citations = None

    return n_citations
