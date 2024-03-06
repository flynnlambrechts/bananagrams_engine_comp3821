import json

# Alphabetically sorts the characters in a string
def sort_word(word):
    return ''.join(sorted(word.upper()))

# So far only finds if a base or base minus one char has anagrams
def find_best_ana(base):
    base_unique = ''.join(set(base))
    ana_list = []
    if base in word_dict.keys():
        ana_list.append(base)
    for i in base_unique:
        base_cat = base.replace(i, '', 1)
        if base_cat in word_dict.keys():
            ana_list.append(base_cat)
    return ana_list

with open("Dictionary/hash_dict.json", "r") as file:
    word_dict = json.load(file)

# for each line, check for anagrams
with open("test.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        base = sort_word(line.strip())
        print(find_best_ana(base))
