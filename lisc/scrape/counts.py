"""Scrape counts data from Pubmed."""

import numpy as np
from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.scrape.info import get_db_info
from lisc.scrape.utils import mk_term
from lisc.scrape.process import extract
from lisc.urls.pubmed import URLS, get_wait_time

###################################################################################################
###################################################################################################

def scrape_counts(terms_a, exclusions_a=[], terms_b=[], exclusions_b=[],
                  db='pubmed', field='TIAB', api_key=None, verbose=False):
    """Scrape pubmed for word co-occurence.

    Parameters
    ----------
    terms_a : list of list of str
        Search terms.
    exclusions_a : list of list of str, optional
        Exclusion words for search terms.
    terms_b : list of list of str, optional
        Secondary list of search terms.
    exclusions_b : list of list of str, optional
        Exclusion words for secondary list of search terms.
    db : str, optional, default: 'pubmed'
        Which pubmed database to use.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    api_key : str
        An API key for a NCBI account.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    data_numbers : 2d array
        The numbers of papers found for each combination of terms.
    data_percent : 2d array
        The percentage of papers for each term that include the corresponding term.
    a_counts : 1d array
        Number of papers for each term.
    b_counts : 1d array
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
    n_terms_a = len(terms_a)
    if len(terms_b) == 0:
        square = True
        terms_b = terms_a
        exclusions_b = exclusions_a
    else:
        square = False
    n_terms_b = len(terms_b)

    # Check exclusions
    if not exclusions_a:
        exclusions_a = [[]] * n_terms_a
    if not exclusions_b:
        exclusions_b = [[]] * n_terms_b

    # Initialize count variables to the correct length
    a_counts = np.ones([n_terms_a], dtype=int) * -1
    b_counts = np.ones([n_terms_b], dtype=int) * -1

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
    for a_ind, (term_a, excl_a) in enumerate(zip(terms_a, exclusions_a)):

        if verbose:
            print('Running counts for: ', term_a[0])

        # Get number of results for current term search
        url = urls.search + mk_term(term_a) + mk_term(excl_a, 'NOT')
        a_counts[a_ind] = get_count(req, url)

        # Loop through each term (list-b)
        for b_ind, (term_b, excl_b) in enumerate(zip(terms_b, exclusions_b)):

            # Skip scrapes of equivalent term combinations - if single term list
            #  This will skip the diaonal row, and any combinations already scraped
            if square and data_numbers[a_ind, b_ind] != -1:
                continue

            # Get number of results for just term search
            url = urls.search + mk_term(term_b) + mk_term(excl_b, 'NOT')
            b_counts[b_ind] = get_count(req, url)

            # Make URL - Exact Term Version, using double quotes, & exclusions
            url = urls.search + mk_term(term_a) + mk_term(excl_a, 'NOT') + \
                    mk_term(term_b, 'AND') + mk_term(excl_b, 'NOT')

            count = get_count(req, url)

            data_numbers[a_ind, b_ind] = count
            data_percent[a_ind, b_ind] = count / a_counts[a_ind]

            if square:
                data_numbers[b_ind, a_ind] = count
                data_percent[b_ind, a_ind] = count / b_counts[b_ind]

    meta_data.add_requester(req)

    return data_numbers, data_percent, a_counts, b_counts, meta_data


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

    counts = extract(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count
