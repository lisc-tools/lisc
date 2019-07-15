"""Scrape counts data from Pubmed."""

import numpy as np
from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.scrape.info import get_db_info
from lisc.scrape.utils import mk_term, join
from lisc.scrape.process import extract
from lisc.urls.pubmed import URLS, get_wait_time

###################################################################################################
###################################################################################################

def scrape_counts(terms_a, exclusions_a=[], terms_b=[], exclusions_b=[], db='pubmed',
                  field='TIAB', api_key=None, logging=None, folder=None, verbose=False):
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
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    data_numbers : 2d array
        The numbers of papers found for each combination of terms.
    counts : 1d array or list of 1d array
        Number of papers for each term independently.
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
    req = Requester(wait_time=get_wait_time(urls.authenticated),
                    logging=logging, folder=folder)

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
    counts_a = np.ones([n_terms_a], dtype=int) * -1
    counts_b = np.ones([n_terms_b], dtype=int) * -1

    # Initialize right size matrices to store data
    data_numbers = np.ones([n_terms_a, n_terms_b], dtype=int) * -1

    # Set diagonal to zero if square (term co-occurence with itself)
    if square:
        np.fill_diagonal(data_numbers, 0)

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.info))

    # Loop through each term (list-A)
    for a_ind, (term_a, excl_a) in enumerate(zip(terms_a, exclusions_a)):

        if verbose:
            print('Running counts for: ', term_a[0])

        # Make term arguments
        term_a_arg = join(mk_term(term_a), mk_term(excl_a), 'NOT')

        # Get number of results for current term search
        url = urls.get_url('search', {'term' : term_a_arg})
        counts_a[a_ind] = get_count(req, url)

        for b_ind, (term_b, excl_b) in enumerate(zip(terms_b, exclusions_b)):

            # Skip scrapes of equivalent term combinations - if single term list
            #  This will skip the diagonal row, and any combinations already scraped
            if square and data_numbers[a_ind, b_ind] != -1:
                continue

            # Make term arguments
            term_b_arg = join(mk_term(term_b), mk_term(excl_b), 'NOT')
            full_term_arg = join(term_a_arg, term_b_arg, 'AND')

            # Get number of results for current term search
            if not square:
                url = urls.get_url('search', {'term' : term_b_arg})
                counts_b[b_ind] = get_count(req, url)

            # Get number of results for combination of terms
            url = urls.get_url('search', {'term' : full_term_arg})
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

    page = req.request_url(url)
    page_soup = BeautifulSoup(page.content, 'lxml')

    counts = extract(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count
