import json

def sort_word(word):
    return ''.join(sorted(word.upper()))

def find_best_ana(base):
    base_unique = ''.join(set(base))
    ana_list = []
    for i in base_unique:
        base_cat = base.replace(i, '', 1)
        if base_cat in word_dict.keys():
            ana_list.append(base_cat)
    


with open("Dictionary/hash_dict.json", "r") as file:
    word_dict = json.load(file)

with open("test.txt", "r") as file:
    lines = file.readlines()
    for line in lines:
        base = sort_word(line.strip())
        if base in word_dict.keys():
            print(word_dict[base])
        else:
            print("sad")
            print(f"1st letter?: {line[0]}")
            print(f"3rd letter?: {line[2]}")