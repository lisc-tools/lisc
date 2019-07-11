"""Scrape counts data from Pubmed."""

import numpy as np
from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.scrape.utils import extract
from lisc.urls.pubmed import URLS, get_wait_time

###################################################################################################
###################################################################################################

def scrape_counts(terms_lst_a, excls_lst_a=[], terms_lst_b=[], excls_lst_b=[],
                  db='pubmed', field='TIAB', api_key=None, verbose=False):
    """Scrape pubmed for word co-occurence.

    Parameters
    ----------
    terms_lst_a : list of list of str
        Search terms.
    excl_lst_a : list of list of str, optional
        Exclusion words for search terms.
    terms_lst_b : list of list of str, optional
        Secondary list of search terms.
    excl_lst_b : list of list of str, optional
        Exclusion words for secondary list of search terms.
    db : str, optional (default: 'pubmed')
        Which pubmed database to use.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    api_key : str
        An API key for a NCBI account.
    verbose : bool, optional (default: False)
        Whether to print out updates.

    Returns
    -------
    data_numbers : 2d array
        The numbers of papers found for each combination of terms.
    data_percent : 2d array
        The percentage of papers for each term that include the corresponding term.
    term_a_counts : 1d array
        Number of papers for each term.
    term_b_counts : 1d array
        Number of papers for each term, in the secondary list of terms.
    meta_data : dict
        Meta data from the scrape.

    Notes
    -----
    The scraping does an exact word search for two terms.

    The HTML page returned by the pubmed search includes a 'count' field.
    This field contains the number of papers with both terms. This is extracted.
    """

    # Get e-utils URLS object. Set retmax as 0, since not using UIDs for counts
    urls = URLS(db=db, retmax='0', field=field, retmode='xml', api_key=api_key)
    urls.build_url('info', ['db'])
    urls.build_url('search', ['db', 'retmax', 'retmode', 'field'])

    # Initialize meta data & requester
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated))

    # Sort out terms
    n_terms_a = len(terms_lst_a)
    if len(terms_lst_b) == 0:
        square = True
        terms_lst_b = terms_lst_a
        excls_lst_b = excls_lst_a
    else:
        square = False
    n_terms_b = len(terms_lst_b)

    # Check exclusions
    if not excls_lst_a:
        excls_lst_a = [[]] * n_terms_a
    if not excls_lst_b:
        excls_lst_b = [[]] * n_terms_b

    # Initialize count variables to the correct length
    term_a_counts = np.ones([n_terms_a], dtype=int) * -1
    term_b_counts = np.ones([n_terms_b], dtype=int) * -1

    # Initialize right size matrices to store data
    data_numbers = np.ones([n_terms_a, n_terms_b], dtype=int) * -1
    data_percent = np.ones([n_terms_a, n_terms_b]) * -1

    # Set diagonal to zero if square (term co-occurence with itself)
    if square:
        np.fill_diagonal(data_numbers, 0)
        np.fill_diagonal(data_percent, 0)

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.info))

    # Loop through each term (list-A)
    for a_ind, term_a in enumerate(terms_lst_a):

        if verbose:
            print('Running counts for: ', terms_lst_a[a_ind][0])

        # Get number of results for current term search
        url = urls.search + _mk(terms_lst_a[a_ind]) + \
              _mk(excls_lst_a[a_ind], 'NOT')
        term_a_counts[a_ind] = get_count(req, url)

        # Loop through each term (list-b)
        for b_ind, term_b in enumerate(terms_lst_b):

            # Skip scrapes of equivalent term combinations - if single term list
            #  This will skip the diaonal row, and any combinations already scraped
            if square and data_numbers[a_ind, b_ind] != -1:
                continue

            # Get number of results for just term search
            url = urls.search + _mk(terms_lst_b[b_ind]) + \
                _mk(excls_lst_b[b_ind], 'NOT')
            term_b_counts[b_ind] = get_count(req, url)

            # Make URL - Exact Term Version, using double quotes, & exclusions
            url = urls.search + _mk(terms_lst_a[a_ind]) + \
                    _mk(excls_lst_a[a_ind], 'NOT') + \
                    _mk(terms_lst_b[b_ind], 'AND') + \
                    _mk(excls_lst_b[b_ind], 'NOT')

            count = get_count(req, url)

            data_numbers[a_ind, b_ind] = count
            data_percent[a_ind, b_ind] = count / term_a_counts[a_ind]

            if square:
                data_numbers[b_ind, a_ind] = count
                data_percent[b_ind, a_ind] = count / term_b_counts[b_ind]

    meta_data.add_requester(req)

    return data_numbers, data_percent, term_a_counts, term_b_counts, meta_data


def get_count(req, url):
    """Get the count of how many articles listed on search results URL.

    Parameters
    ----------
    url : str
        URL to search with.

    Returns
    -------
    count : int
        Count of the number of articles found.
    """

    page = req.get_url(url)
    page_soup = BeautifulSoup(page.content, 'lxml')

    # Get all count tags
    counts = extract(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count
