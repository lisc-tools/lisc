"""Utilities for downloading data."""

import nltk

###################################################################################################
###################################################################################################

def download_nltk_data():
	"""Download required nltk data for LISC analyses."""

    nltk.download('punkt')
    nltk.download('stopwords')
