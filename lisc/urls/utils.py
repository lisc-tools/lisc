"""Utilities for managing URLs in LISC."""

###################################################################################################
###################################################################################################

def check_none(val, default):
    """Check an input for if it is None, and if so return a default object.

    Parameters
    ----------
    val : collection object or None
        An object to check whether is None.
    default : collection object
        What to default to if `val` is None.

    Returns
    -------
    collection object
        Either the original input item, or the default input.

    Notes
    -----
    This function is used to catch unused inputs (that end up as None), before they
    are passed into subsequent functions that presume collection objects.
    """

    return val if val else default


def check_settings(settings):
    """Check that all settings are defined as strings.

    Parameters
    ----------
    settings : dict
        Dictionary to check.

    Returns
    -------
    dict
        Dictionary with all values set as strings.
    """

    return {key : str(val) for key, val in settings.items()}


def prepend(string, prefix):
    """Append something to the beginning of another string.

    Parameters
    ----------
    string : str
        String to prepend to.
    prefix : str
        String to add to the beginning.

    Returns
    -------
    str
        String with the addition to the beginning.

    Notes
    -----
    This function deals with empty inputs, and returns an empty string in that case.
    """

    return prefix + string if string else string


def make_segments(segments):
    """Make the segments portion of a URL.

    Parameters
    ----------
    segments : list of str
        Segments to use to create the segments string for a URL.

    Returns
    -------
    str
        Segments for a URL.
    """

    return prepend('/'.join(segments), '/')


def make_settings(settings, prefix='?'):
    """Make the settings portion of a URL.

    Parameters
    ----------
    settings : dict
        Settings to use to create the settings string for a URL.
    prefix : str
        String to add to the beginning.

    Returns
    -------
    str
        Setting for a URL.
    """

    return prepend('&'.join([ke + '=' + va for ke, va in settings.items()]), prefix)
