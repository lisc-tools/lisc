"""Collect words data from EUtils."""

from bs4 import BeautifulSoup

from lisc.data.term import Term
from lisc.requester import Requester
from lisc.data.articles import Articles
from lisc.data.meta_data import MetaData
from lisc.collect.utils import mk_term
from lisc.collect.info import get_db_info
from lisc.collect.process import (extract, ids_to_str, process_ids, process_authors,
                                  process_words, process_keywords, process_pub_date)
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_words(terms, inclusions=[], exclusions=[], db='pubmed',
                  retmax=None, field='TIAB', usehistory=False, api_key=None,
                  save_and_clear=False, logging=None, directory=None, verbose=False):
    """Collect text data and metadata from EUtils using specified search term(s).

    Parameters
    ----------
    terms : list of list of str
        Search terms.
    inclusions : list of list of str, optional
        Inclusion words for search terms.
    exclusions : list of list of str, optional
        Exclusion words for search terms.
    db : str, optional, default: 'pubmed'
        Which database to access from EUtils.
    retmax : int, optional
        Maximum number of articles to return.
    field : str, optional, default: 'TIAB'
        Field to search for term within.
        Defaults to 'TIAB', which is Title/Abstract.
    usehistory : bool, optional, default: False
        Whether to use EUtils history, storing results on their server.
    api_key : str
        An API key for a NCBI account.
    save_and_clear : bool, optional, default: False
        Whether to save words data to disk per term as it goes, instead of holding in memory.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB object, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.

    Returns
    -------
    results : list of Articles object
        Results from collecting data for each term.
    meta_data : MetaData object
        Meta data from the data collection.

    Notes
    -----
    The collection does an exact word search for the term given.
    It then loops through all the articles found about that data.
    For each article, i pulls and saves out data (including title, abstract, authors, etc)
        It pulls data using the hierarchical tag structure that organizes the articles.
    """

    # Get EUtils URLS object, with desired settings, and build required utility URLs
    urls = EUtils(db=db, usehistory='y' if usehistory else 'n', retmax=retmax,
                  retmode='xml', field=field, api_key=api_key)
    urls.build_url('info', settings=['db'])
    urls.build_url('search', settings=['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_url('fetch', settings=['db', 'retmode'])

    # Initialize results, meta data & requester
    results = []
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated),
                    logging=logging, directory=directory)

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.get_url('info')))

    # Check inclusions & exclusions
    inclusions = inclusions if inclusions else [[]] * len(terms)
    exclusions = exclusions if exclusions else [[]] * len(terms)

    # Loop through all the terms
    for search, incl, excl in zip(terms, inclusions, exclusions):

        # Collect term information and make search term argument
        term = Term(search[0], search, incl, excl)
        term_arg = mk_term(term)

        if verbose:
            print('Collecting data for: ', term.label)

        # Initialize object to store data for current term articles
        cur_dat = Articles(term)

        # Request web page
        url = urls.get_url('search', settings={'term' : term_arg})
        page = req.request_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        if usehistory:

            # Get number of articles, and keys to use history
            count = int(page_soup.find('count').text)
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Loop through, collecting article data, using history
            ret_start_it = 0
            while ret_start_it < count:

                # Set the number of articles per iteration (the ret_max per call)
                #  This defaults to 100, but will set to less if fewer needed to reach retmax
                ret_end_it = min(100, int(retmax) - ret_start_it)

                # Get article page, collect data, update position
                url_settings = {'WebEnv' : web_env, 'query_key' : query_key,
                                'retstart' : str(ret_start_it), 'retmax' : str(ret_end_it)}
                art_url = urls.get_url('fetch', settings=url_settings)
                cur_dat = get_articles(req, art_url, cur_dat)
                ret_start_it += ret_end_it

                if ret_start_it >= int(retmax):
                    break

        # Without using history
        else:

            ids = page_soup.find_all('id')
            art_url = urls.get_url('fetch', settings={'id' : ids_to_str(ids)})
            cur_dat = get_articles(req, art_url, cur_dat)

        cur_dat._check_results()

        if save_and_clear:
            cur_dat.save_and_clear(directory=directory)
        results.append(cur_dat)

    meta_data.add_requester(req)

    return results, meta_data


def get_articles(req, art_url, cur_dat):
    """Collect information for each article found for a given term.

    Parameters
    ----------
    req : Requester object
        Requester object to launch requests from.
    art_url : str
        URL for the article to be collected.
    cur_dat : Articles object
        Object to add data to.

    Returns
    -------
    cur_dat : Articles object
        Object to store information for the current term.
    """

    # Get page of all articles
    art_page = req.request_url(art_url)
    art_page_soup = BeautifulSoup(art_page.content, "xml")
    articles = art_page_soup.findAll('PubmedArticle')

    # Loop through each article, extracting relevant information
    for art in articles:

        # Get ID of current article & extract and add info to data object
        new_id = process_ids(extract(art, 'ArticleId', 'all'), 'pubmed')
        cur_dat = extract_add_info(cur_dat, new_id, art)

    return cur_dat


def extract_add_info(cur_data, art_id, art):
    """Extract information from an article and add it to a data object.

    Parameters
    ----------
    cur_data : Articles object
        Object to store information for the current article.
    art_id : int
        ID of the new article.
    art : bs4.element.Tag object
        Extracted article.

    Returns
    -------
    cur_data : Articles object
        Object updated with data from the current article.
    """

    cur_data.add_data('ids', art_id)
    cur_data.add_data('titles', extract(art, 'ArticleTitle', 'str'))
    cur_data.add_data('authors', process_authors(extract(art, 'AuthorList', 'raw')))
    cur_data.add_data('journals', (extract(art, 'Title', 'str'),
                                   extract(art, 'ISOAbbreviation', 'str')))
    cur_data.add_data('words', process_words(extract(art, 'AbstractText', 'str')))
    cur_data.add_data('keywords', process_keywords(extract(art, 'Keyword', 'all')))
    cur_data.add_data('years', process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_data.add_data('dois', process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

    return cur_data
