"""Base object for LISC."""

from lisc.utils.io import load_terms_file
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

    @property
    def has_data(self):
        return bool(self.terms)

    @property
    def n_terms(self):
        return len(self.terms)

    @property
    def labels(self):
        return [term[0] for term in self.terms]


    def add_terms(self, terms, term_type='terms'):
        """Add the given list of strings as terms to use.

        Parameters
        ----------
        terms : list of str or list of list of str
            List of terms to be used.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to use.
        """

        self.unload_terms(term_type)
        for term in terms:
            getattr(self, term_type).append(self._check_type(term))
        self._check_term_consistency()


    def add_terms_file(self, f_name, term_type='terms', directory=None):
        """Load terms from a text file.

        Parameters
        ----------
        f_name : str
            File name to load terms from.
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to use.
        directory : SCDB or str or None, optional
            Folder or database object specifying the file location.
        """

        terms = load_terms_file(f_name, directory)
        self.add_terms(terms, term_type)


    def check_terms(self, term_type='terms'):
        """Print out the current list of terms.

        Attributes
        ----------
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to use.
        """

        print('List of {} used: \n'.format(term_type))

        width = len(max(self.labels, key=len))
        for label, terms in zip(self.labels, getattr(self, term_type)):
            print('{:{width}s}  : '.format(label, width=width) + ", ".join(term for term in terms))


    def unload_terms(self, term_type='terms'):
        """Unload the current set of terms.

        Attributes
        ----------
        term_type : {'terms', 'inclusions', 'exclusions'}
            Which type of terms to use.
        """

        if getattr(self, term_type):

            print('Unloading previous {} words.'.format(term_type))
            setattr(self, term_type, list())


    def _check_term_consistency(self):
        """Check if the loaded terms and inclusions/exclusions are consistent size."""

        if self.inclusions and self.n_terms != len(self.inclusions):
            raise InconsistentDataError('Mismatch in number of inclusions and terms!')

        if self.exclusions and self.n_terms != len(self.exclusions):
            raise InconsistentDataError('Mismatch in number of exclusions and terms!')


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
