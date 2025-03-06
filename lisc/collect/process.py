"""Functions to process tags from collected data."""

from lisc.modutils.decorators import catch_none

###################################################################################################
###################################################################################################

def get_info(tag, label, how):
    """Get information from a tag.

    Parameters
    ----------
    tag : bs4.element.Tag
        The data object to find the information from.
    label : str
        The name of the tag to get information from.
    how : {'raw', 'all' , 'txt', 'str'}
        Method to use to get the information.
            raw      - get an embedded tag
            str      - get text and convert to string
            all      - get all embedded tags
            all-str  - get all embedded tags, and convert to string
            all-list - get all embedded tags, and collect into a list

    Returns
    -------
    {bs4.element.Tag, bs4.element.ResultSet, unicode, str, None}
        Requested data from the tag. Returns None is requested tag is unavailable.
    """

    if how not in ['raw', 'str', 'all', 'all-str', 'all-list']:
        raise ValueError('Value for how is not understood.')

    # Use try to be robust to missing tag
    try:
        if how == 'raw':
            return tag.find(label)
        elif how == 'str':
            return tag.find(label).text
        elif how == 'all':
            return tag.find_all(label)
        elif how == 'all-str':
            return ' '.join([part.text for part in tag.find_all(label)])
        elif how == 'all-list':
            return [part.text for part in tag.find_all(label)]

    except AttributeError:
        return None


def extract_tag(page, label, approach='first', raise_error=False):
    """Extract a specified tag from a page.

    Parameters
    ----------
    page : bs4.BeautifulSoup or bs4.element.Tag
        Page of information with tags.
    label : str
        The name of the tag to extract.
    approach : {'first', 'all'}, optional
        Which approach to take for extracting tags.
        `first` extracts only the first relevant tag, `all` extracts all relevant tags.
    raise_error : bool, optional, default: False
        Whether to raise an error if the tag is not found.

    Returns
    -------
    page : bs4.BeautifulSoup
        The page, after extracting the tag.
    tag : bs4.element.Tag or None
        The extracted tag from the input page.
        If the tag was not found in the given page, is None.
    """

    if approach == 'first':

        try:
            tag = page.find(label).extract()
        except AttributeError:
            if raise_error:
                raise
            else:
                tag = None

    elif approach == 'all':

        tag = []
        try:
            while True:
                tag.append(page.find(label).extract())
        except AttributeError:
            if not tag:
                if raise_error:
                    raise
                else:
                    tag = None

    return page, tag


@catch_none(1)
def process_authors(authors):
    """Get information for and process authors.

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
    authors = get_info(authors, 'Author', 'all')

    # Get data for each author
    out = []
    for author in authors:
        out.append((get_info(author, 'LastName', 'str'), get_info(author, 'ForeName', 'str'),
                    get_info(author, 'Initials', 'str'), get_info(author, 'Affiliation', 'str')))

    return out


@catch_none(1)
def process_pub_date(pub_date):
    """Get information for and process publication dates.

    Parameters
    ----------
    pub_date : bs4.element.Tag
        PubDate tag, which contains tags with publication date information.

    Returns
    -------
    year : int or None
        Year the article was published.
    """

    # Check if the date is encoded in a 'Year' tag
    year = get_info(pub_date, 'Year', 'str')

    if not year:

        # Check for and get date from medline date tag if available
        year = get_info(pub_date, 'MedlineDate', 'str')

        # Sometimes date is year followed by months - so get first part
        if year[:4].isnumeric():
            year = year[:4]

        # Sometimes date is season followed by year - so get last part
        elif year[-4:].isnumeric():
            year = year[-4:]

        # Otherwise, date info is not clear: drop so as to not cause an error
        else:
            year = None

    # If a year was extracted, typecast to int
    year = int(year) if year else year

    return year


@catch_none(1)
def process_ids(ids, id_type):
    """Get information for and process IDs.

    Parameters
    ----------
    ids : bs4.element.ResultSet
        All the ArticleId tags, with all IDs for the article.
    id_type : {'pubmed', 'doi'}
        Which type of ID to get & process.

    Returns
    -------
    out : str or list or None
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
