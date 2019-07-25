"""Utilities for managing URLs in LISC."""

###################################################################################################
###################################################################################################

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
