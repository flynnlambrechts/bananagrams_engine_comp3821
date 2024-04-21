from players.player import Player
from algorithms import where_to_play_word
from trie_service import all_words_trie
from word import Word
from board.tile import Tile
from board.board import Board
from constants import NO_SPACE_FOR_WORD

class StandardPlayer(Player):
    def play_first_turn(self):
        # Find the first word, play it, and add its first and last characters/tiles
        # to `anchors`
        words = all_words_trie.all_subwords(self.hand)
        if len(words) == 0:
            # if start_word == None:
            # give up
            self.game_running = False
            self.speak("GIVE UP", "Could not find starting word")
        start_word = max(words, key = lambda word: self.word_scorer.score_word(word.string, hand = self.hand))
        # start_word: Word = long_with_lowest_rank(all_words_trie.all_subwords(
        #     self.hand), closeness_to_longest=2, attempt=self.board_attempt)
        # if start_word == None:
        #     start_word = long_with_lowest_rank(all_words_trie.all_subwords(
        #         self.hand), closeness_to_longest=3, attempt=self.board_attempt)
        
            
        self.speak("Playing", start_word)
        self.play_word(str(start_word))

    def play_turn(self):
        print()
        # Peel if hand is empty
        if len(self.hand) == 0:
            self.peel()

        if not self.game.game_is_active:
            return

        # If this is the first turn the player acts differently
        if not self.playing:
            self.playing = True
            self.play_first_turn()
            return

        # Otherwise generic implementation of play turn
        self.speak('Finding Word', f"available letters {self.hand}")
        # print("no anchors:", len(self.board.anchors))
        # Words that can be formed using an anchor
        word_candidates: tuple[Word, Tile] = []
        for anchor in self.board.anchors:
            # Looping over anchors to see if the hand+anchor can make a word
            # print(f"anchor: {repr(anchor)}")
            words = all_words_trie.all_subwords(self.hand, anchor.char, anchor.lims)
            # print(f"len(words) prefilter = {len(words)}")
            words = [
                    word for word in words
                    if where_to_play_word(word.string, anchor) != NO_SPACE_FOR_WORD
                    ]
            # print(f"len(words) postfilter = {len(words)}")
            if len(words) > 0:
                word = max(words, key = lambda word: self.word_scorer.score_word(word.string, hand = self.hand))
            else:
                word = None
            # word = long_with_lowest_rank(all_words_trie.all_subwords(
            #     self.hand, anchor.char, anchor.lims), anchor)

            if word is not None and word.has_anchor(anchor.char):
                word_candidates.append((word, anchor))

        self.speak("Found", f"{len(word_candidates)} word candidates")
        if len(word_candidates) == 0:
            self.speak("Problem", "Could not find next word")
            return self.restructure_board()

        # Very weird way of calculating the best next word and its
        # corresponding anchor
        word, anchor = max(word_candidates, key = lambda word_tup: self.word_scorer.score_word(word_tup[0].string, hand = self.hand))
        # long_with_lowest_rank([word for word, _ in word_candidates])
        # print(f"word: {word.string}")
        # if any(word in w_tuple for w_tuple in word_candidates):
        #     print("the word is in the list")
        # anchor = next(anchor for w, anchor in word_candidates if w == word)

        self.speak("Playing", f"{word} on anchor {anchor}")
        self.play_word(str(word), anchor)

    def restructure_board(self):
        '''
        If we cannot continue without our current board formation
        this function is called. It should made adjustments and try
        play a word again
        '''
        if self.board_attempt > 20:
            self.speak("Error", "Too Many Rebuild Attempts")
            self.show_board()
            return "Error"

        self.board_attempt += 1
        self.playing = False
        while len(self.board.tiles) > 0:
            self.hand += (self.board.tiles.popitem()[1].char)
        self.board = Board()
        self.speak("Rebuild Attempt",
                   f"attempt {self.board_attempt - 1} failed")
        self.play_turn()
