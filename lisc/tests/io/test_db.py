"""Tests for lisc.io.db"""

from pathlib import Path

from lisc.io.db import *

###################################################################################################
###################################################################################################

def test_scdb():

    # Test defining object with no explicit base (implicitly current directory)
    db = SCDB(generate_paths=False)
    assert db
    assert db.paths['base'] == Path('.')

    # Test defining object with an explicit base
    db = SCDB(base='data', generate_paths=False)
    assert db
    assert db.paths['base'] == Path('data')

def test_scdb_gen_paths():

    names, paths = get_structure_info(STRUCTURE)

    # Test with no explicit base
    db = SCDB(generate_paths=True)
    for name, path in zip(names, paths):
        assert name in db.paths
        assert db.paths[name] == Path(path)

    # Test with specified base
    db = SCDB(base='data', generate_paths=False)
    db.gen_paths()
    assert db.paths['base'] == Path('data')
    for name, path in zip(names, paths):
        assert name in db.paths
        assert db.paths[name] == Path('data') / path

    # Check with a custom structure
    T_STRUCTURE = {1 : {'base' : ['magic', 'music']},
                   2 : {'magic' : ['silly', 'scary'], 'music' : ['guitar', 'piano']},
                   3 : {'scary' : ['too_true']}}
    db = SCDB(generate_paths=True, structure=T_STRUCTURE)
    t_names, t_paths = get_structure_info(T_STRUCTURE)
    for name, path in zip(t_names, t_paths):
        assert name in db.paths
        assert db.paths[name] == Path(path)

def test_scdb_get_folder_path():

    db = SCDB()
    assert db.get_folder_path('base') == Path('')
    assert db.get_folder_path('data') == Path('data')

    db = SCDB(base='tdb')
    assert db.get_folder_path('base') == Path('tdb')
    assert db.get_folder_path('data') == Path('tdb/data')

def test_scdb_get_file_path():

    db = SCDB()
    file_path = db.get_file_path('data', 'test.txt')
    assert file_path == Path('data/test.txt')

def test_scdb_get_files(tdb):

    terms_files = tdb.get_files('terms')
    assert isinstance(terms_files, list)
    assert isinstance(terms_files[0], str)

    terms_files = tdb.get_files('terms', drop_ext=True)
    assert '.' not in terms_files[0]

def test_scdb_check_file_structure(tdb):

    tdb.check_file_structure()

def test_check_directory():

    assert check_directory(None) == Path('.')
    assert check_directory('/path/to/file') == Path('/path/to/file')
    assert check_directory(Path('path/to/file')) == Path('path/to/file')
    assert isinstance(check_directory(SCDB(), 'terms'), Path)

def test_check_file_structure(tdb):

    check_file_structure(tdb.paths['base'])

def test_get_structure_info():

    names, paths = get_structure_info(STRUCTURE)
    assert 'terms' in names
    assert 'data/counts' in paths
