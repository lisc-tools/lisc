"""Scrape words data from Pubmed."""

from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk.corpus import stopwords

from lisc.data import Data
from lisc.requester import Requester
from lisc.data.meta_data import MetaData
from lisc.scrape.info import get_db_info
from lisc.scrape.utils import comb_terms, extract
from lisc.urls.pubmed import URLS, get_wait_time
from lisc.core.decorators import CatchNone, CatchNone2

###################################################################################################
###################################################################################################

def scrape_words(terms_lst, exclusions_lst=[], db='pubmed', retmax=None, field='TIAB',
                 api_key=None, use_hist=False, save_n_clear=True, verbose=False):
    """Scrape pubmed for documents using specified term(s).

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
    save_n_clear : bool, optional, default: False
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

    # Get e-utils URLS object
    hist_val = 'y' if use_hist else 'n'
    urls = URLS(db=db, usehistory=hist_val, retmax=retmax,
                retmode='xml', field=field, api_key=api_key)
    urls.build_url('info', ['db'])
    urls.build_url('search', ['db', 'usehistory', 'retmax', 'retmode', 'field'])
    urls.build_url('fetch', ['db', 'retmode'])

    # Initialize results, meta data & requester
    results = []
    meta_data = MetaData()
    req = Requester(wait_time=get_wait_time(urls.authenticated))

    # Get current information about database being used
    meta_data.add_db_info(get_db_info(req, urls.info))

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

        cur_dat.update_history('Start Scrape')

        # Create the url for the search term
        url = urls.search + term_arg

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
                cur_dat = get_papers(req, art_url, cur_dat)
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
            cur_dat = get_papers(req, art_url, cur_dat)

        # Check consistency of extracted results
        cur_dat.check_results()
        cur_dat.update_history('End Scrape')

        # Save out and clear data
        if save_n_clear:
            cur_dat.save_n_clear()
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

    Returns
    -------
    cur_dat : Data() object
        Object to store information for the current term.
    """

    # Get page of all articles
    art_page = req.get_url(art_url)
    art_page_soup = BeautifulSoup(art_page.content, "xml")
    articles = art_page_soup.findAll('PubmedArticle')

    # Loop through each article, extracting relevant information
    for art in articles:

        # Get ID of current article & extract and add info to data object
        new_id = _process_ids(extract(art, 'ArticleId', 'all'), 'pubmed')
        cur_dat = _extract_add_info(cur_dat, new_id, art)

    return cur_dat

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

    cur_dat.add_id(new_id)
    cur_dat.add_title(extract(art, 'ArticleTitle', 'str'))
    cur_dat.add_authors(_process_authors(extract(art, 'AuthorList', 'raw')))
    cur_dat.add_journal(extract(art, 'Title', 'str'), extract(art, 'ISOAbbreviation', 'str'))
    cur_dat.add_words(_process_words(extract(art, 'AbstractText', 'str')))
    cur_dat.add_kws(_process_kws(extract(art, 'Keyword', 'all')))
    cur_dat.add_pub_date(_process_pub_date(extract(art, 'PubDate', 'raw')))
    cur_dat.add_doi(_process_ids(extract(art, 'ArticleId', 'all'), 'doi'))

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

    # Check how many ids in list & initialize string with first ID
    n_ids = len(ids)
    ids_str = str(ids[0].text)

    # Loop through rest of the ID's, appending to end of id_str
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

    words = word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation)
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
