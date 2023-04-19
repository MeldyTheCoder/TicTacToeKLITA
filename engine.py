import json
import os
import random
import string
import config
from typing import Union
from models.board import BoardModel
from models.constants import CIRCLE, CROSS, IN_PROCESS
from models.player import PlayerModel
from models.game import GameModel
from models.database import Database
from models import exceptions

class GameEngine:
    PLAYERS_REQUIRED = 2

    def __init__(self, use_db: bool = False):
        self.connected_database = Database(config.DATABASE_PATH) if use_db else None
        self.BOARD_GAMES: dict = {} if not self.connected_database else {game.game_id: game for game in self.get_games_from_database()}

    @property
    def random_id(self) -> str:
        length = 10
        letters = string.ascii_letters + string.digits
        return "".join([random.choice(letters) for _ in range(length)])

    def new_game(self, players: list[int, int], diagonal: int = 3) -> GameModel:
        if len(players) != self.PLAYERS_REQUIRED:
            raise exceptions.NotEnoughPlayersException(self.PLAYERS_REQUIRED)

        marks = [CIRCLE, CROSS]
        players = [PlayerModel(id=player, mark_symbol=marks[index]) for index, player in enumerate(players)]
        board = BoardModel(diagonal=diagonal)
        random_id = self.random_id
        game_data = {'game_id': random_id, 'players': players, 'board': board}
        new_game = GameModel(**game_data)
        self.BOARD_GAMES[random_id] = new_game
        database_id = 0

        if self.connected_database:
            database_data = {'game_id': random_id,
                             'players': self.to_json([player.source for player in players]),
                             'board': board.to_json,
                             'status': IN_PROCESS,
                             'winner': 0,
                             'last_step': 0
                             }
            database_id = self.connected_database.create_game(**database_data)

        return self.BOARD_GAMES[random_id], database_id


    def get_game(self, game_id: str) -> GameModel:
        if game_id not in self.BOARD_GAMES:
            if self.connected_database:
                game_data = self.get_game_from_database(game_id=game_id)
                if game_data:
                    return game_data
            raise exceptions.GameNotFoundException(game_id=game_id)

        return self.BOARD_GAMES[game_id]
    
    def is_player_in_game(self, game_id: str, player_id: int) -> bool:
        game = self.get_game(game_id)
        players = (player.id for player in game.players)
        return player_id in players

    def is_player_busy(self, player_id: int) -> bool:
        if self.connected_database:
            games = self.get_games_from_database()
        else:
            games = self.BOARD_GAMES.values()

        for game in games:
            if self.is_player_in_game(game.game_id, player_id) and game.status in [IN_PROCESS]:
                return True

        return False

    def select(self, game_id: str, player_id: int, pos: int) -> None:
        game: GameModel = self.get_game(game_id)
        in_game = self.is_player_in_game(game_id, player_id)
        if not in_game:
            raise exceptions.PlayerNotInGameException(player_id=player_id)

        game.select(player_id, pos)


        if self.connected_database:
            database_data = {
                "status": game.status,
                "winner": game.winner,
                "last_step": game.last_step,
                "board": game.board.to_json
            }
            self.connected_database.update_game(game_id, **database_data)
    
    def get_winner(self, game_id: str) -> int:
        game = self.get_game(game_id)
        return game.winner

    def from_json(self, data: Union[str, bytes]) -> Union[list, dict]:
        return json.loads(data)

    def to_json(self, data: Union[list, dict]) -> Union[str, bytes]:
        return json.dumps(data)


    def get_game_from_database(self, **options):
        if not self.connected_database:
            raise exceptions.NoDatabaseConnected()

        game = self.connected_database.get_game(**options)
        if game:
            game['board'] = BoardModel(self.from_json(game['board']))
            game['players'] = [PlayerModel(**player) for player in self.from_json(game['players'])]

        return GameModel(**game)

    def get_games_from_database(self, **options):
        if not self.connected_database:
            raise exceptions.NoDatabaseConnected()

        games = self.connected_database.get_games(**options)
        for game in games:
            game['board'] = BoardModel(self.from_json(game['board']))
            game['players'] = [PlayerModel(**player) for player in self.from_json(game['players'])]

        return [GameModel(**game) for game in games]

    def get_game_by_game_id(self, game_id: str):
        if not self.connected_database:
            raise exceptions.NoDatabaseConnected()

        return self.connected_database.get_game(game_id=game_id)

    def get_game_by_auto_id(self, id: int):
        if not self.connected_database:
            raise exceptions.NoDatabaseConnected()

        return self.connected_database.get_game(id=id)

    def is_draw(self, game_id: str):
        game = self.get_game(game_id)
        return game.board.all_cells_selected
