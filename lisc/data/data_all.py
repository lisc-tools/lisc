"""Classes and functions to store aggregated term paper data."""

import os
import json

import nltk

from lisc.core.io import check_ext
from lisc.core.db import check_folder

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
            xx
        exclusions : list of str
            Words to exclude from the word collections.
        """

        self.label = term_data.label
        self.term = term_data.term
        self.n_articles = term_data.n_articles

        # Combine all articles into single list of all words
        self.all_words = _combine(term_data.words)
        self.all_kws = _combine(term_data.kws)

        # Convert lists of all words in frequency distributions
        self.word_freqs = _freq_dist(self.all_words, self.term + [self.label] + exclusions)
        self.kw_freqs = _freq_dist(self.all_kws, self.term + [self.label] + exclusions)

        # Get counts of authors, journals, years
        self.author_counts = _proc_authors(term_data.authors)
        self.f_author_counts, self.l_author_counts = \
            _proc_end_authors(term_data.authors)
        self.journal_counts = _proc_journals(term_data.journals)
        self.year_counts = _proc_years(term_data.years)

        # Initialize summary dictionary
        self.summary = dict()


    def check_words(self, n_check=20):
        """Check the most common words for the term.

        Parameters
        ----------
        n_check : int, optional, default: 20
            Number of top words to print out.
        """

        _check(self.word_freqs, n_check, self.label)


    def check_kws(self, n_check=20):
        """Check the most common kws for the term.

        Parameters
        ----------
        n_check : int, optional, default: 20
            Number of top words to print out.
        """

        _check(self.kw_freqs, n_check, self.label)


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

###################################################################################################
###################################################################################################

def _check(freqs, n_check, label):
    """Prints out the most common items in frequecy distribution.

    Parameters
    ----------
    freqs : nltk.FreqDist
        Frequency distribution to check.
    n_check : int
        Number of most common items to print out.
    label : str
        Label to print for which data this relates to.
    """

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
    print("{:5} : ".format(label) + top_str)


def _combine(in_lst):
    """Combine list of lists into one large list.

    Parameters
    ----------
    in_lst : list of list of str
        Embedded lists to combine.

    Returns
    -------
    out : list of str
        Combined list.
    """

    out = []

    for ind in range(len(in_lst)):
        if in_lst[ind]:
            out.extend(in_lst[ind])

    return out


def _freq_dist(in_lst, exclude):
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


def _proc_years(year_lst):
    """Process years.

    Parameters
    ----------
    year_lst : list of int
        Year of publication of all papers.

    Returns
    -------
    counts : list of tuple of (int, int)
        Number of publications per year - (year, n).
    """

    counts = [(year, year_lst.count(year)) for year in set(year_lst) - set([None])]
    counts.sort()

    return counts


def _proc_journals(journals_lst):
    """Process journals.

    Parameters
    ----------
    j_lst : list of tuple of (str, str)
        List of journals articles come from.
            (Journal Name, ISO abbreviation)

    Returns
    -------
    counts : list of tuple of (int, str)
        Number of publications per journal - (n, Journal Name).
    """

    names = [journal[0] for journal in journals_lst]

    # TODO: Update this quick fix (??)
    names = [name for name in names if name is not None]

    counts = [(names.count(element), element) for element in set(names)]
    counts.sort(reverse=True)

    return counts


def _proc_authors(authors_lst):
    """Process all authors.

    Parameters
    ----------
    authors_lst : list of list of tuple of (str, str, str, str)
        Authors of all articles included in object.
            (Last Name, First Name, Initials, Affiliation)

    Returns
    -------
    author_counts : list of tuple of (int, (str, str))
        Number of publications per author - (n, (Last Name, Initials)).
    """

    # Drop author lists that are None
    authors_lst = [author for author in authors_lst if author is not None]

    # Reduce author fields to pair of tuples (L_name, Initials)
    # This list comprehension can be equivalently written as:
    # all_authors = []
    # for authors in a_lst:
    #     for author in authors:
    #         all_authors.append(author)
    names = [(author[0], author[2]) for authors in authors_lst for author in authors]

    # Count how often each author published
    author_counts = _count(_fix_names(names))

    return author_counts


def _proc_end_authors(authors_lst):
    """Process first and last authors only.

    Parameters
    ----------
    authors_lst : list of list of tuple of (str, str, str, str)
        Authors of all articles included in object.
            (Last Name, First Name, Initials, Affiliation)

    Returns
    -------
    counts : list of tuple of (int, (str, str))
        Number of publications per author - (n, (Last Name, Initials)).
    """

    # Drop author lists that are None
    authors_lst = [author for author in authors_lst if author is not None]

    # Pull out the full name for the first & last author of each paper
    #  Last author is only considered if there is more than 1 author
    firsts = [authors[0] for authors in authors_lst]
    f_names = [(author[0], author[2]) for author in firsts]
    lasts = [authors[-1] for authors in authors_lst if len(authors) > 1]
    l_names = [(author[0], author[2]) for author in lasts]

    f_counts = _count(_fix_names(f_names))
    l_counts = _count(_fix_names(l_names))

    return f_counts, l_counts


def _fix_names(names):
    """Fix author names.

    Parameters
    ----------
    names : list of tuple of (L_Name, Initials)
        Author names.

    Returns
    -------
    names : list of tuple of (L_Name, Initials)
        Author names.

    Notes
    -----
    Sometimes full author name ends up in the last name field.
    If first name is None, assume this happened:
        Split up the text in first name, and grab the first name initial.
    """

    # Drop names whos data is all None
    names = [name for name in names if name != (None, None)]

    # TODO: figure out and fix
    # Fix names if full name ended up in last name field
    #names = [(name[0].split(' ')[1], name[0].split(' ')[0][0])
    #         if name[1] is None else name for name in names]

    return names


def _count(data_lst):
    """Count occurences of each item in a list.

    Parameters
    ----------
    data_lst : list of str
        List of items to count occurences of.

    Returns
    -------
    counts : list of tuple of (item_label, count)
        Counts for how often each item occurs in the input list.
    """

    counts = [(data_lst.count(element), element) for element in set(data_lst)]
    counts.sort(reverse=True)

    return counts
