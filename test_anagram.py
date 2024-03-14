from Dictionary.trie import Trie
from bananapouch import BananaPouch
import time
trie = Trie()
trie.make_trie("Dictionary/word_dictionary.txt")
pouch = BananaPouch()
print("trie made!")

with open("starting_letters_x100.txt", "r") as file:
    durations = []
    words_found = []
    nodes_visited = []
    lines = file.readlines()
    j = 0

    for line in lines:
        base = ''.join(sorted(line.strip().upper()))
        j += 1
        print(f"run {j}: {base}")

        start = time.time()
        word_count = trie.all_subwords(base)
        end = time.time()

        durations.append(end-start)
        # Note that the nodes visited part of all_subwords is by default commented out
        # Since it's not useful for actually doing stuff
        # So it needs to be uncommented for that to work.
        nodes_visited.append(word_count.pop())
        words_found.append(len(word_count))

        print(f"found {words_found[-1]} words in {end - start} seconds by looking at {nodes_visited[-1]} nodes!")

    print(f"av. time: {sum(durations)/len(durations)}")
    print(f"Total time: {sum(durations)}")
    print(f"av. words found: {sum(words_found)/len(words_found)}")
    print(f"av. nodes visited: {sum(nodes_visited)/len(nodes_visited)}")