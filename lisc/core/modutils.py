"""Utility functions & decorators for dealing with LISC, as a module."""

from importlib import import_module

###################################################################################################
###################################################################################################

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
        mod = False

    # Prior to py 3.5.4, import module could throw a SystemError
    #  Older approach requires the parent module be imported first
    #  If triggered, re-check for module after first importing the parent
    except SystemError:
        try:
            _ = import_module(args[-1])
            mod = import_module(*args)
        except ImportError:
            mod = False

    return mod
