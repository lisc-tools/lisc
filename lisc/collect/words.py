"""Collect words data from EUtils."""

from bs4 import BeautifulSoup

from lisc.data.term import Term
from lisc.requester import Requester
from lisc.data.articles import Articles
from lisc.data.meta_data import MetaData
from lisc.collect.utils import mk_term
from lisc.collect.info import get_db_info
from lisc.collect.process import get_info, extract_tag, ids_to_str
from lisc.collect.process import process_ids, process_authors, process_pub_date
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_words(terms, inclusions=None, exclusions=None, db='pubmed', retmax=None,
                  field='TIAB', usehistory=False, api_key=None, save_and_clear=False,
                  logging=None, directory=None, verbose=False, **eutils_kwargs):
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
    api_key : str, optional
        An API key for a NCBI account.
    save_and_clear : bool, optional, default: False
        Whether to save words data to disk per term as it goes, instead of holding in memory.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    directory : str or SCDB, optional
        Folder or database object specifying the save location.
    verbose : bool, optional, default: False
        Whether to print out updates.
    **eutils_kwargs
        Additional settings for the EUtils API.

    Returns
    -------
    results : list of Articles
        Results from collecting data for each term.
    meta_data : MetaData
        Meta data from the data collection.

    Notes
    -----
    The collection does an exact word search for the term given. It then loops through all
    the articles found for that term.

    For each article, it pulls and saves out data (including title, abstract, authors, etc),
    using the hierarchical tag structure that organizes the articles.

    Examples
    --------
    Collect words data for two terms, limiting the results to 5 articles per term:

    >>> results, meta_data = collect_words([['frontal lobe'], ['temporal lobe']], retmax=5)
    """

    # Get EUtils URLS object, with desired settings, and build required utility URLs
    urls = EUtils(db=db, retmax=retmax, usehistory='y' if usehistory else 'n',
                  field=field, retmode='xml', **eutils_kwargs, api_key=api_key)
    urls.build_url('info', settings=['db'])
    search_settings = ['db', 'usehistory', 'retmax', 'retmode', 'field']
    urls.build_url('search', settings=search_settings + list(eutils_kwargs.keys()))
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
        arts = Articles(term)

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
                arts = get_articles(req, art_url, arts)
                ret_start_it += ret_end_it

                if ret_start_it >= int(retmax):
                    break

        # Without using history
        else:

            ids = page_soup.find_all('id')
            art_url = urls.get_url('fetch', settings={'id' : ids_to_str(ids)})
            arts = get_articles(req, art_url, arts)

        arts._check_results()

        if save_and_clear:
            arts.save_and_clear(directory=directory)
        results.append(arts)

    meta_data.add_requester(req)

    return results, meta_data


def get_articles(req, url, arts):
    """Collect information for each article found for a given term.

    Parameters
    ----------
    req : Requester
        Requester object to launch requests from.
    url : str
        URL for the article to be collected.
    arts : Articles
        Object to add data to.

    Returns
    -------
    arts : Articles
        Object to store information for the current term.
    """

    # Get page of all articles
    page = req.request_url(url)
    page_soup = BeautifulSoup(page.content, 'xml')

    # Extract a list of all articles on the page
    articles = page_soup.findAll('PubmedArticle')

    # Loop through each article, extracting and collecting information from it
    for article in articles:
        arts = extract_add_info(arts, article)

    return arts


def extract_add_info(arts, article):
    """Extract information from an article and add it to a data object.

    Parameters
    ----------
    arts : Articles
        Object to store information for the current article.
    article : bs4.element.Tag
        Extracted article.

    Returns
    -------
    arts : Articles
        Object updated with data from the current article.
    """

    # Extract reference list, if present
    #   Otherwise, tags within this can interfere with collected data
    refs = extract_tag(article, 'ReferenceList')

    arts.add_data('ids', process_ids(get_info(article, 'ArticleId', 'all'), 'pubmed'))
    arts.add_data('titles', get_info(article, 'ArticleTitle', 'str'))
    arts.add_data('authors', process_authors(get_info(article, 'AuthorList', 'raw')))
    arts.add_data('journals', (get_info(article, 'Title', 'str'),
                               get_info(article, 'ISOAbbreviation', 'str')))
    arts.add_data('words', get_info(article, 'AbstractText', 'all-str'))
    arts.add_data('keywords', get_info(article, 'Keyword', 'all-list'))
    arts.add_data('years', process_pub_date(get_info(article, 'PubDate', 'raw')))
    arts.add_data('dois', process_ids(get_info(article, 'ArticleId', 'all'), 'doi'))

    return arts
