"""Scraper functions for LISC.

Notes
-----
The wait time for requesting is set for the E-Utils API, which allows for:
- 10 requests/second for authenticated users (using an API key)
- 3 requests/second otherwise
"""

import datetime

import nltk
import numpy as np
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

from lisc.data import Data
from lisc.core.urls import URLS
from lisc.core.requester import Requester
from lisc.core.utils import comb_terms, extract, CatchNone, CatchNone2

###################################################################################################
###################################################################################################

def scrape_counts(terms_lst_a, excls_lst_a=[], terms_lst_b=[], excls_lst_b=[],
                  db='pubmed', field='TIAB', api_key=None, verbose=False):
    """Search through pubmed for all abstracts for co-occurence.

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
    dat_numbers : 2d array
        The numbers of papers found for each combination of terms.
    dat_percent : 2d array
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

    # Initialize meta data
    meta_data = dict()

    # Set date of when data was scraped
    meta_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Get e-utils URLS object. Set retmax as 0, since not using UIDs for counts
    urls = URLS(db=db, retmax='0', field=field, retmode='xml', api_key=api_key)
    urls.build_url('info', ['db'])
    urls.build_url('search', ['db', 'retmax', 'retmode', 'field'])

    # Initialize Requester object
    req = Requester()
    req.set_wait_time(1/10 if urls.authenticated else 1/3)

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
    dat_numbers = np.ones([n_terms_a, n_terms_b], dtype=int) * -1
    dat_percent = np.ones([n_terms_a, n_terms_b]) * -1

    # Set diagonal to zero if square (term co-occurence with itself)
    if square:
        np.fill_diagonal(dat_numbers, 0)
        np.fill_diagonal(dat_percent, 0)

    # Get current information about database being used
    meta_data['db_info'] = _get_db_info(req, urls.info)

    # Loop through each term (list-A)
    for a_ind, term_a in enumerate(terms_lst_a):

        if verbose:
            print('Running counts for: ', terms_lst_a[a_ind][0])

        # Get number of results for current term search
        url = urls.search + _mk(terms_lst_a[a_ind]) + \
              _mk(excls_lst_a[a_ind], 'NOT')
        term_a_counts[a_ind] = _get_count(req, url)

        # Loop through each term (list-b)
        for b_ind, term_b in enumerate(terms_lst_b):

            # Skip scrapes of equivalent term combinations - if single term list
            #  This will skip the diaonal row, and any combinations already scraped
            if square and dat_numbers[a_ind, b_ind] != -1:
                continue

            # Get number of results for just term search
            url = urls.search + _mk(terms_lst_b[b_ind]) + \
            	_mk(excls_lst_b[b_ind], 'NOT')
            term_b_counts[b_ind] = _get_count(req, url)

            # Make URL - Exact Term Version, using double quotes, & exclusions
            url = urls.search + _mk(terms_lst_a[a_ind]) + \
                    _mk(excls_lst_a[a_ind], 'NOT') + \
                    _mk(terms_lst_b[b_ind], 'AND') + \
                    _mk(excls_lst_b[b_ind], 'NOT')

            count = _get_count(req, url)

            dat_numbers[a_ind, b_ind] = count
            dat_percent[a_ind, b_ind] = count / term_a_counts[a_ind]

            if square:
                dat_numbers[b_ind, a_ind] = count
                dat_percent[b_ind, a_ind] = count / term_b_counts[b_ind]

    # Set Requester object as finished being used
    req.close()
    meta_data['req'] = req

    return dat_numbers, dat_percent, term_a_counts, term_b_counts, meta_data


def scrape_words(terms_lst, exclusions_lst=[], db='pubmed', retmax=None, field='TIAB',
                 api_key=None, use_hist=False, save_n_clear=True, verbose=False):
    """Search and scrape from pubmed for all abstracts referring to a given term.

    Parameters
    ----------
    terms_lst : list of list of str
        Search terms.
    exclusions_lst : list of list of str, optional
        Exclusion words for search terms.
    db : str, optional, default: 'pubmed'
        Which pubmed database to use.
    retmax : int, optional
        Maximum number of records to return.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    api_key : str
        An API key for a NCBI account.
    use_hist : bool, optional, default: False
        Use e-utilities history: storing results on their server, as needed.
    save_n_clear : bool, optional (default: False)
        Whether to save words data to disk per term as it goes, instead of holding in memory.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    results : list of lisc Data() objects
        Results from the scraping data for each term.
    meta_data : dict
        Meta data from the scrape.

    Notes
    -----
    The scraping does an exact word search for the term given.
    It then loops through all the articles found about that data.
    For each article, pulls and saves out data (including title, abstract, authors, etc)
        Pulls data using the hierarchical tag structure that organize the articles.
        This procedure loops through each article tag.
    """

    # Initialize results & meta data
    results = []
    meta_data = dict()

    # Set date of when data was collected
    meta_data['date'] = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    # Get e-utils URLS object
    hist_val = 'y' if use_hist else 'n'
    urls = URLS(db=db, usehistory=hist_val, retmax=retmax,
                retmode='xml', field=field, api_key=api_key)

    urls.build_url('info', ['db'])
    urls.build_url('search', ['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_url('fetch', ['db', 'retmode'])

    # Initialize Requester object
    req = Requester()
    req.set_wait_time(1/10 if urls.authenticated else 1/3)

    # Get current information about database being used
    meta_data['db_info'] = _get_db_info(req, urls.info)

    # Check exclusions
    if not exclusions_lst:
        exclusions_lst = [[] for i in range(len(terms_lst))]

    # Loop through all the terms
    for ind, terms in enumerate(terms_lst):

        if verbose:
            print('Scraping words for: ', terms[0])

        # Initiliaze object to store data for current term papers
        cur_dat = Data(terms[0], terms)

        # Set up search terms - add exclusions, if there are any
        if exclusions_lst[ind]:
            term_arg = comb_terms(terms, 'or') + comb_terms(exclusions_lst[ind], 'not')
        else:
            term_arg = comb_terms(terms, 'or')

        # Create the url for the search term
        url = urls.search + term_arg

        # Update history
        cur_dat.update_history('Start Scrape')

        # Get page and parse
        page = req.get_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        # Using history
        if use_hist:

            # Initialize to start at 0
            ret_start_it = 0

            # Get number of papers, and keys to use history
            count = int(page_soup.find('count').text)
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Loop through pulling paper data, using history
            while ret_start_it < count:

                # Set the number of papers per iteration (the ret_max per call)
                #  This defaults to 100, but will sets to less if fewer needed to reach retmax
                ret_end_it = min(100, int(retmax) - ret_start_it)

                # Get article page, scrape data, update position
                art_url = urls.fetch + '&WebEnv=' + web_env + '&query_key=' + query_key + \
                          '&retstart=' + str(ret_start_it) + '&retmax=' + str(ret_end_it)
                cur_dat = _scrape_papers(req, art_url, cur_dat)
                ret_start_it += ret_end_it

                # Stop if number of scraped papers has reached total retmax
                if ret_start_it >= int(retmax):
                    break

        # Without using history
        else:

            # Get all ids
            ids = page_soup.find_all('id')

            # Convert ids to string
            ids_str = _ids_to_str(ids)

            # Get article page & scrape data
            art_url = urls.fetch + '&id=' + ids_str
            cur_dat = _scrape_papers(req, art_url, cur_dat)

        # Check consistency of extracted results
        cur_dat.check_results()
        cur_dat.update_history('End Scrape')

        # Save out and clear data
        if save_n_clear:
            cur_dat.save_n_clear()
        results.append(cur_dat)

    # Set Requester object as finished being used
    req.close()
    meta_data['req'] = req

    return results, meta_data

###################################################################################################
###################################################################################################

def _get_db_info(req, info_url):
    """Calls EInfo to get info and status of db to be used for scraping.

    Parameters
    ----------
    req : Requester object
        Requester object to launch requests from.
    info_url : str
        URL to request db information from.

    Returns
    -------
    db_info : dict
        Database information.
    """

    # Get the info page and parse with BeautifulSoup
    info_page = req.get_url(info_url)
    info_page_soup = BeautifulSoup(info_page.content, 'lxml')

    # Set list of fields to extract from eInfo
    fields = ['dbname', 'menuname', 'description', 'dbbuild', 'count', 'lastupdate']

    # Extract basic infomation into a dictionary
    db_info = dict()
    for field in fields:
        db_info[field] = extract(info_page_soup, field, 'str')

    return db_info


def _scrape_papers(req, art_url, cur_dat):
    """Scrape information for each article found for a given term.

    Parameters
    ----------
    req : Requester() object
        Requester object to launch requests from.
    art_url : str
        URL for the article to be scraped.

    Returns
    -------
    cur_dat : Data() object
        Object to store information for the current term.
    """

    # Get page of all articles
    art_page = req.get_url(art_url)
    art_page_soup = BeautifulSoup(art_page.content, "xml")

    # Pull out articles
    articles = art_page_soup.findAll('PubmedArticle')

    # Loop through each article, extracting relevant information
    for ind, art in enumerate(articles):

        # Get ID of current article
        new_id = _process_ids(extract(art, 'ArticleId', 'all'), 'pubmed')

        # Extract and add all relevant info from current articles to Data object
        cur_dat = _extract_add_info(cur_dat, new_id, art)

    return cur_dat


def _get_count(req, url):
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

    # Request page from URL
    page = req.get_url(url)
    page_soup = BeautifulSoup(page.content, 'lxml')

    # Get all count tags
    counts = extract(page_soup, 'count', 'all')

    try:
        count = int(counts[0].text)
    except IndexError:
        count = 0

    return count


def _mk(t_lst, cm=''):
    """Create search term component.

    Parameters
    ----------
    t_lst : list of str
        List of words to connect together.
    cm : str
        Connector word to append to front of search term.

    Returns
    -------
    str
        Search term.
    """

    if t_lst and t_lst[0]:
        return cm + comb_terms(t_lst, 'or')
    else:
        return ''

###################################################################################################
###################################################################################################

def _extract_add_info(cur_dat, new_id, art):
    """Extract information from article web page and add to

    Parameters
    ----------
    cur_dat : Data() object
        Object to store information for the current term.
    new_id : int
        Paper ID of the new paper.
    art : bs4.element.Tag() object
        Extracted pubmed article.

    Returns
    -------
    cur_dat : Data() object
        Object to store data from the current term.

    NOTES
    -----
    Data extraction is all in try/except statements in order to
        deal with missing data, since fields may be missing.
    """

    # Add ID of current article
    cur_dat.add_id(new_id)
    cur_dat.add_title(extract(art, 'ArticleTitle', 'str'))
    cur_dat.add_authors(_process_authors(extract(art, 'AuthorList', 'raw')))
    cur_dat.add_journal(extract(art, 'Title', 'str'), extract(art, 'ISOAbbreviation', 'str'))
    cur_dat.add_words(_process_words(extract(art, 'AbstractText', 'str')))
    cur_dat.add_kws(_process_kws(extract(art, 'Keyword', 'all')))
    cur_dat.add_pub_date(_process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_dat.add_doi(_process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

    # Increment number of articles included in Data
    cur_dat.increment_n_articles()

    return cur_dat


def _ids_to_str(ids):
    """Takes a list of pubmed ids, returns a str of the ids separated by commas.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        List of pubmed ids.

    Returns
    -------
    ids_str : str
        A string of all concatenated ids.
    """

    # Check how many ids in list & initialize string with first id
    n_ids = len(ids)
    ids_str = str(ids[0].text)

    # Loop through rest of the id's, appending to end of id_str
    for ind in range(1, n_ids):
        ids_str = ids_str + ',' + str(ids[ind].text)

    return ids_str


@CatchNone
def _process_words(text):
    """Processes abstract text - sets to lower case, and removes stopwords and punctuation.

    Parameters
    ----------
    text : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of words, after processing.
    """

    # Tokenize input text
    words = nltk.word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation). Return the result.
    words_cleaned = [word.lower() for word in words if (
        (not word.lower() in stopwords.words('english')) & word.isalnum())]

    return words_cleaned


@CatchNone
def _process_kws(keywords):
    """Extract and process keywords data.

    Parameters
    ----------
    kws : bs4.element.ResultSet
        List of all the keyword tags.

    Returns
    -------
    list of str
        List of all the keywords.
    """

    return [kw.text.lower() for kw in keywords]


@CatchNone
def _process_authors(author_list):
    """Extract and process author data.

    Parameters
    ----------
    author_list : bs4.element.Tag
        AuthorList tag, which contains tags related to author data.

    Returns
    -------
    out : list of tuple of (str, str, str, str)
        List of authors, each as (LastName, FirstName, Initials, Affiliation).
    """

    # Pull out all author tags from the input
    authors = extract(author_list, 'Author', 'all')

    # Extract data for each author
    out = []
    for author in authors:
        out.append((extract(author, 'LastName', 'str'), extract(author, 'ForeName', 'str'),
                    extract(author, 'Initials', 'str'), extract(author, 'Affiliation', 'str')))

    return out


@CatchNone2
def _process_pub_date(pub_date):
    """Extract and process publication date data.

    Parameters
    ----------
    pub_date : bs4.element.Tag
        PubDate tag, which contains tags with publication date information.

    Returns
    -------
    year : int or None
        Year the article was published.
    month : str or None
        Month the article was published.
    """

    # Extract year, convert to int if not None
    year = extract(pub_date, 'Year', 'str')
    year = int(year) if year else year

    # Extract month
    month = extract(pub_date, 'Month', 'str')

    return year, month


@CatchNone
def _process_ids(ids, id_type):
    """Extract and process ID data.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        All the ArticleId tags, with all IDs for the article.

    Returns
    -------
    str or None
        The DOI if available, otherwise None.
    """

    lst = [str(id.contents[0]) for id in ids if id.attrs == {'IdType' : id_type}]

    return None if not lst else lst
