import time
from src.pouch import Pouch
from src.trie import Trie
from pathlib import Path

POUCH_AS_STRING = "AAAAAAAAAAAAABBBCCCDDDDDDEEEEEEEEEEEEEEEEEEFFFGGGGHHHIIIIIIIIIIIIJJKKLLLLLMMMNNNNNNNNOOOOOOOOOOOPPPQQRRRRRRRRRSSSSSSTTTTTTTTTUUUUUUVVVWWWXXYYYZZ"

this_directory = Path(__file__).parent.resolve()
dictionary = this_directory / '..' / 'assets' / 'word_dictionary.txt'
print(f'[Initializing]')
all_words = Trie(mode='sort', dictionary_path=dictionary)
forward_words = Trie('forward', dictionary_path=dictionary)
reverse_words = Trie('reverse', dictionary_path=dictionary)
pouch = Pouch()

print("tries made!")
# alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# is_prefix_of_count = {}
# is_suffix_of_count = {}
# pair_start_count = {}
# pair_end_count = {}

# for char in alphabet:
#     as_prefix = forward_words.all_subwords(POUCH_AS_STRING.replace(char, '', 1), char)
#     as_suffix = reverse_words.all_subwords(POUCH_AS_STRING.replace(char, '', 1), char)
#     pairs_start_with = (sum(len(word.string) == 2 for word in as_prefix ))
#     pairs_end_with = (sum(len(word.string) == 2 for word in as_suffix ))
#     words_start_with = (len(as_prefix))
#     words_end_with = (len(as_suffix))
#     is_prefix_of_count[char] = words_start_with
#     is_suffix_of_count[char] = words_end_with
#     pair_start_count[char] = pairs_start_with
#     pair_end_count[char] = pairs_end_with

#     print(f"{char}: pre: {words_start_with} ({pairs_start_with}), post: {words_end_with}, ({pairs_end_with})")

# print("Is prefix of:\n", is_prefix_of_count)
# print("Is suffix of:\n", is_suffix_of_count)
# print("Pair start count:\n", pair_start_count)
# print("Pair end count:\n", pair_end_count)





# tonight_anagrams = all_words.all_subwords("TONIGHT")
# for word in tonight_anagrams:
#     print(word)

# base = "IP"
# print(f"base: {base}")
# anchor = "CRA"
# print(f"anchor: {anchor}")
# f_list = forward_words.all_subwords(base, anchor)
# print("forward:")
# for word in f_list:
#     print(word.string, end=", ")
# r_list = reverse_words.all_subwords(base, anchor)
# print("\n\nreverse:")
# for word in r_list:
#     print(word.string, end=", ")
# s_list = all_words.all_subwords(base, anchor)
# print("sorted:")
# for word in s_list:
#     print(word.string, end=", ")



def look_at_word_sizes(fun_base, word_size_arr, no_bigs_wanted):
    word_count = all_words.all_subwords(fun_base)

    word_count.sort(key=lambda word: len(word.string))
    count = 0
    word_length = 2
    for i in range(len(word_count)):

        l = len(word_count[i].string)
        if l != word_length:
            word_size_arr[word_length].append(count)
            count = 0
            word_length = l
        count += 1
    mediums = []
    for i in range(no_bigs_wanted):
        mediums.append(word_count[-1-i])
    return mediums

word_size_array_1 = []
for i in range(22):
    word_size_array_1.append([])

word_size_array_2 = []
for i in range(22):
    word_size_array_2.append([])
OUTER_ITERATIONS = 3
BIG_ITERATIONS = 5
MED_ITERATIONS = 5
for i in range(OUTER_ITERATIONS):
    pouch = Pouch()
    base = ''.join(pouch.get_starting_tiles())
    bigs = look_at_word_sizes(base, word_size_array_1, 20)
    for word in bigs:
        small_base = base
        for char in word.string:
            small_base = small_base.replace(char,'',1)
        look_at_word_sizes(small_base, word_size_array_2, 0)

for i in range(22):
    print(f"wl {i}: {sum(word_size_array_1[i])/OUTER_ITERATIONS}")
print("\n\n\nINNER: \n\n")
for i in range(22):
    print(f"wl {i}: {sum(word_size_array_2[i])/(OUTER_ITERATIONS * INNER_ITERATIONS)}")

# durations = []
# nodes_visited = []
# words_found = []
# big_words_found = []
# two_letter_count = []
# big_ish_words = []
# word_size_array = []
# for i in range(22):
#     word_size_array.append([])

# for i in range(10):
#     pouch = Pouch()
#     base = ''.join(pouch.get_starting_tiles())
#     print(f"run {i}: {base}")

#     start = time.time()
#     word_count = all_words.all_subwords(base)
#     end = time.time()

#     durations.append(end-start)
#     # Note that the nodes visited part of all_subwords is by default commented out
#     # Since it's not useful for actually doing stuff
#     # So it needs to be uncommented for that to work.
#     nodes_visited.append(word_count.pop())
#     words_found.append(len(word_count))
#     word_sizes = [0,0]
#     word_count.sort(key=lambda word: len(word.string))
#     count = 0
#     word_length = 2
#     for i in range(len(word_count)):

#         l = len(word_count[i].string)
#         if l != word_length:
#             word_size_array[word_length].append(count)
#             count = 0
#             word_length = l
#         count += 1
        

#     big_word_count = sum(len(item.string) >= 9 for item in word_count)
#     two_letter_count.append(sum(len(item.string) == 2 for item in word_count))
#     big_ish_words.append(sum(len(item.string) >= 6 for item in word_count))
#     print(f"two letter count: {two_letter_count[-1]}")
#     big_words_found.append(big_word_count)
#     print(
#         f"found {words_found[-1]} words in {end - start} seconds!")

# print(f"av. time: {sum(durations)/len(durations)}")
# print(f"Total time: {sum(durations)}")
# print(f"av. words found: {sum(words_found)/len(words_found)}")
# print(f"max words found: {max(words_found)}")
# print(f"av. long words found: {sum(big_words_found)/len(big_words_found)}")
# print(f"min. long words found: {min(big_words_found)}")
# print(f"max. long words found: {max(big_words_found)}")
# print(f"av. 2 letter count: {sum(two_letter_count)/len(two_letter_count)}")
# print(f"av. 6+ letter count: {sum(big_ish_words)/len(big_ish_words)}")
# for i in range(22):
#     print(f"wl {i}: {sum(word_size_array[i])/len(words_found)}")
# # print(f"av. nodes visited: {sum(nodes_visited)/len(nodes_visited)}")
