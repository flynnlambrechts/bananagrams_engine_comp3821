from src.Algorithm.Trie.Trie import Trie
from src.Algorithm.algorithm_functions import run_algorithm

with open("starting_letters_x1000.txt", "r") as file:
    trie = Trie()
    trie.make_trie("word_dictionary.txt")

    for line in file.readlines():
        base = ''.join(sorted(line.strip()))
        run_algorithm(base, trie)
