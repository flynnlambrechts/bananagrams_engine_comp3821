from pouch import Pouch
from players.player import Player
import threading


class Game:
    '''
    Game class is responsible for managing the players and the pouch of letters
    '''

    def __init__(self, seed=None) -> None:
        '''
        Initialise a game new players can be added each game
        should have at least one player
        '''
        self.pouch = Pouch(seed=seed)
        self.players: list[Player] = []
        self.lock =  threading.Lock()
        self.player_threads = []
        self.game_is_active = False
        
    def add_player(self, player: Player):
        '''
        Method to add new players, only required in multiplayer
        '''
        
        self.players.append(player)

    def _calculate_starting_tiles(self):
        n_players = len(self.players)
        if n_players == 0: raise ValueError("No players in game")
        if n_players <= 4: return 21
        if n_players <= 6: return 15
        if n_players <= 8: return 11
        raise ValueError(f"Too many players in game, maximum 8, found {n_players}")

    def start(self):
        self.game_is_active = True
        
        for i, player in enumerate(self.players):
            player.give_tiles(self.pouch.get_starting_tiles(self._calculate_starting_tiles()))
            self.player_threads.append(threading.Thread(target=player.play, name=f"Player{i + 1}"))
            
        for thread in self.player_threads:
            thread.start()
            
        for thread in self.player_threads:
            thread.join()
            
        print("Game Completed, All Players Done")

    def end_game(self):
        for player in self.players:
            player.game_over()

    def peel(self) -> bool:
        '''
        Returns True if the peel was successful, returns false if there wasn't enough for each player
        and we have a winner
        '''
        if self.pouch.n_remaining() < len(self.players):
            print("Insufficient letters for peel, ending game.")
            self.end_game()
            return False
        
        letters = []
        print(f"Executing Peel: Current Bunch {self.pouch}")
        for _ in self.players:
            letters.append(self.pouch.peel())
        print(f"Finished Executing Peel: Bunch {self.pouch}")
        
        for i, player in enumerate(self.players):
            player.give_tiles(letters[i])
        return True

    def dump(self, player: Player, tile: str):
        print(f"game dumping {tile} in hand {player.hand}")
        if tile not in player.hand: 
            raise IndexError("Can't dump tile if it's in player's hand")
        player.hand = player.hand.replace(tile, '', 1)
        new_tiles = self.pouch.dump(tile)
        player.give_tiles(new_tiles)
        print(f"player hand is now: [{player.hand}]")

    def __str__(self) -> str:
        '''
        Used to support print(Game) functionality
        '''

        game_str = (
            '[Game Status]\n' +
            f'\n - Tiles in pouch: {len(self.pouch.remaining)}'
        )

        for i, player in enumerate(self.players):
            game_str += f"Player: {i}\n"
            game_str += str(player) + "\n"

        return game_str

    def end_game(self):
        self.game_is_active = False
        winners = []
        for player in self.players:
            if len(player.hand) == 0:
                winners.append(player.name)
        print("GAME OVER")
        print("Winners: ")
        if winners:
            for winner in winners:
                print(f"\t{winner}")
        else:
            print("None :(")