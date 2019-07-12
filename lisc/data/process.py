"""Helper functions to process data for LISC."""

from lisc.data.utils import count_occurences

###################################################################################################
###################################################################################################

def process_years(years):
    """Process years.

    Parameters
    ----------
    years : list of int
        Year of publication of all papers.

    Returns
    -------
    counts : list of tuple of (int, int)
        Number of publications per year, as (year, count).
    """

    counts = [(year, years.count(year)) for year in set(years) - set([None])]
    counts.sort()

    return counts


def process_journals(journals):
    """Process journals.

    Parameters
    ----------
    journals : list of tuple of (str, str)
        List of journals articles come from.
        (journal name, ISO abbreviation)

    Returns
    -------
    counts : list of tuple of (int, str)
        Number of publications per journal, as (count, journal name).
    """

    names = [journal[0] for journal in journals]

    # TODO: Update this quick fix (??)
    names = [name for name in names if name is not None]

    counts = [(names.count(element), element) for element in set(names)]
    counts.sort(reverse=True)

    return counts


def process_authors(authors):
    """Process all authors.

    Parameters
    ----------
    authors : list of list of tuple of (str, str, str, str)
        Authors of all articles included in object, as
        (last name, first name, initials, affiliation)

    Returns
    -------
    counts : list of tuple of (int, (str, str))
        Number of publications per author, as (count, (last name, initials)).
    """

    # Drop author lists that are None
    authors = [author for author in authors if author is not None]

    # Reduce author fields to pair of tuples (last name, initials)
    # This list comprehension can be equivalently written as:
    # all_authors = []
    # for authors in a_lst:
    #     for author in authors:
    #         all_authors.append(author)
    names = [(author[0], author[2]) for authors in authors for author in authors]

    # Count how often each author published
    counts = count_occurences(fix_author_names(names))

    return counts


def process_end_authors(authors):
    """Process first and last authors only.

    Parameters
    ----------
    authors_lst : list of list of tuple of (str, str, str, str)
        Authors of all articles included in object, as
        (last name, first name, initials, affiliation)

    Returns
    -------
    f_counts, l_counts : list of tuple of (int, (str, str))
        Number of publications for first & last authors, as (count, (last name, initials))
    """

    # Drop author lists that are None
    authors = [author for author in authors if author is not None]

    # Pull out the full name for the first & last author of each paper
    #  Last author is only considered if there is more than 1 author
    firsts = [auth[0] for auth in authors]
    f_names = [(author[0], author[2]) for author in firsts]
    lasts = [auth[-1] for auth in authors if len(auth) > 1]
    l_names = [(author[0], author[2]) for author in lasts]

    f_counts = count_occurences(fix_author_names(f_names))
    l_counts = count_occurences(fix_author_names(l_names))

    return f_counts, l_counts


def fix_author_names(names):
    """Fix author names.

    Parameters
    ----------
    names : list of tuple of (str, str)
        Author names, as (last name, initials)

    Returns
    -------
    names : list of tuple of (str, str)
        Author names, as (last name, initials)

    Notes
    -----
    Sometimes full author name ends up in the last name field.
    If first name is None, assume this happened:
        Split up the text in first name, and grab the first name initial.
    """

    # Drop names whos data is all None
    names = [name for name in names if name != (None, None)]

    # TODO: figure out and fix
    # Fix names if full name ended up in last name field
    #names = [(name[0].split(' ')[1], name[0].split(' ')[0][0])
    #         if name[1] is None else name for name in names]

    return names
