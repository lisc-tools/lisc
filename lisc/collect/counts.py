"""Collect counts data from EUtils."""

import numpy as np
from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.data.term import Term
from lisc.data.meta_data import MetaData
from lisc.collect.info import get_db_info
from lisc.collect.utils import mk_term, join
from lisc.collect.process import extract
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_counts(terms_a, inclusions_a=[], exclusions_a=[],
                   terms_b=[], inclusions_b=[], exclusions_b=[],
                   db='pubmed', field='TIAB', api_key=None,
                   logging=None, directory=None, verbose=False):
    """Collect word co-occurrence data from EUtils.

    Parameters
    ----------
    terms_a : list of list of str
        Search terms.
    inclusions_a : list of list of str, optional
        Inclusions words for search terms.
    exclusions_a : list of list of str, optional
        Exclusion words for search terms.
    terms_b : list of list of str, optional
        Secondary list of search terms.
    inclusions_b : list of list of str, optional
        Inclusions words for secondary lis of search terms.
    exclusions_b : list of list of str, optional
        Exclusion words for secondary list of search terms.
    db : str, optional, default: 'pubmed'
        Which database to access from EUtils.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    api_key : str
        An API key for a NCBI account.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB object, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    data_numbers : 2d array
        The numbers of articles found for each combination of terms.
    counts : 1d array or list of 1d array
        Number of articles for each term independently.
    meta_data : dict
        Meta data from the data collection.

    Notes
    -----
    The collection does an exact word search for two terms.

    The HTML page returned by the EUtils search includes a 'count' field.
    This field contains the number of articles with both terms. This is extracted.
    """

    # Get e-utils URLS object. Set retmax as 0, since not using UIDs for counts
    urls = EUtils(db=db, retmax='0', field=field, retmode='xml', api_key=api_key)
    urls.build_url('info', settings=['db'])
    urls.build_url('search', settings=['db', 'retmax', 'retmode', 'field'])

    # Initialize meta data & requester
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated),
                    logging=logging, directory=directory)

    # Sort out terms
    n_terms_a = len(terms_a)
    if len(terms_b) == 0:
        square = True
        terms_b, inclusions_b, exclusions_b = terms_a, inclusions_a, exclusions_a
    else:
        square = False
    n_terms_b = len(terms_b)

    # Check inclusions & exclusions
    inclusions_a = [[]] * n_terms_a if not inclusions_a else inclusions_a
    inclusions_b = [[]] * n_terms_b if not inclusions_b else inclusions_b
    exclusions_a = [[]] * n_terms_a if not exclusions_a else exclusions_a
    exclusions_b = [[]] * n_terms_b if not exclusions_b else exclusions_b

    # Initialize count variables to the correct length
    counts_a = np.ones([n_terms_a], dtype=int) * -1
    counts_b = np.ones([n_terms_b], dtype=int) * -1

    # Initialize right size matrices to store data
    data_numbers = np.ones([n_terms_a, n_terms_b], dtype=int) * -1

    # Set diagonal to zero if square (term co-occurrence with itself)
    if square:
        np.fill_diagonal(data_numbers, 0)

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.get_url('info')))

    # Loop through each term (list-A)
    for a_ind, (search_a, incl_a, excl_a) in enumerate(zip(terms_a, inclusions_a, exclusions_a)):

        # Make term arguments
        term_a = Term(search_a[0], search_a, incl_a, excl_a)
        term_a_arg = mk_term(term_a)

        if verbose:
            print('Running counts for: ', term_a.label)

        # Get number of results for current term search
        url = urls.get_url('search', settings={'term' : term_a_arg})
        counts_a[a_ind] = get_count(req, url)

        # For each term in list a, loop through each term in list b
        for b_ind, (search_b, incl_b, excl_b) in enumerate(zip(terms_b, inclusions_b, exclusions_b)):

            # Skip collections of equivalent term combinations - if single term list
            #  This will skip the diagonal row, and any combinations already collected
            if square and data_numbers[a_ind, b_ind] != -1:
                continue

            # Make term arguments
            term_b = Term(search_b[0], search_b, incl_b, excl_b)
            term_b_arg = mk_term(term_b)
            full_term_arg = join(term_a_arg, term_b_arg, 'AND')

            # Get number of results for current term search
            if not square:
                url = urls.get_url('search', settings={'term' : term_b_arg})
                counts_b[b_ind] = get_count(req, url)

            # Get number of results for combination of terms
            url = urls.get_url('search', settings={'term' : full_term_arg})
            count = get_count(req, url)

            data_numbers[a_ind, b_ind] = count
            if square:
                data_numbers[b_ind, a_ind] = count

    if square:
        counts = counts_a
    else:
        counts = [counts_a, counts_b]

    meta_data.add_requester(req)

    return data_numbers, counts, meta_data


def get_count(req, url):
    """Get the count of how many articles listed at the requested URL.

    Parameters
    ----------
    req : Requester object
        Object to launch requests from.
    url : str
        URL to request count data from.

    Returns
    -------
    count : int
        Count of the number of articles found.
    """

    page = req.request_url(url)
    page_soup = BeautifulSoup(page.content, 'lxml')

    counts = extract(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count
