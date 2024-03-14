from Classes.trie import Trie
from Game_Structure.bananapouch import BananaPouch
import time
s_trie = Trie()
f_trie = Trie("forward")
r_trie = Trie("reverse")
s_trie.make_trie("Classes/word_dictionary.txt")
f_trie.make_trie("Classes/word_dictionary.txt")
r_trie.make_trie("Classes/word_dictionary.txt")
pouch = BananaPouch()

print("tries made!")
base = "IP"
print(f"base: {base}")
anchor=  "CRA"
print(f"anchor: {anchor}")
f_list = f_trie.all_subwords(base, anchor)
print("forward:")
for word in f_list:
    print(word.word, end = ", ")
r_list = r_trie.all_subwords(base, anchor)
print("\n\nreverse:")
for word in r_list:
    print(word.word, end = ", ")
s_list = s_trie.all_subwords(base, anchor)
print("sorted:")
for word in s_list:
    print(word.word, end = ", ")


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
        word_count = s_trie.all_subwords(base)
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