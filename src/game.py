from pouch import Pouch
from player import Player



class Game:
    '''
    Game class is responsible for managing the players and the pouch of letters
    '''
    def __init__(self) -> None:
        '''
        Initialise a game new players can be added each game
        should have at least one player
        '''
        self.pouch = Pouch()
        self.players: list[Player] = []

    def add_player(self):
        '''
        Method to add new players, only required in multiplayer
        '''
        self.players.append(Player(self))

    def start(self):
        for player in self.players:
            # TODO: For multiplayer change number of starting tiles based
            # on number of players
            player.give_tiles(self.pouch.get_starting_tiles(21))

        # At the moment we only allow the first player to player
        # in future it should be implemented in either a turn based
        # or multithreaded format
        self.players[0].play()

    def peel(self):
        # TODO: check there are enough tiles for each player
        
        for player in self.players:
            player.give_tiles(self.pouch.peel())

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
