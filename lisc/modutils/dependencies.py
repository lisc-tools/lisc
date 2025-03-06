"""Dependency related utitiles and decorators."""

from importlib import import_module

###################################################################################################
###################################################################################################

class Dependency():
    """An object to represent optional dependencies that are not available.


    Attributes
    ----------
    mod_name :str
        The name of the module that was not imported.

    Notes
    -----
    This object raises an error if something tries to use the represented module.
    """

    def __init__(self, mod_name):

        self.mod_name = mod_name

    def __getattr__(self, val):

        message = "The {} module is required for this functionality."
        raise ImportError(message.format(self.mod_name))


def safe_import(*args):
    """Import a module, with a safety net for if the module is not available.

    Parameters
    ----------
    *args : str
        Module to import.

    Returns
    -------
    mod : module or False
        Requested module, if successfully imported, otherwise boolean (False).

    Notes
    -----
    *args accepts either 1 or 2 strings, as pass through inputs to import_module.
        To import a whole module, pass a single string, ex: ('matplotlib').
        To import a specific package, pass two strings, ex: ('.pyplot', 'matplotlib')
    """

    try:
        mod = import_module(*args)
    except ImportError:
        mod = Dependency(args[-1])

    # Prior to Python 3.5.4, import module could throw a SystemError
    #  Older approach requires the parent module be imported first
    #  If triggered, re-check for module after first importing the parent
    except SystemError:
        try:
            _ = import_module(args[-1])
            mod = import_module(*args)
        except ImportError:
            mod = Dependency(args[-1])

    return mod
