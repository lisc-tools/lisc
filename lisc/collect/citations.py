"""Collect citation data from OpenCitations."""

import json

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.urls.open_citations import OpenCitations

###################################################################################################
###################################################################################################

def collect_citations(dois, util='citations', logging=None, directory=None, verbose=False):
    """Collect citation data from OpenCitations.

    Parameters
    ----------
    dois : list of str
        DOIs to collect citation data for.
    util : {'citations', 'references'}
        Which utility to collect citation data with. Options:

        * 'citations': collects the number of citations citing the specified DOI.
        * 'references': collects the number of references cited by the specified DOI.
    logging : {None, 'print', 'store', 'file'}, optional
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    citations : dict
        The number of citations for each DOI.
    meta_data : MetaData
        Meta data about the data collection.
    """

    urls = OpenCitations()
    urls.build_url(util)

    meta_data = MetaData()
    req = Requester(wait_time=0.1, logging=logging, directory=directory)

    if verbose:
        print('Collecting citation data.')

    citations = {doi : get_citation_data(req, urls.get_url(util, [doi])) for doi in dois}

    meta_data.add_requester(req)

    return citations, meta_data


def get_citation_data(req, citation_url):
    """Extract the number of citations from an OpenCitations URL request.

    Parameters
    ----------
    req : Requester
        Requester to launch requests from.
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


def collect_citation_dois(dois, util='citations', logging=None, directory=None, verbose=False):
    """Collect a list of DOIs citing the target(s) using OpenCitations.

    Parameters
    ----------
    dois : list of str
        DOIs to collect citation data for.
    util : {'citations', 'references'}
        Which utility to collect citation data with. Options:

        * 'citations': collects the number of citations citing the specified DOI.
        * 'references': collects the number of references cited by the specified DOI.
    logging : {None, 'print', 'store', 'file'}, optional
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    citations : dict
        The number of citations for each DOI.
    meta_data : MetaData
        Meta data about the data collection.
    """

    urls = OpenCitations()
    urls.build_url(util)

    meta_data = MetaData()
    req = Requester(wait_time=0.1, logging=logging, directory=directory)

    if verbose:
        print('Collecting citation data.')

    citations = {doi : get_citation_doi_data(req, urls.get_url(util, [doi])) for doi in dois}

    meta_data.add_requester(req)

    return citations, meta_data


def get_citation_doi_data(req, citation_url):
    """Extract the number of citations from an OpenCitations URL request.

    Parameters
    ----------
    req : Requester
        Requester to launch requests from.
    citation_url : str
        URL to collect citation data from.

    Returns
    -------
   citations : list of strings
        The DOIs of articles citing the target article.
    """

    page = req.request_url(citation_url)
    jpage = json.loads(page.content.decode('utf-8'))
    n_citations = len(jpage)

    # If the return is empty, encode as None instead of zero
    #   This is because we don't want to treat missing data as 0 citations
    if n_citations == 0:
        citations = None
    else:
        citations = [ acite['citing'] for acite in jpage]

    return citations


