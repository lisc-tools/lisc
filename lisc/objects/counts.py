"""Class for collection and analyses of co-occurrences data."""

from copy import deepcopy
from collections import defaultdict

import numpy as np

from lisc.objects.base import Base
from lisc.utils.base import wrap, get_max_length
from lisc.collect import collect_counts
from lisc.analysis.counts import (compute_normalization, compute_association_index,
                                  compute_similarity)

###################################################################################################
###################################################################################################

class Counts1D(Base):
    """A class for collecting counts data for specified terms.

    Attributes
    ----------
    counts : 1d array
        The number of articles found for each term.
    meta_data : MetaData
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Counts1D object."""

        Base.__init__(self)

        self.counts = np.zeros(0)
        self.meta_data = None


    def __getitem__(self, item):
        """Index into Counts1D object, accessing count.

        Parameters
        ----------
        keys : str or int
            Label or index to access.
        """

        ind = self.get_index(item) if isinstance(item, str) else item

        return self.counts[ind]


    @property
    def has_data(self):
        """Indicator for if the object has collected data."""

        return np.any(self.counts)


    def run_collection(self, db='pubmed', field='TIAB', api_key=None, logging=None,
                       directory=None, verbose=False, **eutils_kwargs):
        """Collect counts data.

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
        **eutils_kwargs
            Additional settings for the EUtils API.

        Examples
        --------
        Collect counts data from added terms:

        >>> counts = Counts1D()
        >>> counts.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> counts.run_collection() # doctest: +SKIP
        """

        self.counts, self.meta_data = collect_counts(
            terms_a=self.terms, inclusions_a=self.inclusions,
            exclusions_a=self.exclusions, labels_a=self.labels,
            db=db, field=field, api_key=api_key, collect_coocs=False,
            logging=logging, directory=directory, verbose=verbose, **eutils_kwargs)


    def check_top(self):
        """Check the term with the most articles."""

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        max_ind = np.argmax(self.counts)
        print("The most studied term is  {}  with  {}  articles.".format(
            wrap(self.labels[max_ind]), self.counts[max_ind]))


    def check_counts(self):
        """Check how many articles were found for each term."""

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        # Calculate widths for printing
        twd = get_max_length(self.labels, 2)
        nwd = get_max_length(self.counts)

        print("The number of documents found for each search term is:")
        for ind, term in enumerate(self.labels):
            print("  {:{twd}}   -   {:{nwd}.0f}".format(
                wrap(term), self.counts[ind], twd=twd, nwd=nwd))


    def drop_data(self, n_articles):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Minimum number of articles required to keep each term.
        """

        # Finds the indices of the terms with enough data to keep
        keep_inds = np.where(self.counts >= n_articles)[0]

        # Drop terms that do not have enough data
        self.terms = [self.terms[ind] for ind in keep_inds]
        self._labels = [self._labels[ind] for ind in keep_inds]
        self.counts = self.counts[keep_inds]


class Counts():
    """A class for collecting and analyzing co-occurrence data for specified terms list(s).

    Attributes
    ----------
    terms : dict
        Search terms to use.
    counts : 2d array
        The number of articles found for each combination of terms.
    score : 2d array
        A transformed 'score' of co-occurrence data.
        This may be normalized count data, or a similarity or association measure.
    score_info : dict
        Information about the computed score data.
    square : bool
        Whether the count data matrix is symmetrical.
    meta_data : MetaData
        Meta data information about the data collection.
    """

    def __init__(self):
        """Initialize LISC Counts object."""

        # Initialize dictionary to store search terms
        self.terms = dict()
        for dim in ['A', 'B']:
            self.terms[dim] = Base()
            self.terms[dim].counts = np.zeros(0, dtype=int)

        self.counts = np.zeros(0)
        self.score = np.zeros(0)
        self.score_info = {}
        self.square = bool()
        self.meta_data = None


    def __getitem__(self, keys):
        """Index into Counts object, accessing count.

        Parameters
        ----------
        keys : list of (str, int)
            Labels or indices for the data to access.
        """

        if not self.has_data:
            raise IndexError('No data is available - cannot proceed.')

        if not isinstance(keys, (tuple, list)):
            return ValueError('Input keys do not match the object.')

        ind0 = self.terms['A'].get_index(keys[0]) if isinstance(keys[0], str) else keys[0]
        ind1 = self.terms['B' if self.terms['B'].terms else 'A'].get_index(keys[1]) \
            if isinstance(keys[1], str) else keys[1]

        return self.counts[ind0, ind1]


    def copy(self):
        """Return a copy of the current object."""

        return deepcopy(self)


    @property
    def has_data(self):
        """Indicator for if the object has collected data."""

        return np.any(self.counts)


    def add_terms(self, terms, term_type='terms', directory=None, dim='A'):
        """Add search terms to the object.

        Parameters
        ----------
        terms : list or dict or str
            Terms to add to the object.
            If list, assumed to be terms, which can be a list of str or a list of list of str.
            If dict, each key should reflect a term_type, and values the corresponding terms.
            If str, assumed to be a file name to load from.
        term_type : {'terms', 'inclusions', 'exclusions'}, optional
            Which type of terms are being added.
        directory : SCDB or str, optional
            A string or object containing a file path.
        dim : {'A', 'B'}, optional
            Which set of terms to add.

        Examples
        --------
        Add one set of terms, from a list:

        >>> counts = Counts()
        >>> counts.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])

        Add a second set of terms, from a list:

        >>> counts.add_terms(['attention', 'perception'], dim='B')

        Add some exclusion words, for the second set of terms, from a list:

        >>> counts.add_terms(['', 'extrasensory'], term_type='exclusions', dim='B')
        """

        self.terms[dim].add_terms(terms,
                                  term_type if not isinstance(terms, dict) else None,
                                  directory)
        if term_type == 'terms':
            self.terms[dim].counts = np.zeros(self.terms[dim].n_terms, dtype=int)


    def add_labels(self, terms, directory=None, dim='A'):
        """Add labels for terms to the object.

        Parameters
        ----------
        labels : list of str or str
            Labels for each term to add to the object.
            If list, is assumed to be labels.
            If str, is assumed to be a file name to load from.
        directory : SCDB or str, optional
            Folder or database object specifying the file location, if loading from file.
        dim : {'A', 'B'}, optional
            Which set of labels to add.
        """

        self.terms[dim].add_labels(terms, directory)


    def run_collection(self, db='pubmed', field='TIAB', api_key=None, logging=None,
                       directory=None, verbose=False, **eutils_kwargs):
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
        **eutils_kwargs
            Additional settings for the EUtils API.

        Examples
        --------
        Collect co-occurrence data from added terms, across one set of terms:

        >>> counts = Counts()
        >>> counts.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> counts.run_collection() # doctest: +SKIP

        Collect co-occurrence data from added terms, across two sets of terms:

        >>> counts = Counts()
        >>> counts.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> counts.add_terms(['attention', 'perception', 'cognition'], dim='B')
        >>> counts.run_collection() # doctest: +SKIP
        """

        # Run single list of terms against themselves, in 'square' mode
        if not self.terms['B'].has_terms:
            self.square = True
            self.counts, self.terms['A'].counts, self.meta_data = collect_counts(
                terms_a=self.terms['A'].terms,
                inclusions_a=self.terms['A'].inclusions,
                exclusions_a=self.terms['A'].exclusions,
                labels_a=self.terms['A'].labels,
                db=db, field=field, api_key=api_key,
                logging=logging, directory=directory,
                verbose=verbose, **eutils_kwargs)

        # Run two different sets of terms
        else:
            self.square = False
            self.counts, term_counts, self.meta_data = collect_counts(
                terms_a=self.terms['A'].terms,
                inclusions_a=self.terms['A'].inclusions,
                exclusions_a=self.terms['A'].exclusions,
                labels_a=self.terms['A'].labels,
                terms_b=self.terms['B'].terms,
                inclusions_b=self.terms['B'].inclusions,
                exclusions_b=self.terms['B'].exclusions,
                labels_b=self.terms['B'].labels,
                db=db, field=field, api_key=api_key,
                logging=logging, directory=directory,
                verbose=verbose, **eutils_kwargs)
            self.terms['A'].counts, self.terms['B'].counts = term_counts


    def compute_score(self, score_type='association', dim='A', return_result=False):
        """Compute a score, such as an index or normalization, of the co-occurrence data.

        Parameters
        ----------
        score_type : {'association', 'normalize', 'similarity'}, optional
            The type of score to apply to the co-occurrence data.
        dim : {'A', 'B'}, optional
            Which dimension of counts to use to normalize by or compute similarity across.
            Only used if 'score' is 'normalize' or 'similarity'.
        return_result : bool, optional, default: False
            Whether to return the computed result.

        Examples
        --------
        Compute association scores of co-occurrence data collected for two lists of terms:

        >>> counts = Counts()
        >>> counts.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> counts.add_terms(['attention', 'perception'], dim='B')
        >>> counts.run_collection() # doctest: +SKIP
        >>> counts.compute_score() # doctest: +SKIP

        Once you have co-occurrence scores calculated, you might want to plot this data.

        You can plot the results as a matrix:

        >>> from lisc.plts.counts import plot_matrix  # doctest:+SKIP
        >>> plot_matrix(counts)  # doctest:+SKIP

        And/or as a clustermap:

        >>> from lisc.plts.counts import plot_clustermap  # doctest:+SKIP
        >>> plot_clustermap(counts)  # doctest:+SKIP

        And/or as a dendrogram:

        >>> from lisc.plts.counts import plot_dendrogram  # doctest:+SKIP
        >>> plot_dendrogram(counts)  # doctest:+SKIP
        """

        # Clear any previously computed score
        self.clear_score()

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        if score_type == 'association':
            if self.square:
                self.score = compute_association_index(
                    self.counts, self.terms['A'].counts, self.terms['A'].counts)
            else:
                self.score = compute_association_index(
                    self.counts, self.terms['A'].counts, self.terms['B'].counts)

        elif score_type == 'normalize':
            self.score = compute_normalization(self.counts, self.terms[dim].counts, dim)

        elif score_type == 'similarity':
            self.score = compute_similarity(self.counts, dim=dim)

        else:
            raise ValueError('Score type not understood.')

        self.score_info['type'] = score_type
        if score_type in ['normalize', 'similarity']:
            self.score_info['dim'] = dim

        if return_result:
            return deepcopy(self.score)


    def clear_score(self):
        """Clear any previously computed score."""

        self.score = np.zeros(0)
        self.score_info = {}


    def check_top(self, dim='A'):
        """Check the terms with the most articles.

        Parameters
        ----------
        dim : {'A', 'B', 'both'}, optional
            Which set of terms to check.

        Examples
        --------
        Print which term has the most articles (assuming `counts` already has data):

        >>> counts.check_top() # doctest: +SKIP
        """

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        if dim == 'both':

            self.check_top('A')
            print('\n')
            self.check_top('B')

        else:

            max_ind = np.argmax(self.terms[dim].counts)
            print("The most studied term is  {}  with  {}  articles.".format(
                wrap(self.terms[dim].labels[max_ind]),
                self.terms[dim].counts[max_ind]))


    def check_counts(self, dim='A'):
        """Check how many articles were found for each term.

        Parameters
        ----------
        dim : {'A', 'B', 'both'}
            Which set of terms to check.

        Examples
        --------
        Print the number of articles found for each term (assuming `counts` already has data):

        >>> counts.check_counts() # doctest: +SKIP
        """

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        if dim == 'both':

            self.check_counts('A')
            print('\n')
            self.check_counts('B')

        else:

            # Calculate widths for printing
            twd = get_max_length(self.terms[dim].labels, 2)
            nwd = get_max_length(self.terms[dim].counts)

            print("The number of documents found for each search term is:")
            for ind, term in enumerate(self.terms[dim].labels):
                print("  {:{twd}}   -   {:{nwd}.0f}".format(
                    wrap(term), self.terms[dim].counts[ind], twd=twd, nwd=nwd))


    def check_data(self, data_type='counts', dim='A'):
        """Prints out the highest value count or score for each term.

        Parameters
        ----------
        data_type : {'counts', 'score'}
            Which data type to use.
        dim : {'A', 'B', 'both'}, optional
            Which set of terms to check.

        Examples
        --------
        Print the highest count for each term (assuming `counts` already has data):

        >>> counts.check_data() # doctest: +SKIP

        Print the highest score value for each term (assuming `counts` already has data):

        >>> counts.check_data(data_type='score') # doctest: +SKIP
        """

        if not self.has_data:
            raise ValueError('No data is available - cannot proceed.')

        if data_type not in ['counts', 'score']:
            raise ValueError('Data type not understood - can not proceed.')
        if data_type == 'score':
            if self.score.size == 0:
                raise ValueError('Score is not computed - can not proceed.')
            if self.score_info['type'] == 'similarity':
                raise ValueError('Cannot check value counts for similarity score.')

        if dim == 'both':

            self.check_data(data_type, 'A')
            print('\n')
            self.check_data(data_type, 'B')

        else:

            # Set up which direction to act across
            data = getattr(self, data_type)
            data = data.T if dim == 'B' else data
            alt = 'B' if dim == 'A' and not self.square else 'A'

            # Calculate widths for printing
            twd1 = get_max_length(self.terms[dim].labels, 2)
            twd2 = get_max_length(self.terms[alt].labels, 2)
            nwd = '>10.0f' if data_type == 'counts' else '06.3f'

            # Loop through each term, find maximally associated term and print out
            for term_ind, term in enumerate(self.terms[dim].labels):

                # Find the index of the most common association for current term
                assoc_ind = np.argmax(data[term_ind, :])

                print("For  {:{twd1}}  the highest association is  {:{twd2}}  with  {:{nwd}}".format(
                    wrap(term), wrap(self.terms[alt].labels[assoc_ind]),
                    data[term_ind, assoc_ind], twd1=twd1, twd2=twd2, nwd=nwd))


    def drop_data(self, n_articles, dim='A', value='count'):
        """Drop terms based on number of article results.

        Parameters
        ----------
        n_articles : int
            Minimum number of articles required to keep each term.
        dim : {'A', 'B'}, optional
            Which set of terms to drop.
        value : {'count', 'coocs'}
            Which data count to drop based on:
                'count' : drops based on the total number of articles per term
                'coocs' : drops based on the co-occurrences, if all values are below `n_articles`

        Notes
        -----
        This will drop any computed scores, as they may not be accurate after dropping data.

        Examples
        --------
        Drop terms with less than 20 articles (assuming `counts` already has data):

        >>> counts.drop_data(20) # doctest: +SKIP
        """

        self.clear_score()

        if dim == 'both':

            self.drop_data(n_articles, 'A', value)
            self.drop_data(n_articles, 'B', value)

        else:

            dim_inds = {'A' : 1, 'B' : 0}

            # Get set of indices to drop & drop them from the object
            if value == 'count':
                drop_inds = np.where(self.terms[dim].counts < n_articles)[0]
            elif value == 'coocs':
                drop_inds = list(np.where(np.all(self.counts < n_articles, dim_inds[dim]))[0])

            self._drop_terms(drop_inds, dim)


    def set_joiners(self, search=None, inclusions=None, exclusions=None, dim='A'):
        """Set joiners to use, specified for each term type.

        Parameters
        ----------
        search, inclusions, exclusions : {'OR', 'AND', 'NOT'}
            Joiner to use to combine terms, for search, inclusions, and exclusions terms.
        dim : {'A', 'B'}, optional
            Which set of terms to set joiners for.
        """

        self.terms[dim].set_joiners(search, inclusions, exclusions)


    def _drop_terms(self, drop_inds, dim):
        """Sub-function to drop terms from object.

        Parameters
        ----------
        drop_inds : list of int
            Indices of terms to drop.
        dim : {'A', 'B'}
            Which dim to drop terms from.
        """

        # Invert to indices of the terms to keep
        keep_inds = np.delete(np.arange(self.terms[dim].n_terms), drop_inds)

        # Drop terms that do not have enough data
        self.terms[dim].terms = [self.terms[dim].terms[ind] for ind in keep_inds]
        self.terms[dim]._labels = [self.terms[dim]._labels[ind] for ind in keep_inds]
        self.terms[dim].counts = self.terms[dim].counts[keep_inds]

        # Create an inds dictionary that defaults to all-index slice
        inds = defaultdict(lambda: np.s_[:])

        # Set a flipper dictionary, to flip inds if needed
        flip_inds = {'A' : 'B', 'B' : 'A'}

        # If square, set both dims, and do array orgs needed for fancy indexing
        if self.square:
            inds[dim] = keep_inds[:, None]
            inds[flip_inds[dim]] = keep_inds
        else:
            inds[dim] = keep_inds

        # Drop raw count data for terms without enough data
        self.counts = self.counts[inds['A'], inds['B']]
