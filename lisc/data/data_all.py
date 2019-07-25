"""Classes and functions to store aggregated term paper data."""

import os
import json

import nltk

from lisc.core.io import check_ext
from lisc.core.db import check_folder
from lisc.data.utils import combine_lists
from lisc.data.count import count_years, count_journals, count_authors, count_end_authors
from lisc.data.base_data import BaseData

###################################################################################################
###################################################################################################

class DataAll(BaseData):
    """Object to hold term data, aggregated across papers.

    Attributes
    ----------
    label : str
        Label for the current term.
    term : Term() object
        Definition of the search term, with inclusions and exclusion words.
    n_articles : int
        Number of articles whos data is included in object.
    ids : list of int
        Pubmed article ids for all articles included in object.
    journals : list of tuple of (int, str)
        Counter across all journals.
    authors : list of tuple of (int, (str, str))
        Counter across all authors.
    first_authors : list of tuple of (int, (str, str))
        Counter across all first authors.
    last_authors : list of tuple of (int, (str, str))
        Counter across all last authors.
    words : nltk.probability.FreqDist
        Frequency distribution of all words.
    kws : nltk.probability.FreqDist
        Frequency distribution of all keywords.
    years : list of tuple of (int, int)
        Counter across all years of publication.
    dois : list of str
        DOIs of each article included in object.
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

        # Inherit from the BaseData object
        BaseData.__init__(self, term_data.term)

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
        self.words = self.create_freq_dist(combine_lists(term_data.words), exclusions)
        self.kws = self.create_freq_dist(combine_lists(term_data.kws), exclusions)

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
            freqs = getattr(self, data)
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
        self.summary['top_kws'] = [freq[0] for freq in self.kws.most_common()[0:5]]
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


    def save_summary(self, folder=None):
        """Save out a summary of the collected words data.

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
