"""Classes and functions to store aggregated term article data."""

import os
import json

import nltk

from lisc.utils.io import check_ext
from lisc.utils.db import check_directory
from lisc.data.utils import combine_lists, convert_string
from lisc.data.count import count_years, count_journals, count_authors, count_end_authors
from lisc.data.base_articles import BaseArticles

###################################################################################################
###################################################################################################

class ArticlesAll(BaseArticles):
    """An object to hold term data, aggregated across articles.

    Attributes
    ----------
    label : str
        Label for the current term.
    term : Term object
        Definition of the search term, with inclusions and exclusion words.
    n_articles : int
        Number of articles included in object.
    ids : list of int
        Article ids for all articles included in object.
    journals : list of tuple of (int, str)
        Counts for each journal.
    authors : list of tuple of (int, (str, str))
        Counts for each author.
    first_authors : list of tuple of (int, (str, str))
        Counts for each first author.
    last_authors : list of tuple of (int, (str, str))
        Counts for each last author.
    words : nltk.probability.FreqDist
        Frequency distribution of all words.
    keywords : nltk.probability.FreqDist
        Frequency distribution of all keywords.
    years : list of tuple of (int, int)
        Counts for each year of publication.
    dois : list of str
        DOIs of each article included in object.
    summary : dict
        A summary of the data associated with the current object.
    """

    def __init__(self, term_data, exclusions=[]):
        """Initialize ArticlesAll object.

        Parameters
        ----------
        term_data : Articles object
            Data for all articles from a given search term.
        exclusions : list of str
            Words to exclude from the word collections.
        """

        # Inherit from the BaseArticles object
        BaseArticles.__init__(self, term_data.term)

        # Copy over tracking of included IDs & DOIs
        self.ids = term_data.ids
        self.dois = term_data.dois

        # Get counts of authors, journals, years
        self.journals = count_journals(term_data.journals)
        self.authors = count_authors(term_data.authors)
        self.first_authors, self.last_authors = count_end_authors(term_data.authors)
        self.years = count_years(term_data.years)

        # Convert lists of all words to frequency distributions
        exclusions = exclusions + self.term.search + self.term.inclusions
        temp_words = [convert_string(words) for words in term_data.words]
        self.words = self.create_freq_dist(combine_lists(temp_words), exclusions)
        self.keywords = self.create_freq_dist(combine_lists(term_data.keywords), exclusions)

        # Initialize summary dictionary
        self.summary = dict()


    def check_frequencies(self, data_type='words', n_check=20):
        """Prints out the most common items in frequecy distribution.

        Parameters
        ----------
        data_type : {'words', 'keywords'}
            Which frequency distribution to check.
        n_check : int
            Number of most common items to print out.
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
        top_str = ' , '.join([word[0] for word in top[:n_check]])

        # Print out the top words for the current term
        print("{:5} : ".format(self.label) + top_str)


    def create_summary(self):
        """Fill the summary dictionary of the current terms Words data."""

        # Add data to summary dictionary.
        self.summary['label'] = self.label
        self.summary['n_articles'] = str(self.n_articles)
        self.summary['top_author_name'] = ' '.join([self.authors[0][1][1],
                                                    self.authors[0][1][0]])
        self.summary['top_author_count'] = str(self.authors[0][0])
        self.summary['top_journal_name'] = self.journals[0][1]
        self.summary['top_journal_count'] = str(self.journals[0][0])
        self.summary['top_keywords'] = [freq[0] for freq in self.keywords.most_common()[0:5]]
        self.summary['first_publication'] = str(min([year[0] for year in self.years]))


    def print_summary(self):
        """Print out a summary of the collected words data."""

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
        directory : str or SCDB object, optional
            Folder or database object specifying the save location.
        """

        directory = check_directory(directory, 'summary')

        with open(os.path.join(directory, check_ext(self.label, '.json')), 'w') as outfile:
            json.dump(self.summary, outfile)


    @staticmethod
    def create_freq_dist(in_lst, exclude):
        """Create frequency distribution.

        Parameters
        ----------
        in_lst : list of str
            Word items to create frequecy distribution of.
        exclude : list of str
            Words to exclude from list.

        Returns
        -------
        freqs : nltk.FreqDist
            Frequency distribution of the input list.
        """

        freqs = nltk.FreqDist(in_lst)

        for excl in exclude:
            try:
                freqs.pop(excl.lower())
            except KeyError:
                pass

        return freqs
