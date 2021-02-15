"""Base object for LISC."""

from lisc.data.term import Term
from lisc.utils.io import load_txt_file
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

class Base():
    """A class for the base object for LISC collections and analyses.

    Attributes
    ----------
    terms : list of list of str
        Terms words.
    labels : list of str
        Label to reference each term.
    inclusions : list of str
        Inclusion words for each term.
    exclusions : list of list str
        Exclusion words for each term.
    has_data : bool
        Whether there is any terms and/or data loaded.
    n_terms : int
        Number of terms.
    """

    def __init__(self):
        """Initialize Base object."""

        self.terms = list()
        self.inclusions = list()
        self.exclusions = list()
        self._labels = list()


    def __getitem__(self, key):
        """Index into Base object, accessing Term."""

        return self.get_term(self.get_index(key))


    @property
    def has_data(self):
        """Indicator for if the object has data."""

        return bool(self.terms)


    @property
    def n_terms(self):
        """How many terms are included in the object."""

        return len(self.terms)


    @property
    def labels(self):
        """The labels for each term."""

        if self.has_data:
            return [label if label else term[0] for label, term in zip(self._labels, self.terms)]
        else:
            return self._labels


    def get_index(self, label):
        """Get the index for a specified search term.

        Parameters
        ----------
        label : str
            The label of the search term.

        Returns
        -------
        ind : int
            The index of the requested search term.

        Raises
        ------
        IndexError
            If the requested term label is not found.
        """

        try:
            ind = self.labels.index(label)
        except ValueError:
            raise IndexError('Requested key not available in object.')

        return ind


    def get_term(self, label):
        """Get a search term from the object.

        Parameters
        ----------
        label : str or int
            The requested term.
            If str, is the label of the term.
            If int, is used as the index of the term.

        Returns
        -------
        term : Term
            The full search term definition.
        """

        ind = self.get_index(label) if isinstance(label, str) else label
        term = Term(self.labels[ind], self.terms[ind], self.inclusions[ind], self.exclusions[ind])

        return term


    def add_terms(self, terms, term_type='terms', directory=None):
        """Add the given list of strings as terms to use.

        Parameters
        ----------
        terms : list or str
            Terms to add to the object.
            If list, assumed to be terms, which can be a list of str or a list of list of str.
            If str, assumed to be a file name to load from.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to are being added.
        directory : SCDB or str, optional
            Folder or database object specifying the file location, if loading from file.

        Examples
        --------
        Add search terms, from a list:

        >>> base = Base()
        >>> base.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])

        Add inclusion terms, from a list:

        >>> base.add_terms([[], ['brain'], [], []], term_type='inclusions')

        Add exclusion terms, from a list:

        >>> base.add_terms([['prefrontal'], [], [], []], term_type='exclusions')
        """

        self.unload_terms(term_type)

        if isinstance(terms, str):
            terms = load_txt_file(terms, directory)

        for term in terms:
            getattr(self, term_type).append(self._check_type(term))

        self._check_term_consistency()
        self._check_label_consistency()


    def add_labels(self, labels, directory=None):
        """Add the given list of strings as labels for the terms.

        Parameters
        ----------
        labels : list of str or str
            Labels for each term to add to the object.
            If list, is assumed to be labels.
            If str, is assumed to be a file name to load from.
        directory : SCDB or str, optional
            Folder or database object specifying the file location, if loading from file.
        """

        # If there are previously loaded labels, then clear them
        if self._labels != [None] * len(self._labels):
            self.unload_labels()

        # If the input is a string, load the requested file
        if isinstance(labels, str):
            labels = load_txt_file(labels, directory, split_elements=False)

        # Add the labels to the object, and check for consistency, if terms are already loaded
        self._labels = labels
        self._check_label_consistency()


    def check_terms(self, term_type='terms'):
        """Print out the current list of terms.

        Attributes
        ----------
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to use.

        Examples
        --------
        Check added terms:

        >>> base = Base()
        >>> base.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> base.check_terms() # doctest: +NORMALIZE_WHITESPACE
        List of terms used:
        <BLANKLINE>
        frontal lobe    : frontal lobe
        temporal lobe   : temporal lobe
        parietal lobe   : parietal lobe
        occipital lobe  : occipital lobe
        """

        print('List of {} used: \n'.format(term_type))

        width = len(max(self.labels, key=len))
        for label, terms in zip(self.labels, getattr(self, term_type)):
            print('{:{width}s}  : '.format(label, width=width) + ", ".join(term for term in terms))


    def drop_term(self, label):
        """Drop specified term(s) from the object.

        Parameters
        ----------
        label : str or int or list
            The label of the term to drop.
            If str, is the label of the term.
            If int, is used as the index of the term.
            If list, drops each element of the list.
        """

        if isinstance(label, list):
            for ll in label:
                self.drop_term(ll)

        ind = self.get_index(label) if isinstance(label, str) else label
        for attr in ['terms', '_labels', 'inclusions', 'exclusions']:
            getattr(self, attr).pop(ind)


    def unload_terms(self, term_type='terms', verbose=True):
        """Completely unload terms from the object.

        Attributes
        ----------
        term_type : {'terms', 'inclusions', 'exclusions', 'all'}
            Which type of terms to use.
        verbose : bool, optional
            Whether to be verbose in printing out any changes.

        Examples
        --------
        Unload added terms:

        >>> base = Base()
        >>> base.add_terms(['frontal lobe', 'temporal lobe', 'parietal lobe', 'occipital lobe'])
        >>> base.unload_terms()
        Unloading terms.
        """

        if term_type == 'all':
            for term_type in ['terms', 'inclusions', 'exclusions', 'labels']:
                self.unload_terms(term_type)

        elif term_type == 'labels':
            self.unload_labels(verbose=verbose)

        else:
            if getattr(self, term_type):
                if verbose:
                    print('Unloading {}.'.format(term_type))
                setattr(self, term_type, list())


    def unload_labels(self, verbose=True):
        """Unload labels from the object."""

        if verbose:
            print('Unloading labels.')
        self._set_none_labels()


    def _set_none_labels(self):
        """Set labels as None."""

        self._labels = [None] * self.n_terms


    def _check_term_consistency(self):
        """Check if loaded terms and inclusions/exclusions are consistent lengths."""

        if self.inclusions and self.n_terms != len(self.inclusions):
            raise InconsistentDataError('There is a mismatch in number of inclusions and terms.')

        if self.exclusions and self.n_terms != len(self.exclusions):
            raise InconsistentDataError('There is a mismatch in number of exclusions and terms.')


    def _check_label_consistency(self):
        """Check if loaded terms and labels are consistent lengths."""

        # If terms are loaded, and no labels are available, set none labels
        if self.has_data and (not self._labels or self._labels == [None] * len(self._labels)):
            self._set_none_labels()

        # If terms are loaded, check the consistency between terms and labels
        if self.has_data and self.n_terms != len(self._labels):
            raise InconsistentDataError('There is a mismatch in number of labels and terms.')


    @staticmethod
    def _check_type(term):
        """Check type of input term, and return as a list.

        Parameters
        ----------
        term : str or list of str
            New term to add to the object.

        Returns
        -------
        list of str
            New term, set as a list.
        """

        if isinstance(term, str):
            return [term]
        elif isinstance(term, list):
            return term
