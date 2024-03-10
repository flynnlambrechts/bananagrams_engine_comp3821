

# word_dictionary.txt key is:
# WORD NUM_WORDS_STARTWITH
with open('word_dictionary.txt', 'r+') as file:
    lines = file.readlines()
    for i, line in enumerate(lines):
        num_words_start = 0
        for j, line2 in enumerate(lines[i:]):
            
            if line2.startswith(line.split('\n')[0]):
                print(num_words_start)
                num_words_start += 1
            else:
                break
        with open('word_dictionary_with_heuristics.txt', "a") as file2:
                file2.write(line.split('\n')[0] + " " + str(num_words_start) + "\n")
        

    
    