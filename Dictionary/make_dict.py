import json
word_dict = {}

def add_word(word):
    s_word = sort_word(word)
    if s_word in word_dict.keys():
        word_dict[s_word].append(word)
    else:
        word_dict[s_word] = [word]

def sort_word(word):
    return ''.join(sorted(word.upper()))

with open("word_dictionary.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        add_word(line.strip())
        # print(sort_word(line.strip()))

with open("hash_dict.json", "w") as file:
    json.dump(word_dict, file)
    # for anagrams in word_dict:
    #     for anagram in word_dict[anagrams]:
    #         print(f"{anagrams}: {anagram}")
    #     print()