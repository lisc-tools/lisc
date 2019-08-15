"""Functions to process extracted tags from data collected with LISC."""

from nltk import word_tokenize
from nltk.corpus import stopwords

from lisc.core.decorators import catch_none

###################################################################################################
###################################################################################################

def extract(tag, label, how):
    """Extract data from HTML tag.

    Parameters
    ----------
    tag : bs4.element.Tag
        HTML data to pull specific tag out of.
    label : str
        Label of the tag to extract.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to extract the data.
            raw    - extract an embedded tag
            str    - extract text and convert to string
            all    - extract all embedded tags
            allstr - extract all embedded tags, and convert to string

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    if how not in ['raw', 'str', 'all', 'allstr']:
        raise ValueError('Value for how is not understood.')

    # Use try to be robust to missing tag
    try:
        if how == 'raw':
            return tag.find(label)
        elif how == 'str':
            return tag.find(label).text
        elif how == 'all':
            return tag.findAll(label)
        elif how == 'allstr':
            return ' '.join([part.text for part in tag.findAll('AbstractText')])

    except AttributeError:
        return None


def ids_to_str(ids):
    """Convert a list of article IDs to a comma separated string of IDs.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        List of article IDs.

    Returns
    -------
    ids_str : str
        A string of all concatenated IDs.
    """

    # Check how many IDs in list & initialize string with first ID
    n_ids = len(ids)
    ids_str = str(ids[0].text)

    # Loop through rest of the ID's, appending to end of id_str
    for ind in range(1, n_ids):
        ids_str = ids_str + ',' + str(ids[ind].text)

    return ids_str


@catch_none(1)
def process_words(text):
    """Processes abstract text.

    Parameters
    ----------
    text : str
        Text as one long string.

    Returns
    -------
    words_cleaned : list of str
        List of tokenized words, after processing.

    Notes
    -----
    This function sets text to lower case, and removes stopwords and punctuation.
    """

    words = word_tokenize(text)

    # Remove stop words, and non-alphabetical tokens (punctuation)
    words_cleaned = [word.lower() for word in words if (
        (not word.lower() in stopwords.words('english')) & word.isalnum())]

    return words_cleaned


@catch_none(1)
def process_keywords(keywords):
    """Extract and process keywords.

    Parameters
    ----------
    keywords : bs4.element.ResultSet
        List of all the keyword tags.

    Returns
    -------
    list of str
        List of all the keywords.
    """

    return [kw.text.lower() for kw in keywords]


@catch_none(1)
def process_authors(authors):
    """Extract and process authors.

    Parameters
    ----------
    authors : bs4.element.Tag
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


@catch_none(1)
def process_pub_date(pub_date):
    """Extract and process publication dates.

    Parameters
    ----------
    pub_date : bs4.element.Tag
        PubDate tag, which contains tags with publication date information.

    Returns
    -------
    year : int or None
        Year the article was published.
    """

    # Extract year, convert to int if not None
    year = extract(pub_date, 'Year', 'str')
    year = int(year) if year else year

    return year


@catch_none(1)
def process_ids(ids, id_type):
    """Extract and process IDs.

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
