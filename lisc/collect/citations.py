"""Collect citation data from OpenCitations."""

import json

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.urls.open_citations import OpenCitations

###################################################################################################
###################################################################################################

def collect_citations(dois, util='citations', collect_dois=False,
                      logging=None, directory=None, verbose=False):
    """Collect citation data from OpenCitations.

    Parameters
    ----------
    dois : list of str
        DOIs to collect citation data for.
    util : {'citations', 'references'}
        Which utility to collect citation data with. Options:

        * 'citations': collects the number of citations citing the specified DOI.
        * 'references': collects the number of references cited by the specified DOI.
    collect_dois : bool, optional, default: False
        Whether to also collect the list of DOIs of cited or referenced papers.
    logging : {None, 'print', 'store', 'file'}, optional
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    n_citations : dict
        The number of citations or references for each article.
    cite_dois : dict
        The DOIs of the citing or references articles.
        Only returned if `collect_dois` is True.
    meta_data : MetaData
        Meta data about the data collection.

    Examples
    --------
    Collect citation data for a specified article:

    >>> citations, meta_data = collect_citations(['10.1038/nmeth.1635'])
    """

    # Get OpenCitations URLs object
    urls = OpenCitations()
    urls.build_url(util)

    # Initialize meta data object
    meta_data = MetaData()

    # Check for a Requester object to be passed in as logging, otherwise initialize
    req = logging if isinstance(logging, Requester) else \
        Requester(wait_time=0.1, logging=logging, directory=directory)

    if verbose:
        print('Collecting citation data.')

    # Initialize dictionaries to store collected data
    n_citations = {}
    cite_dois = {}

    for doi in dois:

        # Make the URL request for each DOI, and collect results
        outputs = get_citation_data(req, urls.get_url(util, [doi]), collect_dois)

        # Unpack outputs depending on wether DOIs were collected
        n_citations[doi], cite_dois[doi] = outputs if collect_dois else (outputs, None)

    meta_data.add_requester(req)

    if not collect_dois:
        return n_citations, meta_data
    else:
        return n_citations, cite_dois, meta_data


def get_citation_data(req, citation_url, collect_dois=False):
    """Extract citations using an OpenCitations URL request.

    Parameters
    ----------
    req : Requester
        Requester to launch requests from.
    citation_url : str
        URL to collect citation data from.
    collect_dois : bool, optional, default: False
        Whether to also collect the list of DOIs of cited or referenced papers.

    Returns
    -------
    n_citations : int
        The number of citations or references of the article.
    citing_dois : list of str
        The DOIs of the citing or references articles.
        Only returned if `collect_dois` is True.
    """

    page = req.request_url(citation_url)
    jpage = json.loads(page.content.decode('utf-8'))
    n_citations = len(jpage)

    if collect_dois:

        # Set which tag to extract, based on whether URL is for 'citations' or 'references'
        cite_tag = 'citing' if 'citations' in citation_url else 'cited'

        # Extract and collect the DOI for each citing or referenced article
        citing_dois = [art_cite[cite_tag] for art_cite in jpage]

    # If the DOI is not found, the return is empty is empty (length of zero)
    #   Therefore, re-encode outputs to None, to not treat missing entries as 0 cites / refs
    if n_citations == 0:
        n_citations = None
        citing_dois = None

    if not collect_dois:
        return n_citations
    else:
        return n_citations, citing_dois
