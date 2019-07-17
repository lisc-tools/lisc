"""Classes and functions to store aggregated term paper data."""

import os
import json

import nltk

from lisc.core.io import check_ext
from lisc.core.db import check_folder
from lisc.data.utils import combine_lists
from lisc.data.count import count_years, count_journals, count_authors, count_end_authors

###################################################################################################
###################################################################################################

class DataAll():
    """Object to hold term data, aggregated across papers.

    Attributes
    ----------
    label : str
        Label for the current term.
    term : list of str
        Name(s) of the term word data relates to.
    n_articles : int
        Number of articles whos data is included in object.
    all_words : list of str
        All abstract words collected across all articles.
    all_kws : list of str
        All keywords collected across all articles.
    word_freqs : nltk.probability.FreqDist
        Frequency distribution of all words.
    kw_freqs : nltk.probability.FreqDist
        Frequency distribution of all keywords.
    author_counts : list of tuple of (int, (str, str))
        Counter across all authors.
    f_author_counts : list of tuple of (int, (str, str))
        Counter across all first authors.
    journal_counts : list of tuple of (int, str)
        Counter across all journals.
    year_counts : list of tuple of (int, int)
        Counter across all years of publication.
    summary : dict
        Summary / overview of data associated with current object.
    """

    def __init__(self, term_data, exclusions=[]):
        """Initialize DataAll() object.

        Parameters
        ----------
        term_data : Data() object
            Data for all papers from a given search term.
        exclusions : list of str
            Words to exclude from the word collections.
        """

        self.label = term_data.label
        self.term = term_data.term
        self.n_articles = term_data.n_articles

        # Combine all articles into single list of all words
        self.all_words = combine_lists(term_data.words)
        self.all_kws = combine_lists(term_data.kws)

        # Convert lists of all words to frequency distributions
        exclusions = exclusions + self.term + [self.label]
        self.word_freqs = self.create_freq_dist(self.all_words, exclusions)
        self.kw_freqs = self.create_freq_dist(self.all_kws, exclusions)

        # Get counts of authors, journals, years
        self.author_counts = count_authors(term_data.authors)
        self.f_author_counts, self.l_author_counts = count_end_authors(term_data.authors)
        self.journal_counts = count_journals(term_data.journals)
        self.year_counts = count_years(term_data.years)

        # Initialize summary dictionary
        self.summary = dict()


    def check_frequencies(self, data='words', n_check=20):
        """Prints out the most common items in frequecy distribution.

        Parameters
        ----------
        data : {'words', 'kws'}
            Which frequency distribution to check.
        n_check : int
            Number of most common items to print out.
        """

        if data in ['words', 'kws']:
            freqs = getattr(self, data[:-1] + '_freqs')
        else:
            raise ValueError('Requested data not understood')

        # Reset number to check if there are fewer words available
        if n_check > len(freqs):
            n_check = len(freqs)

        # Get the requested number of most common kws for the term
        top = freqs.most_common()[0:n_check]

        # Join together the top words into a string
        top_str = ''
        for i in range(n_check):
            top_str += top[i][0]
            top_str += ' , '

        # Print out the top words for the current term
        print("{:5} : ".format(self.label) + top_str)


    def create_summary(self):
        """Fill the summary dictionary of the current terms Words data."""

        # Add data to summary dictionary.
        self.summary['n_articles'] = str(self.n_articles)
        self.summary['top_author_name'] = ' '.join([self.author_counts[0][1][1],
                                                    self.author_counts[0][1][0]])
        self.summary['top_author_count'] = str(self.author_counts[0][0])
        self.summary['top_journal_name'] = self.journal_counts[0][1]
        self.summary['top_journal_count'] = str(self.journal_counts[0][0])
        self.summary['top_kws'] = [f[0] for f in self.kw_freqs.most_common()[0:5]]
        self.summary['first_publication'] = str(min([y[0] for y in self.year_counts]))

        if self.label != str(self.term[0]):
            self.summary['name'] = str(self.term[0])
        else:
            self.summary['name'] = ''


    def print_summary(self):
        """Print out a summary of the scraped term paper data."""

        # Print out summary information
        print(self.label, ':')
        print('  Full name of this term is: \t', self.summary['name'])
        print('  Number of articles: \t\t', self.summary['n_articles'])
        print('  First publication: \t\t', self.summary['first_publication'])
        print('  Most common author: \t\t', self.summary['top_author_name'])
        print('    number of publications: \t', self.summary['top_author_count'])
        print('  Most common journal: \t\t', self.summary['top_journal_name'])
        print('    number of publications: \t', self.summary['top_journal_count'], '\n')


    def save_summary(self, folder=None):
        """Save out a summary of the scraped term paper data.

        Parameters
        ----------
        folder : str or SCDB() object, optional
            Folder or database object specifying the save location.
        """

        folder = check_folder(folder, 'summary')

        with open(os.path.join(folder, check_ext(self.label, '.json')), 'w') as outfile:
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

        for it in exclude:
            try:
                freqs.pop(it.lower())
            except KeyError:
                pass

        return freqs
