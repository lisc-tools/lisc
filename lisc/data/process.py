"""Utilities for processing article data."""

from copy import deepcopy

from lisc.data.utils import convert_string, lower_list

###################################################################################################
###################################################################################################

def process_articles(articles, process_copy=False):
    """Process collected data in an Articles object.

    Parameters
    ----------
    articles : Articles
        Articles data.
    process_copy : bool, optional, default: False
        Whether to process a copy of the input.

    Notes
    -----
    Processing includes tokenizing the text data and preprocessing the journal and author names.
    """

    if process_copy:
        articles = deepcopy(articles)

    # Process text data: tokenizing, dropping stopwords, and making lowercase
    articles.words = [convert_string(words) for words in articles.words]
    articles.keywords = [lower_list(keywords) for keywords in articles.keywords]

    # Sub-select the journal names, keeping only the
    articles.journals = [journal[0] for journal in articles.journals]

    # Process author data: restrict the last name and initials
    articles.authors = _process_authors(articles.authors)

    return articles


def _process_authors(authors):
    """Process author names.

    Parameters
    ----------
    authors : list of list of str
        Collected author information. Each list is an articles.
        Each author is [last_name, first_name, initials, affiliations]

    Notes
    -----
    Processing means checking the author names and dropping to [last_name, initials].
    """

    # Reduce author fields to pair of tuples (last name, initials)
    authors = [[(author[0], author[2]) for author in art_authors] if art_authors else None \
        for art_authors in authors]

    # Check and fix author names
    authors = [_fix_author_names(art_authors) if art_authors else None for art_authors in authors]

    return authors


def _fix_author_names(names):
    """Fix author names.

    Parameters
    ----------
    names : list of tuple of (str, str)
        Author names, as (last name, initials).

    Returns
    -------
    names : list of tuple of (str, str)
        Author names, as (last name, initials).

    Notes
    -----
    Sometimes full author name ends up in the last name field.
    If first name is None, assume this happened:
    Split up the text in first name, and grab the first name initial.
    """

    # Drop names where the contents is all None
    names = [name for name in names if name != (None, None)]

    # Fix names if full name ended up in last name field
    names = [(name[0].split(' ')[-1], ''.join([temp[0] for temp in name[0].split(' ')[:-1]]))
             if name[1] is None else name for name in names]

    return names
