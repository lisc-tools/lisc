"""Classes and functions to store aggregated term article data."""

from copy import deepcopy

from lisc.io.io import save_json
from lisc.io.db import check_directory
from lisc.data.utils import combine_lists, count_elements
from lisc.data.base_articles import BaseArticles
from lisc.data.process import process_articles

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
    has_data : bool
        Whether the object contains data.
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

    def __init__(self, articles, exclusions=None):
        """Initialize ArticlesAll object.

        Parameters
        ----------
        articles : Articles
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
        BaseArticles.__init__(self, articles.term)

        # Process the article data
        if not articles.processed:
            articles = process_articles(articles)

        # Set exclusions, copying input list, if given, and adding current search terms
        exclusions = list(set((deepcopy(exclusions) if exclusions else []) + \
            [articles.term.label] + articles.term.search + articles.term.inclusions))

        # Copy over tracking of included IDs & DOIs
        self.ids = articles.ids
        self.dois = articles.dois

        # Get frequency distributions of years, journals, authors
        self.years = count_elements(articles.years)
        self.journals = count_elements(articles.journals)
        self.first_authors = count_elements(\
            auth[0] if auth else None for auth in articles.authors)
        self.last_authors = count_elements(\
            auth[-1] if auth and len(auth) > 1 else None for auth in articles.authors)
        self.authors = count_elements(combine_lists(articles.authors))

        # Convert lists of all words to frequency distributions
        self.words = count_elements(combine_lists(articles.words), exclusions)
        self.keywords = count_elements(combine_lists(articles.keywords), exclusions)

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

        self.summary['label'] = self.label
        self.summary['n_articles'] = str(self.n_articles)
        if self.has_data:
            self.summary['top_author_name'] = ' '.join(self.authors.most_common()[0][0])
            self.summary['top_author_count'] = str(self.authors.most_common()[0][1])
            self.summary['top_journal_name'] = self.journals.most_common()[0][0]
            self.summary['top_journal_count'] = str(self.journals.most_common()[0][1])
            self.summary['top_keywords'] = [freq[0] for freq in self.keywords.most_common()[0:5]]
            self.summary['first_publication'] = str(min(self.years.keys()))
        else:
            labels = ['top_author_name', 'top_author_count', 'top_journal_name',
                      'top_journal_count', 'top_keywords', 'first_publication']
            for label in labels:
                self.summary[label] = None


    def print_summary(self):
        """Print out a summary of the collected words data.

        Examples
        --------
        Print a summary for a term, assuming an initialized ``ArticlesAll`` object with data:

        >>> articles_all.create_summary() # doctest:+SKIP
        >>> articles_all.print_summary() # doctest:+SKIP
        """

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

        save_json(self.summary, self.label, check_directory(directory, 'summary'))
