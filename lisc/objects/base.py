"""Base object for LISC."""

from copy import deepcopy

from lisc.data.term import Term
from lisc.io import load_txt_file
from lisc.utils.base import flatten
from lisc.collect.terms import make_term, check_joiner, DEFAULT_TERM_JOINERS
from lisc.modutils.errors import InconsistentDataError

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
    has_terms : bool
        Whether the object has terms loaded.
    n_terms : int
        Number of terms.
    """

    def __init__(self):
        """Initialize Base object."""

        self.terms = list()
        self.inclusions = list()
        self.exclusions = list()
        self._labels = list()
        self._joiners = deepcopy(DEFAULT_TERM_JOINERS)


    def __getitem__(self, key):
        """Index into Base object, accessing Term.

        Parameters
        ----------
        key : str or int
            Label or index of the element to extract.
        """

        return self.get_term(self.get_index(key) if isinstance(key, str) else key)


    def __iter__(self):
        """Allow for iterating across the object by stepping through terms."""

        for ind in range(self.n_terms):
            yield self.get_term(ind)


    def copy(self):
        """Return a copy of the current object."""

        return deepcopy(self)


    @property
    def has_terms(self):
        """Indicator for if the object has terms."""

        return bool(self.terms)


    @property
    def n_terms(self):
        """How many terms are included in the object."""

        return len(self.terms)


    @property
    def labels(self):
        """The labels for each term."""

        if self.has_terms:
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


    def add_terms(self, terms, term_type=None, directory=None,
                  append=False, check_consistency=True):
        """Add terms to the object.

        Parameters
        ----------
        terms : list or dict or str
            Terms to add to the object.
            If list, assumed to be terms, which can be a list of str or a list of list of str.
            If dict, each key should reflect a term_type, and values the corresponding terms.
            If str, assumed to be a file name to load from.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to are being added.
        directory : SCDB or str, optional
            Folder or database object specifying the file location, if loading from file.
        append : boolean, optional, default: False
            Whether to append the new term(s) to any existing terms.
            If False, any prior terms are cleared prior to adding current term(s).
        check_consistency : bool, optional, default: True
            Whether to check the object for consistency after adding terms.

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

        if not term_type:
            if isinstance(terms, list) and isinstance(terms[0], Term):
                term_type = 'all'
            elif isinstance(terms, dict):
                for term_type, term_values in terms.items():
                    self.add_terms(term_values, term_type, None, append, check_consistency)
                return
            else:
                term_type = 'terms'

        if term_type == 'labels':
            self.add_labels(terms, directory, check_consistency)
            return

        if self.n_terms and not append:
            self.unload_terms(term_type, reset=False)

        if isinstance(terms, str):
            terms = load_txt_file(terms, directory)

        if isinstance(terms, Term):
            self._add_term(terms)

        else:

            for term in terms:

                if isinstance(term, str):
                    getattr(self, term_type).append([term])
                elif isinstance(term, list):
                    getattr(self, term_type).append(term)
                elif isinstance(term, Term):
                    self._add_term(term)

        self._check_labels()
        self._check_clusions()

        if check_consistency:
            self._check_term_consistency()


    def add_labels(self, labels, directory=None, check_consistency=True):
        """Add the given list of strings as labels for the terms.

        Parameters
        ----------
        labels : list of str or str
            Labels for each term to add to the object.
            If list, is assumed to be labels.
            If str, is assumed to be a file name to load from.
        directory : SCDB or str, optional
            Folder or database object specifying the file location, if loading from file.
        check_consistency : bool, optional, default: True
            Whether to check the object for consistency after adding labels.
        """

        # If there are previously loaded labels, then clear them
        if self._labels != [None] * len(self._labels):
            self.unload_labels()

        # If the input is a string, load the requested file
        if isinstance(labels, str):
            labels = load_txt_file(labels, directory, split_elements=False)

        # Add the labels to the object, and check for consistency, if terms are already loaded
        self._labels = labels
        self._check_labels()
        if check_consistency:
            self._check_term_consistency()


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

            if isinstance(label[0], int):
                label = list(reversed(sorted(label)))

            for element in label:
                self.drop_term(element)

        ind = self.get_index(label) if isinstance(label, str) else label
        for attr in ['terms', '_labels', 'inclusions', 'exclusions']:
            if getattr(self, attr):
                getattr(self, attr).pop(ind)


    def unload_terms(self, term_type='terms', reset=True, verbose=True):
        """Completely unload terms from the object.

        Attributes
        ----------
        term_type : {'terms', 'inclusions', 'exclusions', 'labels', 'all'}
            Which type of terms to unload.
        reset : bool, optional, default: True
            Whether to reset in/exclusions to empty lists.
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
            for attr in ['terms', 'inclusions', 'exclusions', 'labels']:
                self.unload_terms(attr)

        elif term_type == 'labels':
            self.unload_labels(verbose=verbose)

        else:
            if verbose and flatten(getattr(self, term_type)):
                print('Unloading {}.'.format(term_type))
            setattr(self, term_type, list())

        if reset:
            self._check_clusions()


    def unload_labels(self, verbose=True):
        """Unload labels from the object."""

        if verbose:
            print('Unloading labels.')
        self._set_none_labels()


    def make_search_term(self, label):
        """Create the combined search term for a selected term.

        Parameters
        ----------
        label : str or int
            The requested term.
            If str, is the label of the term.
            If int, is used as the index of the term.
        """

        return make_term(self[label], joiners=self._joiners)


    def set_joiners(self, search=None, inclusions=None, exclusions=None):
        """Set joiners to use, specified for each term type.

        Parameters
        ----------
        search, inclusions, exclusions : {'OR', 'AND', 'NOT'}
            Joiner to use to combine terms, for search, inclusions, and exclusions terms.
        """

        input_joiners = {
            'search' : search,
            'inclusions' : inclusions,
            'exclusions' : exclusions,
        }

        for label, joiner in input_joiners.items():
            if joiner:
                check_joiner(joiner)
                self._joiners[label] = joiner


    def _set_none_labels(self):
        """Set labels as None."""

        self._labels = [None] * self.n_terms


    def _check_term_consistency(self):
        """Check if loaded term definitions are consistent."""

        if self.n_terms != len(self.inclusions):
            raise InconsistentDataError('There is a mismatch in number of inclusions and terms.')

        if self.n_terms != len(self.exclusions):
            raise InconsistentDataError('There is a mismatch in number of exclusions and terms.')

        if self.n_terms != len(self._labels):
            raise InconsistentDataError('There is a mismatch in number of labels and terms.')


    def _check_labels(self):
        """Check loaded terms and labels, and set None labels if needed."""

        if self.has_terms and (not self._labels or self._labels == [None] * len(self._labels)):
            self._set_none_labels()

        if not len(self.labels) == len(set(self.labels)):
            raise InconsistentDataError('Not all labels are unique. Labels must be unique.')


    def _check_clusions(self):
        """Check loaded in/exclusion terms, and set as null lists if needed."""

        if not flatten(self.inclusions):
            self.inclusions = [[]] * self.n_terms
        if not flatten(self.exclusions):
            self.exclusions = [[]] * self.n_terms


    def _add_term(self, term):
        """Add term information from a Term object.

        Parameters
        ----------
        term : Term
            Term information.
        """

        self.terms.append(term.search)
        self.inclusions.append(term.inclusions)
        self.exclusions.append(term.exclusions)
        if term.label != term.search[0]:
            self._labels.append(term.label)
        else:
            self._labels.append(None)
