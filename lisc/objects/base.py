"""Base object for LISC."""

from lisc.core.io import load_terms_file
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

class Base():
    """Base class for LISC analyses.

    Attributes
    ----------
    terms : list of list of str
        Terms words.
    labels : list of str
        Label to reference each term.
    exclusions : list of list str
        Exclusion words for each term, used to avoid unwanted articles.
    has_data : bool
        Whether there is any terms and/or data loaded.
    n_terms : int
        Number of terms.
    """

    def __init__(self):
        """Initialize Base() object."""

        self.terms = list()
        self.labels = list()
        self.exclusions = list()


    @property
    def has_data(self):
        return bool(self.terms)


    @property
    def n_terms(self):
        return len(self.terms)


    def set_terms(self, terms):
        """Sets the given list of strings as terms to use.

        Parameters
        ----------
        terms : list of str OR list of list of str
            List of terms to be used.
        """

        self.unload_terms()

        for term in terms:
            self.terms.append(self._check_type(term))
        self.get_term_labels()


    def set_terms_file(self, f_name, folder=None):
        """Load terms from a text file.

        Parameters
        ----------
        f_name : str
            File name to load terms from.
        folder : SCDB or str or None
            A string or object containing a file path.
        """

        self.unload_terms()

        terms = load_terms_file(f_name, folder)

        for term in terms:
            self.terms.append(term.split(','))
        self.get_term_labels()


    def check_terms(self):
        """Print out the current list of terms."""

        # Print out header and all term words
        print('List of terms used: \n')
        for terms_ls in self.terms:
            print(", ".join(term for term in terms_ls))


    def unload_terms(self):
        """Unload the current set of terms."""

        if self.terms:

            print('Unloading previous terms words.')
            self.terms = list()


    def get_term_labels(self):
        """Get term labels."""

        self.labels = [term[0] for term in self.terms]


    def set_exclusions(self, exclusions):
        """Sets the given list of strings as exclusion words.

        Parameters
        ----------
        exclusions : list of str OR list of list of str
            List of exclusion words to be used.
        """

        self.unload_exclusions()

        for exclude in exclusions:
            self.exclusions.append(self._check_type(exclude))

        if len(exclusions) != self.n_terms:
            raise InconsistentDataError('Mismatch in number of exclusions and terms!')


    def set_exclusions_file(self, f_name, folder=None):
        """Load exclusion words from a text file.

        Parameters
        ----------
        f_name : str
            File name to load exclusion terms from.
        folder : SCDB or str or None
            A string or object containing a file path.
        """

        self.unload_exclusions()
        exclusions = load_terms_file(f_name, folder)

        if len(exclusions) != self.n_terms:
            raise InconsistentDataError('Mismatch in number of exclusions and terms!')

        for exclusion in exclusions:
            self.exclusions.append(exclusion.split(','))


    def check_exclusions(self):
        """Print out the current list of exclusion words."""

        print('List of exclusion words used: \n')
        for lab, excs in zip(self.labels, self.exclusions):
            print(lab + "\t : " + ", ".join(exc for exc in excs))


    def unload_exclusions(self):
        """Unload the current set of exclusion words."""

        if self.exclusions:

            print('Unloading previous exclusion words.')
            self.exclusions = list()


    @staticmethod
    def _check_type(term):
        """Check type of input term, and return as a list.

        Parameters
        ----------
        term : str OR list of str
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
