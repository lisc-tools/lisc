"""Base object for LISC."""

import pkg_resources as pkg

#from lisc.core.io import save_object
from lisc.core.errors import InconsistentDataError

###################################################################################################
###################################################################################################

class Base():
    """Base class for LISC analyses.

    Attributes
    ----------
    db_info : dict()
        Stores info about the database used for scarping data.
    terms : list of list of str
        Terms words.
    labels : list of str
        Label to reference each term.
    exclusions : list of list str
        Exclusion words for each term, used to avoid unwanted articles.
    n_terms : int
        Number of terms.
    date : str
        Date data was collected.
    meta_data : dict
        Meta data for the scrape.
    has_dat : bool
        Whether there is any terms and/or data loaded.
    """

    def __init__(self):
        """Initialize Base() object."""

        # Initialize list of terms to use, including exclusions & labels
        self.terms = list()
        self.labels = list()
        self.exclusions = list()
        self.has_dat = False

        # Initialize counters for numbers of terms
        self.n_terms = int()


    def set_terms(self, terms):
        """Sets the given list of strings as terms to use.

        Parameters
        ----------
        terms : list of str OR list of list of str
            List of terms to be used.
        """

        # Unload previous terms if some are already loaded
        self.unload_terms()

        # Set given list as the terms
        for term in terms:
            self.terms.append(_check_type(term))
        self.get_term_labels()

        # Set the number of terms
        self.n_terms = len(terms)
        self.has_dat = True


    def set_terms_file(self, terms_f_name):
        """Load terms from a txt file.

        Parameters
        ----------
        terms_f_name : str
            File name to load terms from.
        """

        # Unload previous terms if some are already loaded
        self.unload_terms()

        # Get terms from module data file
        terms = _terms_load_file(terms_f_name)

        # Set the number of terms
        self.n_terms = len(terms)

        # Set as list, attach to object, set labels
        for i in range(self.n_terms):
            self.terms.append(terms[i][:].split(','))
        self.get_term_labels()


    def check_terms(self):
        """Print out the current list of terms."""

        # Print out header and all term words
        print('List of terms used: \n')
        for terms_ls in self.terms:
            print(", ".join(term for term in terms_ls))


    def unload_terms(self):
        """Unload the current set of terms."""

        # Check if exclusions are loaded, to empty them if so.
        if self.terms:

            # Print status that term words are being unloaded
            print('Unloading previous terms words.')

            # Reset term variables to empty
            self.terms = list()
            self.n_terms = int()

        self.has_dat = False


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

        # Unload previous terms if some are already loaded
        self.unload_exclusions()

        # Set given list as exclusion words
        for exclude in exclusions:
            self.exclusions.append(_check_type(exclude))

        # Check that the number of exclusions matches n_terms
        if len(exclusions) != self.n_terms:
            raise InconsistentDataError('Mismatch in number of exclusions and terms!')


    def set_exclusions_file(self, excl_f_name='exclusions'):
        """Load exclusion words from a txt file.

        Parameters
        ----------
        excl_f_name : str
            xx
        """

        # Unload previous terms if some are already loaded
        self.unload_exclusions()

        # Get exclusion words from module data file
        exclusions = _terms_load_file(excl_f_name)

        # Check that the number of exclusions matches n_terms
        if len(exclusions) != self.n_terms:
            raise InconsistentDataError('Mismatch in number of exclusions and terms!')

        # Drop number indices for exclusions, and set as list
        for i in range(self.n_terms):
            self.exclusions.append(exclusions[i][3:].split(','))


    def check_exclusions(self):
        """Print out the current list of exclusion words."""

        # Print out header and all exclusion words
        print('List of exclusion words used: \n')
        for lab, excs in zip(self.labels, self.exclusions):
            print(lab + "\t : " + ", ".join(exc for exc in excs))


    def unload_exclusions(self):
        """Unload the current set of exclusion words."""

        # Check if exclusions are loaded. If so, print status and empty.
        if self.exclusions:

            # Print status that exclusion words are being unloaded
            print('Unloading previous exclusion words.')

            # Reset exclusions variables to empty
            self.exclusions = list()


    def save(self, f_name, db=None):
        """Save out the current object.

        Parameters
        ----------
        f_name : str
            Name to append to saved out file name.
        db : SCDB() object, optional
            Database object for the LISC project.
        """

        save_object(f_name, db)

###################################################################################################
###################################################################################################

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

    # Check the type of the given item, return as list
    if isinstance(term, str):
        return [term]
    elif isinstance(term, list):
        return term

def _terms_load_file(dat_name):
    """Loads a terms data file from within the module.

    Parameters
    ----------
    dat_name : str
        Name of the terms data file to load.

    Returns
    -------
    dat : list of str
        Data from the file.
    """

    f_name = 'terms/' + dat_name + '.txt'
    f_path = pkg.resource_filename(__name__, f_name)
    terms_file = open(f_path, 'r')

    dat = terms_file.read().splitlines()

    return dat
