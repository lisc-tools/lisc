"""Functions to process extracted tags from scraping for LISC."""

from nltk import word_tokenize
from nltk.corpus import stopwords

from lisc.core.decorators import CatchNone, CatchNone2

###################################################################################################
###################################################################################################

def extract(dat, tag, how):
    """Extract data from HTML tag.

    Parameters
    ----------
    dat : bs4.element.Tag
        HTML data to pull specific tag out of.
    tag : str
        Label of the tag to extract.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to extract the data.
            raw - extract an embedded tag
            str - extract text and convert to string
            all - extract all embedded tags

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    # Check how spec if valid
    if how not in ['raw', 'str', 'all']:
        raise ValueError('Value for how is not understood.')

    # Use try to be robust to missing tag
    try:
        if how == 'raw':
            return dat.find(tag)
        elif how == 'str':
            return dat.find(tag).text
        elif how == 'all':
            return dat.findAll(tag)

    except AttributeError:
        return None


def ids_to_str(ids):
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
def process_words(text):
    """Processes abstract text - sets to lower case, and removes stopwords and punctuation.

    Parameters
    ----------
    text : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of tokenized words, after processing.
    """

    words = word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation)
    words_cleaned = [word.lower() for word in words if (
        (not word.lower() in stopwords.words('english')) & word.isalnum())]

    return words_cleaned


@CatchNone
def process_kws(keywords):
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
def process_authors(authors):
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
    authors = extract(authors, 'Author', 'all')

    # Extract data for each author
    out = []
    for author in authors:
        out.append((extract(author, 'LastName', 'str'), extract(author, 'ForeName', 'str'),
                    extract(author, 'Initials', 'str'), extract(author, 'Affiliation', 'str')))

    return out


@CatchNone2
def process_pub_date(pub_date):
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
def process_ids(ids, id_type):
    """Extract and process ID data.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        All the ArticleId tags, with all IDs for the article.
    id_type : {'pubmed', 'doi'}
        Which type of ID to extract & process.

    Returns
    -------
    out : str or lst or None
        A str or list of available IDs, if any are available, otherwise None.
    """

    lst = [str(cur_id.contents[0]) for cur_id in ids if cur_id.attrs == {'IdType' : id_type}]

    if not lst:
        out = None
    elif len(lst) == 1:
        out = lst[0]
    else:
        out = lst

    return out
