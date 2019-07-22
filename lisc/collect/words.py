"""Scrape words data from Pubmed."""

from bs4 import BeautifulSoup

from lisc.data.data import Data
from lisc.data.term import Term
from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.collect.utils import mk_term
from lisc.collect.info import get_db_info
from lisc.collect.process import (extract, ids_to_str, process_ids, process_authors,
                                  process_words, process_kws, process_pub_date)
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def collect_words(terms, inclusions=[], exclusions=[], db='pubmed', retmax=None,
                  field='TIAB', api_key=None, use_hist=False, save_n_clear=False,
                  logging=None, folder=None, verbose=False):
    """Scrape pubmed for documents using specified term(s).

    Parameters
    ----------
    terms : list of list of str
        Search terms.
    inclusions : list of list of str, optional
        Inclusion words for search terms.
    exclusions : list of list of str, optional
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
    save_n_clear : bool, optional, default: False
        Whether to save words data to disk per term as it goes, instead of holding in memory.
    logging : {None, 'print', 'store', 'file'}
        What kind of logging, if any, to do for requested URLs.
    folder : str or SCDB() object, optional
        Folder or database object specifying the save location.
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

    # Get e-utils URLS object
    urls = EUtils(db=db, usehistory='y' if use_hist else 'n', retmax=retmax,
                  retmode='xml', field=field, api_key=api_key)
    urls.build_url('info', settings=['db'])
    urls.build_url('search', settings=['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_url('fetch', settings=['db', 'retmode'])

    # Initialize results, meta data & requester
    results = []
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated),
                    logging=logging, folder=folder)

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
            print('Scraping words for: ', term.label)

        # Initiliaze object to store data for current term papers
        cur_dat = Data(term)

        # Request web page
        url = urls.get_url('search', settings={'term' : term_arg})
        page = req.request_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        if use_hist:

            # Get number of papers, and keys to use history
            count = int(page_soup.find('count').text)
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Loop through pulling paper data, using history
            ret_start_it = 0
            while ret_start_it < count:

                # Set the number of papers per iteration (the ret_max per call)
                #  This defaults to 100, but will set to less if fewer needed to reach retmax
                ret_end_it = min(100, int(retmax) - ret_start_it)

                # Get article page, scrape data, update position
                url_settings = {'WebEnv' : web_env, 'query_key' : query_key,
                                'retstart' : str(ret_start_it), 'retmax' : str(ret_end_it)}
                art_url = urls.get_url('fetch', settings=url_settings)
                cur_dat = get_papers(req, art_url, cur_dat)
                ret_start_it += ret_end_it

                if ret_start_it >= int(retmax):
                    break

        # Without using history
        else:

            ids = page_soup.find_all('id')
            art_url = urls.get_url('fetch', settings={'id' : ids_to_str(ids)})
            cur_dat = get_papers(req, art_url, cur_dat)

        cur_dat.check_results()

        if save_n_clear:
            cur_dat.save_n_clear(folder=folder)
        results.append(cur_dat)

    meta_data.add_requester(req)

    return results, meta_data


def get_papers(req, art_url, cur_dat):
    """Scrape information for each article found for a given term.

    Parameters
    ----------
    req : Requester() object
        Requester object to launch requests from.
    art_url : str
        URL for the article to be scraped.
    cur_dat : Data() object
        Data object to add data to

    Returns
    -------
    cur_dat : Data() object
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
    """Extract information from article web page and add to a data object.

    Parameters
    ----------
    cur_data : Data() object
        Object to store information for the current article.
    art_id : int
        Paper ID of the new paper.
    art : bs4.element.Tag() object
        Extracted pubmed article.

    Returns
    -------
    cur_data : Data() object
        Object updated with data from the current article.
    """

    cur_data.add_data('ids', art_id)
    cur_data.add_data('titles', extract(art, 'ArticleTitle', 'str'))
    cur_data.add_data('authors', process_authors(extract(art, 'AuthorList', 'raw')))
    cur_data.add_data('journals', (extract(art, 'Title', 'str'), extract(art, 'ISOAbbreviation', 'str')))
    cur_data.add_data('words', process_words(extract(art, 'AbstractText', 'str')))
    cur_data.add_data('kws', process_kws(extract(art, 'Keyword', 'all')))
    cur_data.add_data('years', process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_data.add_data('dois', process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

    return cur_data
