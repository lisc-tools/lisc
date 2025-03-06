"""Collect counts data from EUtils."""

import numpy as np
from bs4 import BeautifulSoup

from lisc.requester import Requester
from lisc.data.term import Term
from lisc.data.meta_data import MetaData
from lisc.collect.info import get_db_info
from lisc.collect.terms import make_term, join
from lisc.collect.process import get_info
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_counts(terms_a, inclusions_a=None, exclusions_a=None, labels_a=None,
                   terms_b=None, inclusions_b=None, exclusions_b=None, labels_b=None,
                   db='pubmed', field='TIAB', api_key=None, collect_coocs=True,
                   logging=None, directory=None, collect_info=True, verbose=False,
                   **eutils_kwargs):
    """Collect count and term co-occurrence data from EUtils.

    Parameters
    ----------
    terms_a : list of list of str
        Search terms.
    inclusions_a : list of list of str, optional
        Inclusion words for search terms.
    exclusions_a : list of list of str, optional
        Exclusion words for search terms.
    labels_a : list of str, optional
        Labels for the search terms.
    terms_b : list of list of str, optional
        Secondary list of search terms.
    inclusions_b : list of list of str, optional
        Inclusion words for the second list of search terms.
    exclusions_b : list of list of str, optional
        Exclusion words for the second list of search terms.
    labels_b : list of str
        Labels for the second list of search terms.
    db : str, optional, default: 'pubmed'
        Which database to access from EUtils.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    api_key : str, optional
        An API key for a NCBI account.
    collect_coocs : bool, optional, default: True
        Whether to collect co-occurence data.
        If False, only collects the counts for first term list.
    logging : {None, 'print', 'store', 'file'}, optional
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.
    collect_info : bool, optional, default: True
        Whether to collect database information, to be added to meta data.
    verbose : bool, optional, default: False
        Whether to print out updates.
    **eutils_kwargs
        Additional settings for the EUtils API.

    Returns
    -------
    co_occurences : 2d array
        The numbers of articles found for each combination of terms.
        Only returned if `collect_coocs` is True.
    counts : 1d array or list of 1d array
        Number of articles for each term independently.
    meta_data : dict
        Meta data from the data collection.

    Notes
    -----
    The collection does an exact word search for search terms.

    The HTML page returned by the EUtils search includes a 'count' field.
    This field contains the number of articles with both terms. This is extracted.

    Examples
    --------
    Collect counts and co-occurrences for a single set of two search terms:

    >>> coocs, counts, meta_data = collect_counts([['frontal lobe'], ['temporal lobe']])

    Collect counts and co-occurrences for two sets of search terms:

    >>> coocs, counts, meta_data = collect_counts(terms_a=[['frontal lobe'], ['temporal lobe']],
    ...                                           terms_b=[['attention'], ['perception']])
    """

    # Initialize meta data object
    meta_data = MetaData()

    # Collect settings for URLs, and add them to the metadata object
    settings = {'db' : db, 'field' : field}
    settings.update(eutils_kwargs)
    meta_data.add_settings(settings)

    # Get e-utils URLS object. Set retmax as 0, since not using UIDs for counts
    urls = EUtils(**settings, retmax='0', retmode='xml', api_key=api_key)

    # Define the settings for the search utility, adding a default for datetype if not provided
    search_settings = ['db', 'retmax', 'retmode', 'field']
    if 'date' in ''.join(eutils_kwargs.keys()) and 'datetype' not in eutils_kwargs.keys():
        search_settings.append('datetype')

    # Build the URLs for the utilities that will be used
    urls.build_url('info', settings=['db'])
    urls.build_url('search', settings=search_settings + list(eutils_kwargs.keys()))

    # Check for a Requester object to be passed in as logging, otherwise initialize
    req = logging if isinstance(logging, Requester) else \
        Requester(wait_time=get_wait_time(urls.authenticated),
                  logging=logging, directory=directory)

    # Sort out terms for list a
    n_terms_a = len(terms_a)
    counts_a = np.ones([n_terms_a], dtype=int) * -1
    labels_a = labels_a if labels_a else [term[0] for term in terms_a]
    inclusions_a = [[]] * n_terms_a if not inclusions_a else inclusions_a
    exclusions_a = [[]] * n_terms_a if not exclusions_a else exclusions_a

    # If collecting co-occurences, sort out terms for list b and initialize co-occurence stores
    if collect_coocs:

        if not terms_b:
            square = True
            terms_b, inclusions_b, exclusions_b = terms_a, inclusions_a, exclusions_a
        else:
            square = False
        n_terms_b = len(terms_b)

        counts_b = np.ones([n_terms_b], dtype=int) * -1
        labels_b = labels_b if labels_b else [term[0] for term in terms_b]
        inclusions_b = [[]] * n_terms_b if not inclusions_b else inclusions_b
        exclusions_b = [[]] * n_terms_b if not exclusions_b else exclusions_b

        # Initialize matrices to store co-occurrence data
        co_occurences = np.ones([n_terms_a, n_terms_b], dtype=int) * -1

        # Set diagonal to zero if square (term co-occurrence with itself)
        if square:
            np.fill_diagonal(co_occurences, 0)

    # Get current information about database being used
    if collect_info:
        meta_data.add_db_info(get_db_info(req, urls.get_url('info')))

    # Loop through each term (list-A)
    for a_ind, (label_a, search_a, incl_a, excl_a) in \
        enumerate(zip(labels_a, terms_a, inclusions_a, exclusions_a)):

        # Make term arguments
        term_a = Term(label_a, search_a, incl_a, excl_a)
        term_a_arg = make_term(term_a)

        if verbose:
            print('Running counts for: ', term_a.label)

        # Get number of results for current term search
        url = urls.get_url('search', settings={'term' : term_a_arg})
        counts_a[a_ind] = get_count(req, url)

        if collect_coocs:

            # For each term in list a, loop through each term in list b
            for b_ind, (label_b, search_b, incl_b, excl_b) in \
                enumerate(zip(labels_b, terms_b, inclusions_b, exclusions_b)):

                # Skip collections of equivalent term combinations - if single term list
                #  This will skip the diagonal row, and any combinations already collected
                if square and co_occurences[a_ind, b_ind] != -1:
                    continue

                # Make term arguments
                term_b = Term(label_b, search_b, incl_b, excl_b)
                term_b_arg = make_term(term_b)
                full_term_arg = join(term_a_arg, term_b_arg, 'AND')

                # Get number of results for current term search
                if not square:
                    url = urls.get_url('search', settings={'term' : term_b_arg})
                    counts_b[b_ind] = get_count(req, url)

                # Get number of results for combination of terms
                url = urls.get_url('search', settings={'term' : full_term_arg})
                count = get_count(req, url)

                co_occurences[a_ind, b_ind] = count
                if square:
                    co_occurences[b_ind, a_ind] = count

    if collect_coocs:
        counts = counts_a if square else [counts_a, counts_b]
    else:
        counts = counts_a

    # If a requester was passed in, assume it is to contiune (don't close)
    meta_data.add_requester(req, close=not isinstance(logging, Requester))

    if not collect_coocs:
        return counts, meta_data
    else:
        return co_occurences, counts, meta_data


def get_count(req, url):
    """Get the count of how many articles listed at the requested URL.

    Parameters
    ----------
    req : Requester
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

    counts = get_info(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count
