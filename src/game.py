from .pouch import Pouch
from .player import Player


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
        self.game_is_active = True # can maybe make it false in future to give time for preprocessing, can have a split() function
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
        new_tiles = []
        for player in self.players:
            new_tile = self.pouch.peel()
            if new_tile != -1:
                new_tiles.append(new_tile)
            else:
                return self.end_game()
        for i, player in enumerate(self.players):
            player.give_tiles(new_tiles[i])

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