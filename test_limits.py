from Game_Structure.game import Game
from Classes.trie import Trie
from run_algorithm import long_start_word

# s_trie = Trie("sort")
# s_trie.make_trie("Classes/word_dictionary.txt")

# game = Game()
# game.setup()
# print(game)
# print(game.hand)
# words = s_trie.all_subwords(game.hand)
# # word = long_start_word(words).word
# word = words[0].word
# print(f"word: {word}")
# game.play_word(word, 0, 0, 0, False)
# print(game)
# print(game.board.tiles[(0,0)].lims)
# print(game.board.tiles[(0,1)].lims)

# words = s_trie.find_two_letters("E")
# for word in words:
#     print(word.word)

game = Game()
game.board.add_word("EEEEE", 0, 0, 0)
game.board.add_word("EEE", 0, 0, 1)
game.board.add_word("EEE", 0, 4, 1)
print(game)
print("0,0:", game.board.tiles[(0,0)].lims)
print("0,1:", game.board.tiles[(0,1)].lims)
print("0,2:", game.board.tiles[(0,2)].lims)
print("1,0:", game.board.tiles[(1,0)].lims)
print("2,0:", game.board.tiles[(2,0)].lims)
# print("3,3:", game.board.tiles[(3,3)].lims)


# game.board.add_word("EE", 0, 0, 0)
# game.board.add_word("EE", 0, 0, 1)
# print(game)
# print("0,0:", game.board.tiles[(0,0)].lims)
# print("0,1:", game.board.tiles[(0,1)].lims)
# print("1,0:", game.board.tiles[(1,0)].lims)

# game.board.add_word("E", 0, 0, 0)
# game.board.add_word("E", 0, 3, 0)
# print(game)
# print("0,0:", game.board.tiles[(0,0)].lims)
# print("0,3:", game.board.tiles[(0,3)].lims)
