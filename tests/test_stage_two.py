from src.game import Game
from src.board import Board
import sys
import re

game = Game()
game.add_player()
player = game.players[0]

def play_game(starting_hand = '', turn_by_turn = False):
    # reset the board and pouch
    player.board = Board()
    player.hand = ''
    player.playing = False
    game.game_is_active = True
    player.dump_on_failure =  True
    player.dump_count = 0
    if len(starting_hand) > 0:
        player.give_tiles(starting_hand)
    else:
        game.pouch.reset()
        player.give_tiles(game.pouch.get_starting_tiles(21))
    go = True
    starting_hand = player.hand
    print(f"Starting hand: {starting_hand}")
    successful_game = True
    while(go):
        if player.play_turn() == "Error":
            go = False
            successful_game = False
        if game.game_is_active == False:
            go = False
        if turn_by_turn:
            input = take_input()
            if input == "End":
                go = False

    print(player)
    print(f"no. dumps: {player.dump_count}")
    if successful_game:
        print("success!")
    else:
        print("failure")
    return (i, starting_hand, successful_game, player.dump_count)

def take_input():
    print("Input: ")
    for line in sys.stdin:
        input = line.rstrip()
        if input == 'q':
            print("quitting")
            game.game_is_active = False
            return "End"
        if input == 'c' or '\n':
            print("continuing")
            return "Continue"
        if input == 'p':
            print(player)
        if input == 'all tiles':
            print(list(player.board.tiles.keys()))
        else:
            input = line.rstrip()
            pattern = r"\((-?\d+),\s*(-?\d+)\)"
            match = re.match(pattern, input)
            if match:
                row = int(match.group(1))
                col = int(match.group(2))
                if (row, col) in player.board.tiles:
                    tile = player.board.tiles[(row, col)]
                    print(tile)
                    print(f"vert parent: {tile.vert_parent}")
                    print(f"horo parent: {tile.horo_parent}")
                    print(f"is-junk: {tile.is_junk}")
                    print(f"lims: ")
                    print(tile.lims)
                else:
                    print(f"{input} not found on board")




# i = 0
# play_game("EQUILIBRATEFNNDODDYJV", turn_by_turn=True)
results = []
ITERATIONS = 100
for i in range(ITERATIONS):
    print(f"\n\nRun {i}")
    results.append(play_game())
failures = list(filter(lambda result: result[2] == False, results))
print(failures)
print(f"{len(failures)} failures out of {ITERATIONS}")

# EQUILIBRATEFNNDODDYJV

# past failures
# ETNNEEJIIFRWIWOIEAFRW

# PHELETIFEMEOUADNMSNBO
# LRYGPALEKEEIOHOPIRDUT