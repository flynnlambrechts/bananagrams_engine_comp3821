
from pickle_manager import load_tries
    
'''
Runs when this file is first imported.

Since the tries aren't modified at runtime, the GIL penalty
is negligible even if every player is using the same trie!
'''
all_words_trie, forward_trie, reverse_trie = load_tries()