import time
from src.pouch import Pouch
from src.trie import Trie
from pathlib import Path

this_directory = Path(__file__).parent.resolve()
dictionary = this_directory / '..' / 'assets' / 'word_dictionary.txt'
print(f'[Initializing]')
all_words = Trie(mode='sort', dictionary_path=dictionary)
forward_words = Trie('forward', dictionary_path=dictionary)
reverse_words = Trie('reverse', dictionary_path=dictionary)
pouch = Pouch()

print("tries made!")
base = "IP"
print(f"base: {base}")
anchor = "CRA"
print(f"anchor: {anchor}")
f_list = forward_words.all_subwords(base, anchor)
print("forward:")
for word in f_list:
    print(word.string, end=", ")
r_list = reverse_words.all_subwords(base, anchor)
print("\n\nreverse:")
for word in r_list:
    print(word.string, end=", ")
s_list = all_words.all_subwords(base, anchor)
print("sorted:")
for word in s_list:
    print(word.string, end=", ")

durations = []
nodes_visited = []
words_found = []
big_words_found = []
for i in range(1000):
    pouch = Pouch()
    base = ''.join(pouch.get_starting_tiles())
    print(f"run {i}: {base}")

    start = time.time()
    word_count = all_words.all_subwords(base)
    end = time.time()

    durations.append(end-start)
    # Note that the nodes visited part of all_subwords is by default commented out
    # Since it's not useful for actually doing stuff
    # So it needs to be uncommented for that to work.
    nodes_visited.append(word_count.pop())
    words_found.append(len(word_count))
    big_word_count = sum(len(item.string) >= 9 for item in word_count)
    big_words_found.append(big_word_count)
    print(
        f"found {words_found[-1]} words in {end - start} seconds!")

print(f"av. time: {sum(durations)/len(durations)}")
print(f"Total time: {sum(durations)}")
print(f"av. words found: {sum(words_found)/len(words_found)}")
print(f"max words found: {max(words_found)}")
print(f"av. long words found: {sum(big_words_found)/len(big_words_found)}")
print(f"min. long words found: {min(big_words_found)}")
print(f"max. long words found: {max(big_words_found)}")

# print(f"av. nodes visited: {sum(nodes_visited)/len(nodes_visited)}")
