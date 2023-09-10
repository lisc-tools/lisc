"""Utilities for working with lisc objects."""

###################################################################################################
###################################################################################################

def check_object_type(obj):
    """Check the type of a LISC object.

    Parameters
    ----------
    obj : Counts1D or Counts or Words
        LISC object to check the type of.

    Returns
    -------
    obj_type : {'counts', 'words'}
        The object type of the input object.

    Raises
    ------
    ValueError
        If input object is not a lisc object / type cannot be inferred.
    """

    # Import objects locally, to avoid circular imports
    from lisc.objects import Counts1D, Counts, Words

    if isinstance(obj, (Counts1D, Counts)):
        obj_type = 'counts'
    elif isinstance(obj, Words):
        obj_type = 'words'
    else:
        raise ValueError('Object type unclear.')

    return obj_type
