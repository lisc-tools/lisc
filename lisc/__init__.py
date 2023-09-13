"""LISC: Literature Scanner."""

from lisc.version import __version__

from lisc.objects import Counts1D, Counts, Words
from lisc.collect import (collect_info, collect_counts, collect_words,
                          collect_across_time, collect_citations)
