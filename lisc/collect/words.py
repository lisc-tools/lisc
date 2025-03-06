"""Collect words data from EUtils."""

from bs4 import BeautifulSoup

from lisc.data.term import Term
from lisc.requester import Requester
from lisc.data.articles import Articles
from lisc.data.meta_data import MetaData
from lisc.collect.terms import make_term
from lisc.collect.info import get_db_info
from lisc.collect.process import get_info, extract_tag
from lisc.collect.process import process_ids, process_authors, process_pub_date
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_words(terms, inclusions=None, exclusions=None, labels=None,
                  db='pubmed', retmax=100, field='TIAB', usehistory=False,
                  api_key=None, save_and_clear=False, logging=None, directory=None,
                  collect_info=True, verbose=False, **eutils_kwargs):
    """Collect text data and metadata from EUtils using specified search term(s).

    Parameters
    ----------
    terms : list of list of str
        Search terms.
    inclusions : list of list of str, optional
        Inclusion words for search terms.
    exclusions : list of list of str, optional
        Exclusion words for search terms.
    labels : list of str, optional
        Labels for the search terms.
    db : str, optional, default: 'pubmed'
        Which database to access from EUtils.
    retmax : int, optional, default: 100
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
    collect_info : bool, optional, default: True
        Whether to collect database information, to be added to meta data.
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

    # Check for valid database based on what words is set up to collect
    if db != 'pubmed':
        msg = 'Only the `pubmed` database is currently supported for words collection.'
        raise NotImplementedError(msg)

    # Initialize meta data object
    meta_data = MetaData()

    # Collect settings for URLs, and add them to the metadata object
    settings = {'db' : db, 'retmax' : retmax, 'field' : field,
                'usehistory' : 'y' if usehistory else 'n'}
    settings.update(eutils_kwargs)
    meta_data.add_settings(settings)

    # Get EUtils URLS object, with desired settings, and build required utility URLs
    urls = EUtils(**settings, retmode='xml', api_key=api_key)

    # Define the settings for the search utility, adding a default for datetype if not provided
    search_settings = ['db', 'usehistory', 'retmax', 'retmode', 'field']
    if 'date' in ''.join(eutils_kwargs.keys()) and 'datetype' not in eutils_kwargs.keys():
        search_settings.append('datetype')

    # Build the URLs for the utilities that will be used
    urls.build_url('info', settings=['db'])
    urls.build_url('search', settings=search_settings + list(eutils_kwargs.keys()))
    urls.build_url('fetch', settings=['db', 'retmode'])

    # Check for a Requester object to be passed in as logging, otherwise initialize
    req = logging if isinstance(logging, Requester) else \
        Requester(wait_time=get_wait_time(urls.authenticated),
                  logging=logging, directory=directory)

    # Get current information about database being used
    if collect_info:
        meta_data.add_db_info(get_db_info(req, urls.get_url('info')))

    # Check labels, inclusions & exclusions
    labels = labels if labels else [term[0] for term in terms]
    inclusions = inclusions if inclusions else [[]] * len(terms)
    exclusions = exclusions if exclusions else [[]] * len(terms)

    # Loop through all the terms, launch collection, and collect results
    results = []
    for label, search, incl, excl in zip(labels, terms, inclusions, exclusions):

        # Collect term information and make search term argument
        term = Term(label, search, incl, excl)
        term_arg = make_term(term)

        if verbose:
            print('Collecting data for: ', term.label)

        # Initialize object to store data for current term articles
        arts = Articles(term)

        # Request web page
        url = urls.get_url('search', settings={'term' : term_arg})
        page = req.request_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        # Get number of articles
        count = int(page_soup.find('count').text)

        # Collect articles, using history
        if usehistory:

            # Get the information from the page for using history
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Set default retmax per history iteration
            retmax_hist = 100

            # Loop through, using history to collect groups of articles at a time
            retstart_it = 0
            while retstart_it < count:

                # Set the retmax for the current iteration
                retmax_it = min(retmax-retstart_it, retmax_hist)

                # Get article page, collect data
                url_settings = {'WebEnv' : web_env, 'query_key' : query_key,
                                'retstart' : str(retstart_it), 'retmax' : str(retmax_it)}
                art_url = urls.get_url('fetch', settings=url_settings)
                arts = get_articles(req, art_url, arts)

                # Update position for counting, and break out if more than global retmax
                retstart_it += retmax_hist
                if retstart_it >= int(retmax):
                    break

        # Without using history
        else:

            ids = page_soup.find_all('id')
            ids_str = ','.join([el.text for el in ids])

            # Batch requested IDs into groups of 100 to avoid URL length limits
            for ind in range(0, len(ids_str), 100):
                art_url = urls.get_url('fetch', settings={'id' : ids_str[ind:ind+100]})
                arts = get_articles(req, art_url, arts)

        arts._check_results()

        if save_and_clear:
            arts.save_and_clear(directory=directory)
        results.append(arts)

    # If a requester was passed in, assume it is to contiune (don't close)
    meta_data.add_requester(req, close=not isinstance(logging, Requester))

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

    # Get a list of all articles on the page
    articles = page_soup.findAll('PubmedArticle')

    # Loop through each article, collecting information from it
    for article in articles:
        arts = get_article_info(arts, article)

    return arts


def get_article_info(arts, article):
    """Get information from an article and add it to a data object.

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
