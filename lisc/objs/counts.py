"""Class for Count analysis: analyses of co-occurences data."""

import numpy as np

from lisc.objs.base import Base
from lisc.scrape import scrape_counts

###################################################################################################
###################################################################################################

class Counts():
    """This is a class for counting co-occurence of pre-specified terms list(s).

    Attributes
    ----------
    terms : dict()
        Search terms to use.
    dat_numbers : 2d array
        The numbers of papers found for each combination of terms.
    dat_percent : 2d array
        The percentage of papers for each term that include the corresponding term.
    square : bool
        Whether the count data matrix is symetrical.
    """

    def __init__(self):
        """Initialize LISC Count() object."""

        # Initialize dictionary to store search terms
        self.terms = dict()
        for dat in ['A', 'B']:
            self.terms[dat] = Base()
            self.terms[dat].counts = np.zeros(0, dtype=int)

        # Initialize data output variables
        self.dat_numbers = np.zeros(0)
        self.dat_percent = np.zeros(0)
        self.square = bool()

        # Initialize dictionary to store db info
        self.meta_data = dict()


    def set_terms(self, terms, dim='A'):
        """Sets the given list of strings as terms to use.

        Parameters
        ----------
        terms : list of str OR list of list of str
            List of terms to be used.
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        self.terms[dim].set_terms(terms)
        self.terms[dim].counts = np.zeros(self.terms[dim].n_terms, dtype=int)


    def set_exclusions(self, exclusions, dim='A'):
        """Sets the given list of strings as exclusion words.

        Parameters
        ----------
        exclusions : list of str OR list of list of str
            List of exclusion words to be used.
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        self.terms[dim].set_exclusions(exclusions)


    def run_scrape(self, db='pubmed', field='TIAB', api_key=None, verbose=False):
        """Scrape co-occurence data.

        Parameters
        ----------
        db : str, optional (default: 'pubmed')
            Which pubmed database to use.
        field : str, optional, default: 'TIAB'
            Field to search for term within.
            Defaults to 'TIAB', which is Title/Abstract.
        api_key : str
            An API key for a NCBI account.
        verbose : bool, optional (default=False)
            Whether to print out updates.
        """

        # Run single list of terms against themselves - 'square'
        if not self.terms['B'].has_dat:
            self.dat_numbers, self.dat_percent, self.terms['A'].counts, \
                _, self.meta_data = \
                    scrape_counts(
                        terms_lst_a=self.terms['A'].terms,
                        excls_lst_a=self.terms['A'].exclusions,
                        db=db, field=field, api_key=api_key,
                        verbose=verbose)
            self.square = True

        # Run two different sets of terms
        else:
            self.dat_numbers, self.dat_percent, self.terms['A'].counts, \
                self.terms['B'].counts, self.meta_data = \
                    scrape_counts(
                        terms_lst_a=self.terms['A'].terms,
                        excls_lst_a=self.terms['A'].exclusions,
                        terms_lst_b=self.terms['B'].terms,
                        excls_lst_b=self.terms['B'].exclusions,
                        db=db, field=field, api_key=api_key,
                        verbose=verbose)
            self.square = False


    def check_cooc(self, dim='A'):
        """"Prints out the most frequent association for each term.

        Parameters
        ----------
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        # Set up which direction to act across
        dat = self.dat_percent if dim == 'A' else self.dat_percent.T
        alt = 'B' if dim == 'A' and not self.square else 'A'

        # Loop through each term, find maximally associated term term and print out
        for term_ind, term in enumerate(self.terms[dim].labels):

            # Find the index of the most common association for current term
            assoc_ind = np.argmax(dat[term_ind, :])

            # Print out the results
            print("For the  {:12} the most common association is \t {:18} with \t %{:05.2f}"
                  .format(term, self.terms[alt].labels[assoc_ind], \
                  dat[term_ind, assoc_ind]*100))


    def check_top(self, dim='A'):
        """Check the terms with the most papers.

        Parameters
        ----------
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        # Find and print the term for which the most papers were found
        print("The most studied term is  {:12}  with {:8.0f} papers"
              .format(self.terms[dim].labels[np.argmax(self.terms[dim].counts)], \
              self.terms[dim].counts[np.argmax(self.terms[dim].counts)]))


    def check_counts(self, dim='A'):
        """Check how many papers found for each term.

        Parameters
        ----------
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        # Check counts for all terms
        for ind, term in enumerate(self.terms[dim].labels):
            print('{:12} - {:8.0f}'.format(term, self.terms[dim].counts[ind]))


    def drop_data(self, n_articles, dim='A'):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Mininum number of articles to keep each term.
        dim : 'A' or 'B', optional
            Which set of terms to operate upon.
        """

        keep_inds = np.where(self.terms[dim].counts > n_articles)[0]

        self.terms[dim].terms = [self.terms[dim].terms[ind] for ind in keep_inds]
        self.terms[dim].labels = [self.terms[dim].labels[ind] for ind in keep_inds]
        self.terms[dim].counts = self.terms[dim].counts[keep_inds]

        self.terms[dim].n_terms = len(self.terms[dim].terms)

        if dim == 'A':
            self.dat_numbers = self.dat_numbers[keep_inds, :]
            self.dat_percent = self.dat_percent[keep_inds, :]
        if dim == 'B':
            self.dat_numbers = self.dat_numbers[:, keep_inds]
            self.dat_percent = self.dat_percent[:, keep_inds]
