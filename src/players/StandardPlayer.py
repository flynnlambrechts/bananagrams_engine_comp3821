from players.player import Player
from algorithms import long_with_lowest_rank
from word import Word
from tile import Tile
from pathlib import Path
from trie import Trie
from board import Board

class StandardPlayer(Player):
        # Initialize our objects
    this_directory = Path(__file__).parent.resolve()
    dictionary = this_directory / '..' / '..' / 'assets' / 'word_dictionary.txt'
    print(f'[Initializing]')
    all_words = Trie(mode='sort', dictionary_path=dictionary)
    forward_words = Trie('forward', dictionary_path=dictionary)
    reverse_words = Trie('reverse', dictionary_path=dictionary)
    
    def play_first_turn(self):
        # Find the first word, play it, and add its first and last characters/tiles
        # to `anchors`
        start_word: Word = long_with_lowest_rank(StandardPlayer.all_words.all_subwords(
            self.hand), closeness_to_longest=2, attempt=self.board_attempt)
        if start_word == None:
            start_word = long_with_lowest_rank(StandardPlayer.all_words.all_subwords(
                self.hand), closeness_to_longest=3, attempt=self.board_attempt)
        if start_word == None:
            self.board_attempt = 21  # give up
            return self.restructure_board()
        self.speak("Playing", start_word)
        self.play_word(str(start_word))
        # self.show_board()
        # self.anchors += [self.board.tiles[(0, 0)], self.board.tiles[(0, len(str(start_word)) - 1)]]

    def play_turn(self):
        print("")
        # Peel if hand is empty
        if len(self.hand) == 0:
            self.peel()
    
        if not self.game_running:
            return

        # If this is the first turn the player acts differently
        if not self.playing:
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        self.speak('Finding Word', f"available letters {self.hand}")

        # Precompute string repesentation of anchors
        anchor_str = ''.join([anchor.char for anchor in self.board.anchors])
        # Words that can be formed using an anchor
        word_candidates: tuple[Word, Tile] = []
        for anchor in self.board.anchors:
            # Looping over anchors to see if the hand+anchor can make a word
            word = long_with_lowest_rank(StandardPlayer.all_words.all_subwords(
                self.hand, anchor.char, anchor.lims), anchor)

            if word is not None and word.has_anchor(anchor.char):
                word_candidates.append((word, anchor))
        self.speak("Found", f"{len(word_candidates)} word candidates")

        if len(word_candidates) == 0:
            self.speak("ERROR", "Could not find next word")
            return self.restructure_board()

        # Very weird way of calculating the best next word and its
        # corresponding anchor
        word = long_with_lowest_rank([word for word, _ in word_candidates])
        anchor = next(anchor for w, anchor in word_candidates if w == word)

        self.speak("Playing", f"{word} on anchor {anchor}")

        self.play_word(str(word), anchor)
        # self.show_board()

    def restructure_board(self):
        '''If we cannot continue without our current board formation
        this function is called. It should made adjustments and try
        play a word again
        '''
        if self.board_attempt > 20:
            return "Error"
        self.board_attempt += 1
        self.playing = False
        while len(self.board.tiles) > 0:
            self.hand += (self.board.tiles.popitem()[1].char)
        self.board = Board()
        self.speak("Rebuild Attempt", f"attempt {self.board_attempt - 1} failed")
        self.play_turn()
        # TODO
        # return "Error"
        # raise NotImplementedError("Board restructuring not implemented yet")
        
    
        
    