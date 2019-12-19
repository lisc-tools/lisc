"""Class for collection and analyses of co-occurrences data."""

import numpy as np

from lisc.objects.base import Base
from lisc.objects.utils import wrap, get_max_length
from lisc.collect import collect_counts
from lisc.analysis.counts import compute_normalization, compute_association_index

###################################################################################################
###################################################################################################

class Counts():
    """A class for collecting and analyzing co-occurrence data for specified terms list(s).

    Attributes
    ----------
    terms : dict
        Search terms to use.
    counts : 2d array
        The numbers of articles found for each combination of terms.
    score : 2d array
        A transformed 'score' of co-occurrence data.
        This can be a normalized version of the data, and/or a computed association index.
    square : bool
        Whether the count data matrix is symmetrical.
    meta_data : MetaData
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Counts object."""

        # Initialize dictionary to store search terms
        self.terms = dict()
        for dat in ['A', 'B']:
            self.terms[dat] = Base()
            self.terms[dat].counts = np.zeros(0, dtype=int)

        self.counts = np.zeros(0)
        self.score = np.zeros(0)
        self.square = bool()
        self.meta_data = None


    def add_terms(self, terms, term_type='terms', dim='A'):
        """Add the given list of strings as terms.

        Parameters
        ----------
        terms : list of str or list of list of str
            List of terms.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms are being added.
        dim : {'A', 'B'}, optional
            Which set of terms to operate upon.
        """

        self.terms[dim].add_terms(terms, term_type)
        if term_type == 'terms':
            self.terms[dim].counts = np.zeros(self.terms[dim].n_terms, dtype=int)


    def add_terms_file(self, f_name, term_type='terms', directory=None, dim='A'):
        """Load terms from a text file.

        Parameters
        ----------
        f_name : str
            File name to load terms from.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms are being added.
        directory : SCDB or str or None
            A string or object containing a file path.
        dim : {'A', 'B'}, optional
            Which set of terms to operate upon.
        """

        self.terms[dim].add_terms_file(f_name, directory, term_type)
        if term_type == 'terms':
            self.terms[dim].counts = np.zeros(self.terms[dim].n_terms, dtype=int)


    def run_collection(self, db='pubmed', field='TIAB', api_key=None,
                       logging=None, directory=None, verbose=False):
        """Collect co-occurrence data.

        Parameters
        ----------
        db : str, optional, default: 'pubmed'
            Which database to access from EUtils.
        field : str, optional, default: 'TIAB'
            Field to search for term in.
            Defaults to 'TIAB', which is Title/Abstract.
        api_key : str, optional
            An API key for a NCBI account.
        logging : {None, 'print', 'store', 'file'}, optional
            What kind of logging, if any, to do for requested URLs.
        directory : str or SCDB, optional
            Folder or database object specifying the save location.
        verbose : bool, optional, default: False
            Whether to print out updates.
        """

        # Run single list of terms against themselves, in 'square' mode
        if not self.terms['B'].has_data:
            self.square = True
            self.counts, self.terms['A'].counts, self.meta_data = collect_counts(
                terms_a=self.terms['A'].terms,
                inclusions_a=self.terms['A'].inclusions,
                exclusions_a=self.terms['A'].exclusions,
                db=db, field=field, api_key=api_key,
                logging=logging, directory=directory,
                verbose=verbose)

        # Run two different sets of terms
        else:
            self.square = False
            self.counts, term_counts, self.meta_data = collect_counts(
                terms_a=self.terms['A'].terms,
                inclusions_a=self.terms['A'].inclusions,
                exclusions_a=self.terms['A'].exclusions,
                terms_b=self.terms['B'].terms,
                inclusions_b=self.terms['B'].inclusions,
                exclusions_b=self.terms['B'].exclusions,
                db=db, field=field, api_key=api_key,
                logging=logging, directory=directory,
                verbose=verbose)
            self.terms['A'].counts, self.terms['B'].counts = term_counts


    def compute_score(self, score_type='association', dim='A'):
        """Compute a score, such as an index or normalization, of the co-occurrence data.

        Parameters
        ----------
        score_type : {'association', 'normalize'}, optional
            The type of score to apply to the co-occurrence data.
        dim : {'A', 'B'}, optional
            Which dimension of counts to use to normalize the co-occurrence data by.
            Only used if 'score' is 'normalize'.
        """

        if score_type == 'association':
            if self.square:
                self.score = compute_association_index(
                    self.counts, self.terms['A'].counts, self.terms['A'].counts)
            else:
                self.score = compute_association_index(
                    self.counts, self.terms['A'].counts, self.terms['B'].counts)

        elif score_type == 'normalize':
            self.score = compute_normalization(
                self.counts, self.terms[dim].counts, dim)

        else:
            raise ValueError('Score type not understood.')


    def check_top(self, dim='A'):
        """Check the terms with the most articles.

        Parameters
        ----------
        dim : {'A', 'B'}, optional
            Which set of terms to check.
        """

        max_ind = np.argmax(self.terms[dim].counts)
        print("The most studied term is  {}  with  {}  articles.".format(
            wrap(self.terms[dim].labels[max_ind]),
            self.terms[dim].counts[max_ind]))


    def check_counts(self, dim='A'):
        """Check how many articles were found for each term.

        Parameters
        ----------
        dim : {'A', 'B'}, optional
            Which set of terms to check.
        """

        print("The number of documents found for each search term is:")
        for ind, term in enumerate(self.terms[dim].labels):
            print("  {:{twd}}   -   {:{nwd}.0f}".format(
                wrap(term), self.terms[dim].counts[ind],
                twd=get_max_length(self.terms[dim].labels, 2),
                nwd=get_max_length(self.terms[dim].counts)))


    def check_data(self, data_type='counts', dim='A'):
        """Prints out the highest value count or score for each term.

        Parameters
        ----------
        data_type : {'counts', 'score'}
            Which data type to use.
        dim : {'A', 'B'}, optional
            Which set of terms to check.
        """

        if data_type not in ['counts', 'score']:
            raise ValueError('Data type not understood - can not proceed.')
        if data_type == 'score' and self.score.size == 0:
            raise ValueError('Score is not computed - can not proceed.')

        # Set up which direction to act across
        dat = getattr(self, data_type) if dim == 'A' else getattr(self, data_type).T
        alt = 'B' if dim == 'A' and not self.square else 'A'

        # Loop through each term, find maximally associated term and print out
        for term_ind, term in enumerate(self.terms[dim].labels):

            # Find the index of the most common association for current term
            assoc_ind = np.argmax(dat[term_ind, :])

            print("For  {:{twd1}}  the highest association is  {:{twd2}}  with  {:{nwd}}".format(
                wrap(term), wrap(self.terms[alt].labels[assoc_ind]),
                dat[term_ind, assoc_ind],
                twd1=get_max_length(self.terms[dim].labels, 2),
                twd2=get_max_length(self.terms[alt].labels, 2),
                nwd='>10.0f' if data_type == 'counts' else '06.3f'))


    def drop_data(self, n_articles, dim='A'):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Minimum number of articles to keep each term.
        dim : {'A', 'B'}, optional
            Which set of terms to drop.
        """

        keep_inds = np.where(self.terms[dim].counts > n_articles)[0]

        self.terms[dim].terms = [self.terms[dim].terms[ind] for ind in keep_inds]
        self.terms[dim].counts = self.terms[dim].counts[keep_inds]

        if dim == 'A':
            self.counts = self.counts[keep_inds, :]
            self.score = self.score[keep_inds, :]
        if dim == 'B':
            self.counts = self.counts[:, keep_inds]
            self.score = self.score[:, keep_inds]
