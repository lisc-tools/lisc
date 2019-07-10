"""   """

from py.test import raises

from lisc.scrape import *

###################################################################################################
###################################################################################################

def test_scrape_counts():
    pass

def test_scrape_words():
    pass

#from lisc.words import _ids_to_str, _process_words, _process_kws
#from lisc.words import _process_authors, _process_pub_date, _process_ids

# def test_scrape_data():
#     """Test the scrape_data method."""

#     words = Words()

#     # Add ERPs and terms
#     #words.set_terms(['N400', 'P600'])
#     words.set_terms(['language', 'memory'])
#     words.set_exclusions(['cell', ''])

#     #words.scrape_data(db='pubmed', retmax='5')

#     assert True

# def test_extract_add_info():
#     """Test the extract_add_info method."""

#     words = Words()

#     # Check page with all fields defined - check data extraction
#     erp_word = Data('test')
#     page = requests.get(("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
#                          "efetch.fcgi?&db=pubmed&retmode=xml&id=28000963"))
#     page_soup = BeautifulSoup(page.content, "xml")
#     art = page_soup.findAll('PubmedArticle')[0]
#     words.extract_add_info(erp_word, 111111, art)

#     assert erp_word.ids[0] == 111111
#     assert erp_word.titles[0] == ("A Neurocomputational Model of the N400"
#                                   " and the P600 in Language Processing.")
#     assert erp_word.words[0][0] == "ten"
#     assert erp_word.kws[0][0] == "computational modeling"
#     assert erp_word.years[0] == 2017
#     assert erp_word.months[0] == 'May'
#     assert erp_word.dois[0] == '10.1111/cogs.12461'

#     # Check page with all fields missing - check error handling
#     page = requests.get('http://www.google.com')
#     erp_word = words.extract_add_info(erp_word, 999999, page)

#     assert erp_word.ids[1] == 999999
#     assert erp_word.titles[1] is None
#     assert erp_word.words[1] is None
#     assert erp_word.kws[1] is None
#     assert erp_word.years[1] is None
#     assert erp_word.months[1] is None
#     assert erp_word.dois[1] is None


# def test_ids_to_str():
#     """Test the _ids_to_str function."""

#     # Initialize id ResultSet
#     idd = bs4.element.Tag(name='id')
#     idd.append('1111')
#     ids = bs4.element.ResultSet(source=None, result=(idd, idd))

#     out = _ids_to_str(ids)

#     assert out == '1111,1111'

# def test_none_process():
#     """The _process functions have a decorator to catch & return None inputs.
#     Test that this is working - returns None when given None.
#     """

#     assert _process_words(None) is None
#     assert _process_kws(None) is None
#     assert _process_authors(None) is None
#     assert _process_authors(None) is None
#     assert _process_pub_date(None) == (None, None)

# def test_process_words():
#     """Test the _process_words function."""

#     words = 'The Last wOrd, in they eRp!'

#     words_out = _process_words(words)
#     exp_out = ['last', 'word', 'erp']

#     assert words_out == exp_out

# def test_process_kws():
#     """Test the _process_kws function."""

#     pass

# def test_process_authors():
#     """Test the _process_authors function."""

#     pass

# def test_process_pub_date():
#     """   """

#     pass

# def test_process_ids():
#     """   """

#     pass