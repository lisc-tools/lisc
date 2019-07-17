"""Scrape words data from Pubmed."""

from bs4 import BeautifulSoup

from lisc.data import Data
from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.scrape.info import get_db_info
from lisc.scrape.utils import mk_term, join
from lisc.scrape.process import (extract, ids_to_str, process_ids, process_authors,
                                 process_words, process_kws, process_pub_date)
from lisc.urls.eutils import EUtils, get_wait_time

###################################################################################################
###################################################################################################

def scrape_words(terms, exclusions=[], db='pubmed', retmax=None, field='TIAB', api_key=None,
                 use_hist=False, save_n_clear=False, logging=None, folder=None, verbose=False):
    """Scrape pubmed for documents using specified term(s).

    Parameters
    ----------
    terms : list of list of str
        Search terms.
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
    urls.build_url('info', ['db'])
    urls.build_url('search', ['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_url('fetch', ['db', 'retmode'])

    # Initialize results, meta data & requester
    results = []
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated),
                    logging=logging, folder=folder)

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.get_url('info')))

    # Check exclusions
    if not exclusions:
        exclusions = [[] for ind in range(len(terms))]

    # Loop through all the terms
    for term, excl in zip(terms, exclusions):

        if verbose:
            print('Scraping words for: ', term[0])

        # Initiliaze object to store data for current term papers
        cur_dat = Data(term[0], term)
        cur_dat.update_history('Start Scrape')

        # Set up search terms - add exclusions, if there are any
        term_arg = join(mk_term(term), mk_term(excl), 'NOT')
        url = urls.get_url('search', {'term' : term_arg})
        page = req.request_url(url)
        page_soup = BeautifulSoup(page.content, 'lxml')

        if use_hist:

            ret_start_it = 0

            # Get number of papers, and keys to use history
            count = int(page_soup.find('count').text)
            web_env = page_soup.find('webenv').text
            query_key = page_soup.find('querykey').text

            # Loop through pulling paper data, using history
            while ret_start_it < count:

                # Set the number of papers per iteration (the ret_max per call)
                #  This defaults to 100, but will set to less if fewer needed to reach retmax
                ret_end_it = min(100, int(retmax) - ret_start_it)

                # Get article page, scrape data, update position
                url_settings = {'WebEnv' : web_env, 'query_key' : query_key,
                                'retstart' : str(ret_start_it), 'retmax' : str(ret_end_it)}
                art_url = urls.get_url('fetch', url_settings)
                cur_dat = get_papers(req, art_url, cur_dat)
                ret_start_it += ret_end_it

                if ret_start_it >= int(retmax):
                    break

        # Without using history
        else:

            ids = page_soup.find_all('id')
            art_url = urls.get_url('fetch', {'id' : ids_to_str(ids)})
            cur_dat = get_papers(req, art_url, cur_dat)

        cur_dat.check_results()
        cur_dat.update_history('End Scrape')

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


def extract_add_info(cur_dat, art_id, art):
    """Extract information from article web page and add to a data object.

    Parameters
    ----------
    cur_dat : Data() object
        Object to store information for the current term.
    art_id : int
        Paper ID of the new paper.
    art : bs4.element.Tag() object
        Extracted pubmed article.

    Returns
    -------
    cur_dat : Data() object
        Object to store data from the current term.
    """

    cur_dat.add_id(art_id)
    cur_dat.add_title(extract(art, 'ArticleTitle', 'str'))
    cur_dat.add_authors(process_authors(extract(art, 'AuthorList', 'raw')))
    cur_dat.add_journal(extract(art, 'Title', 'str'), extract(art, 'ISOAbbreviation', 'str'))
    cur_dat.add_words(process_words(extract(art, 'AbstractText', 'str')))
    cur_dat.add_kws(process_kws(extract(art, 'Keyword', 'all')))
    cur_dat.add_pub_date(process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_dat.add_doi(process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

    cur_dat.increment_n_articles()

    return cur_dat
