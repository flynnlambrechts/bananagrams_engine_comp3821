from anagram_solver import *
from Dictionary.make_dict import *
import timeit
import time
trie = Trie()
make_trie(trie, "Dictionary/word_dictionary.txt")
pouch = BananaPouch()
print("trie made!")
with open("starting_letters_x100.txt", "w") as file:
    for i in range (100):
        pouch.reset()
        starting_tiles = ''.join(sorted(pouch.setup()))
        file.write(starting_tiles + '\n')


def find_subwords_w_info(trie, base):
    subwords = trie.all_subwords(base)
    # words_found.append(len(subwords))


with open("starting_letters_x100.txt", "r") as file:
    times = []
    words_found = []
    nodes_checked = []
    lines = file.readlines()
    j = 0
    for line in lines:
        base = sort_word(line.strip())
        print(base)
        print(j)
        # setup = f"from __main__ import find_subwords_w_info; trie = {trie}, base = {base}"
        # stmt = "find_subwords_w_info(trie, base)"
        # elapsed = timeit.timeit(stmt, setup=setup, number=3)
        j += 1
        # if j < 30:
        #     continue
        start = time.time()
        word_count = trie.all_subwords(base)
        end = time.time()
        times.append(end-start)
        words_found.append(len(word_count) - 1)
        nodes_checked.append(word_count.pop())
        print(end - start)

        print(f"nodes visited: {nodes_checked[len(nodes_checked) - 1]}")
        print(f"words found: {words_found[len(words_found) - 1]}")

        if j > 60: 
            break
    print(f"av. time: {sum(times)/len(times)}")
    print(f"av. words found: {sum(words_found)/len(words_found)}")
    print(f"av. nodes visited: {sum(nodes_checked)/len(nodes_checked)}")
    