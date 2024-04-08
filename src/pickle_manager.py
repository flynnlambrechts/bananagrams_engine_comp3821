'''
Python pickles save objects to disk for later use.

This is especially useful for our Trie objects as
they take a long time to setup and are static accross
executions.

Run this file directly to compile the Tries from scratch
and then save them to a file so that main.py doesn't have to
'''


from pathlib import Path
import pickle
from trie import Trie

_this_directory = Path(__file__).parent.resolve()
_pickle_dir = _this_directory / 'pickles'


def _compile_pickle(object, pickle_name):
    with open(_pickle_dir / (pickle_name + '.pkl'), 'wb') as file:
        pickle.dump(object, file)


def _load_pickle(pickle_name):
    with open(_pickle_dir / (pickle_name + '.pkl'), 'rb') as file:
        return pickle.load(file)


def compile_tries():
    '''
    Compiles the tries into pickles
    '''
    dictionary = _this_directory / '..' / 'assets' / 'word_dictionary.txt'

    all_words = Trie(mode='sort', dictionary_path=dictionary)
    forward_words = Trie(mode='forwards', dictionary_path=dictionary)
    reverse_words = Trie(mode='reverse', dictionary_path=dictionary)

    _compile_pickle(all_words, 'all_words')
    _compile_pickle(forward_words, 'forward_words')
    _compile_pickle(reverse_words, 'reverse_words')


def load_tries():
    '''
    Loads the tries from pickles

    USAGE:
    all_words, forward_words, reverse_words = load_tries()
    '''
    return (
        _load_pickle('all_words'),
        _load_pickle('forward_words'),
        _load_pickle('reverse_words')
    )


if __name__ == '__main__':
    compile_tries()
    # load_tries()
