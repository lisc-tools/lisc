"""Classes and functions to store aggregated term article data."""

import os
import json

from lisc.utils.io import check_ext
from lisc.utils.db import check_directory
from lisc.data.utils import combine_lists, convert_string, count_elements, drop_none
from lisc.data.base_articles import BaseArticles

###################################################################################################
###################################################################################################

class ArticlesAll(BaseArticles):
    """An object to hold term data, aggregated across articles.

    Attributes
    ----------
    label : str
        Label for the term.
    term : Term
        Definition of the search term, with inclusion and exclusion words.
    n_articles : int
        Number of articles included in object.
    ids : list of int
        Article ids for all articles included in object.
    journals : collections.Counter
        Frequency distribution for each journal.
    authors : collections.Counter
        Frequency distribution for each author.
    first_authors : collections.Counter
        Frequency distribution for each first author.
    last_authors : collections.Counter
        Frequency distribution for each last author.
    words : collections.Counter
        Frequency distribution of all words.
    keywords : collections.Counter
        Frequency distribution of all keywords.
    years : collections.Counter
        Frequency distribution for each year of publication.
    dois : list of str
        DOIs of each article included in object.
    summary : dict
        A summary of the data associated with the current object.
    """

    def __init__(self, term_data, exclusions=None):
        """Initialize ArticlesAll object.

        Parameters
        ----------
        term_data : Articles
            Data for all articles from a given search term.
        exclusions : list of str, optional
            Words to exclude from the word collections.

        Examples
        --------
        Create an ``ArticlesAll`` object from an :class:`~.Articles` object:

        >>> from lisc.data import Articles
        >>> articles = Articles('frontal lobe')
        >>> articles_all = ArticlesAll(articles)
        """

        # Inherit from the BaseArticles object
        BaseArticles.__init__(self, term_data.term)

        # Collect together search terms to add to exclusions or use as exclusions
        term = term_data.term
        searches = list(set(list([term.label] + term.search + term.inclusions)))
        exclusions = searches if not exclusions else exclusions.extend(searches)

        # Copy over tracking of included IDs & DOIs
        self.ids = term_data.ids
        self.dois = term_data.dois

        # Get frequency distributions of authors, journals, years
        self.journals = count_elements([journal[0] for journal in term_data.journals])
        self.years = count_elements(term_data.years)
        self.authors = _count_authors(term_data.authors)
        self.first_authors, self.last_authors = _count_end_authors(term_data.authors)

        # Convert lists of all words to frequency distributions
        exclusions = exclusions if exclusions else [] + self.term.search + self.term.inclusions
        temp_words = [convert_string(words) for words in term_data.words]
        self.words = count_elements(combine_lists(temp_words), exclusions)
        self.keywords = count_elements(combine_lists(term_data.keywords), exclusions)

        # Initialize summary dictionary
        self.summary = dict()


    def check_frequencies(self, data_type='words', n_check=20):
        """Prints out the most common items in a frequency distribution.

        Parameters
        ----------
        data_type : {'words', 'keywords'}
            Which frequency distribution to check.
        n_check : int, optional, default: 20
            Number of most common items to print out.

        Examples
        --------
        Print the most frequent words, assuming an initialized ``ArticlesAll`` object with data:

        >>> articles_all.check_frequencies() # doctest:+SKIP
        """

        if data_type in ['words', 'keywords']:
            freqs = getattr(self, data_type)
        else:
            raise ValueError('Requested data not understood')

        # Reset number to check if there are fewer words available
        if n_check > len(freqs):
            n_check = len(freqs)

        # Get the requested number of most common words, and convert to str
        top = freqs.most_common()[0:n_check]
        top_str = ', '.join([word[0] for word in top[:n_check]])

        # Print out the top words for the current term
        print("{:5} : ".format(self.label) + top_str)


    def create_summary(self):
        """Fill the summary dictionary of the current terms Words data.

        Examples
        --------
        Create a summary for a term, assuming an initialized ``ArticlesAll`` object with collected
        ``Words`` data:

        >>> articles_all.create_summary() # doctest:+SKIP
        """

        # Add data to summary dictionary.
        self.summary['label'] = self.label
        self.summary['n_articles'] = str(self.n_articles)
        self.summary['top_author_name'] = ' '.join(self.authors.most_common()[0][0])
        self.summary['top_author_count'] = str(self.authors.most_common()[0][1])
        self.summary['top_journal_name'] = self.journals.most_common()[0][0]
        self.summary['top_journal_count'] = str(self.journals.most_common()[0][1])
        self.summary['top_keywords'] = [freq[0] for freq in self.keywords.most_common()[0:5]]
        self.summary['first_publication'] = str(min(self.years.keys()))


    def print_summary(self):
        """Print out a summary of the collected words data.

        Examples
        --------
        Print a summary for a term, assuming an initialized ``ArticlesAll`` object with data:

        >>> articles_all.create_summary() # doctest:+SKIP
        >>> articles_all.print_summary() # doctest:+SKIP
        """

        # Print out summary information
        print(self.summary['label'], ':')
        print('  Number of articles: \t\t', self.summary['n_articles'])
        print('  First publication: \t\t', self.summary['first_publication'])
        print('  Most common author: \t\t', self.summary['top_author_name'])
        print('    number of publications: \t', self.summary['top_author_count'])
        print('  Most common journal: \t\t', self.summary['top_journal_name'])
        print('    number of publications: \t', self.summary['top_journal_count'], '\n')


    def save_summary(self, directory=None):
        """Save out a summary of the collected words data.

        Parameters
        ----------
        directory : str or SCDB or None, optional
            Folder or database object specifying the save location.

        Examples
        --------
        Save a summary for a term, assuming an initialized ``ArticlesAll`` object with data::

        >>> articles_all.create_summary() # doctest:+SKIP
        >>> articles_all.save_summary() # doctest:+SKIP
        """

        directory = check_directory(directory, 'summary')

        with open(os.path.join(directory, check_ext(self.label, '.json')), 'w') as outfile:
            json.dump(self.summary, outfile)


def _count_authors(authors):
    """Count all authors.

    Parameters
    ----------
    authors : list of list of tuple of (str, str, str, str)
        Authors, as (last name, first name, initials, affiliation).

    Returns
    -------
    author_counts : collections.Counter
        Number of publications per author.
    """

    # Reduce author fields to pair of tuples (last name, initials)
    all_authors = [(author[0], author[2]) for art_authors \
        in drop_none(authors) for author in art_authors]

    # Standardize author names and count number of publications per author
    author_counts = count_elements(_fix_author_names(all_authors))

    return author_counts


def _count_end_authors(authors):
    """Count first and last authors only.

    Parameters
    ----------
    authors : list of list of tuple of (str, str, str, str)
        Authors, as (last name, first name, initials, affiliation).

    Returns
    -------
    first_counts, last_counts : collections.Counter
        Number of publications for each first and last author.
    """

    # Pull out the full name for the first & last author of each article
    #  Last author is only considered if there is more than 1 author
    firsts = [auth[0] for auth in drop_none(authors)]
    f_names = [(author[0], author[2]) for author in firsts]

    lasts = [auth[-1] for auth in drop_none(authors) if len(auth) > 1]
    l_names = [(author[0], author[2]) for author in lasts]

    f_counts = count_elements(_fix_author_names(f_names))
    l_counts = count_elements(_fix_author_names(l_names))

    return f_counts, l_counts


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
