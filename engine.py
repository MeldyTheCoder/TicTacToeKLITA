import json
import os
import random
import string
import config
from typing import Union
from engine.board import BoardModel
from engine.base import CIRCLE, CROSS, IN_PROCESS
from engine.player import PlayerModel
from engine.game import GameModel
from engine.database import Database

class GameEngine:
    BOARD_GAMES: dict = {}
    PLAYERS_REQUIRED = 2

    def __init__(self, use_db: bool = False):
        self.connected_database = Database(config.DATABASE_PATH) if use_db else None

    @property
    def random_id(self) -> str:
        length = 10
        letters = string.ascii_letters + string.digits
        return "".join([random.choice(letters) for i in range(length)])

    def new_game(self, players: list[int], diagonal: int = 3) -> GameModel:
        if len(players) == self.PLAYERS_REQUIRED:
            raise Exception(f"There are {self.PLAYERS_REQUIRED} required!")

        marks = [CIRCLE, CROSS]
        players = [PlayerModel(id=player, mark_symbol=marks[index]) for index, player in enumerate(players)]
        board = BoardModel(diagonal=diagonal)
        random_id = self.random_id
        game_data = {'game_id': random_id, 'players': players, 'board': board}
        new_game = GameModel(**game_data)
        self.BOARD_GAMES[random_id] = new_game

        if self.connected_database:
            database_data = {'game_id': random_id,
                             'players': self.to_json([player.source for player in players]),
                             'board': board.to_json,
                             'status': IN_PROCESS,
                             'winner': 0
                             }
            self.connected_database.create_game(**database_data)
        return self.BOARD_GAMES[random_id]


    def get_game(self, game_id: str) -> GameModel:
        if game_id not in self.BOARD_GAMES:
            if self.connected_database:
                game_data = self.get_game_from_database(game_id=game_id)
                if game_data:
                    return game_data
            raise Exception(f"No such game with id {game_id}")

        return self.BOARD_GAMES[game_id]
    
    def is_player_in_game(self, game_id: str, player_id: int) -> bool:
        game = self.get_game(game_id)
        players = (player.id for player in game.players)
        return player_id in players

    def is_player_busy(self, player_id: int) -> bool:
        for game in self.BOARD_GAMES.values():
            if self.is_player_in_game(game.game_id, player_id) and game.status in [IN_PROCESS]:
                return True
        return False

    def select(self, game_id: str, player_id: int, pos: int) -> None:
        game: GameModel = self.get_game(game_id)
        in_game = self.is_player_in_game(game_id, player_id)
        if not in_game:
            raise Exception("Player not in this game!")

        game.select(player_id, pos)

        if self.connected_database:
            self.connected_database.update_game(game_id, board=game.board.to_json)
    
    def get_winner(self, game_id: str) -> int:
        game = self.get_game(game_id)
        return game.winner

    def from_json(self, data: Union[str, bytes]) -> Union[list, dict]:
        return json.loads(data)

    def to_json(self, data: Union[list, dict]) -> Union[str, bytes]:
        return json.dumps(data)


    def get_game_from_database(self, **options):
        if not self.connected_database:
            raise Exception("No database connected!")
        game = self.connected_database.get_game(**options)
        if game:
            game['board'] = BoardModel(self.from_json(game['board']))
            game['players'] = [PlayerModel(**player) for player in self.from_json(game['players'])]

        return game

    def get_games_from_database(self, **options):
        if not self.connected_database:
            raise Exception("No database connected!")

        games = self.connected_database.get_games(**options)
        for game in games:
            game['board'] = BoardModel(self.from_json(game['board']))
            game['players'] = [PlayerModel(**player) for player in self.from_json(game['players'])]

        return games





g = GameEngine()