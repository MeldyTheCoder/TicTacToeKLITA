from .base import BaseModel, IN_PROCESS, CLOSED, DRAW
from .player import PlayerModel
from .board import BoardModel
from typing import Optional

class GameModel(BaseModel):
    def __init__(self, game_id: str, players: list[PlayerModel], board: BoardModel, **kwargs):
        self.__game_id: str = game_id
        self.__players: list[PlayerModel] = players
        self.__board: BoardModel = board
        self.__status: int = IN_PROCESS
        self.__winner: int = 0
        self.__last_step: int = 0

        kwargs = {f"__{key}": val for key, val in kwargs.items() if key and val}
        self.__dict__.update(**kwargs)

    @property
    def status(self) -> int:
        return self.__status

    @status.setter
    def status(self, new_status: int) -> None:
        if new_status not in [IN_PROCESS, DRAW, CLOSED]:
            raise Exception(f"No such status %{new_status}")
        self.__status = new_status

    @property
    def winner(self) -> int:
        if not self.__winner:
            winner_mark = self.board.get_winner()
            players_filtered = list(filter(lambda player: player.mark_symbol == winner_mark, self.__players))
            if players_filtered:
                self.__winner = players_filtered[0].id
                return self.__winner

        return self.__winner


    @property
    def board(self) -> BoardModel:
        return self.__board

    @property
    def players(self) -> list[PlayerModel]:
        return self.__players

    @property
    def game_id(self) -> str:
        return self.__game_id

    @property
    def last_step(self):
        return self.__last_step

    def select(self, player_id: int, pos: int) -> None:
        if self.__last_step == player_id:
            raise Exception("This player has been already stepped!")

        player = self.get_player(player_id)
        if not player:
            raise Exception("No such player in this game!")

        self.__board = self.board.select(player.mark_symbol, pos)
        self.__last_step = player_id

    def get_player(self, user_id: int) -> Optional[PlayerModel]:
        if not user_id:
            return None
        try:
            return list(filter(lambda player: player.id == user_id, self.players))[0]
        except:
            return None

