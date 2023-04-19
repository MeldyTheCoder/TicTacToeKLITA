import os
from typing import Union

class NoDatabaseException(Exception):
    text = 'No database connected!'

    def __str__(self):
        return self.text


class NotEnoughPlayersException(Exception):
    text = 'Game requires %{min_players} players.'

    def __init__(self, min_players: int):
        self.text = self.text.format(min_players=min_players)

    def __str__(self):
        return self.text

class PlayerNotFoundException(Exception):
    text = 'Player %{player_id} not found!'

    def __init__(self, player_id: int):
        self.text = self.text.format(player_id=player_id)

    def __str__(self):
        return self.text


class GameNotFoundException(Exception):
    text = 'Game %{game_id} not found!'

    def __init__(self, game_id: Union[str, int]):
        self.text = self.text.format(game_id=game_id)

    def __str__(self):
        return self.text

class GameStatusException(Exception):
    text = 'No such status %{status}'

    def __init__(self, status: int):
        self.text = self.text.format(status=status)

    def __str__(self):
        return self.text

class PlayerNotInGameException(Exception):
    text = 'Player %{player_id} is not in this game!'

    def __init__(self, player_id: int):
        self.text = self.text.format(player_id=player_id)

    def __str__(self):
        return self.text

class MarkSymbolException(Exception):
    text = 'No such game mark symbol %{mark_symbol}'

    def __init__(self, mark_symbol: str):
        self.text = self.text.format(mark_symbol=mark_symbol)

    def __str__(self):
        return self.text

class BoardCellNotFound(Exception):
    text = 'No board cell with id %{cell_id}'

    def __init__(self, cell_id: int):
        self.text = self.text.format(cell_id=cell_id)

    def __str__(self):
        return self.text

class InvalidBoardDiagonalException(Exception):
    text = 'Minimal value of board diagonal is %{min_diagonal}.'

    def __init__(self, min_diagonal: int):
        self.text = self.text.format(min_diagonal=min_diagonal)

    def __str__(self):
        return self.text

class DatabaseNoArgumentsPassed(Exception):
    text = 'No arguments passed'

    def __str__(self):
        return self.text

class NoDatabaseFoundException(Exception):
    text = 'No database on path %{path}'

    def __init__(self, path: Union[str, os.PathLike]):
        self.text = self.text.format(path=path)

    def __str__(self):
        return self.text

class NoDatabaseConnected(Exception):
    text = 'No database connected!'

    def __str__(self):
        return self.text

class PlayerAlreadySteppedException(Exception):
    text = 'Player has been already stepped!'

    def __str__(self):
        return self.text

class BoardCellAlreadySelected(Exception):
    text = 'Cell with id %{cell_id} has been already selected!'

    def __init__(self, cell_id: int):
        self.text = self.text.format(cell_id=cell_id)

    def __str__(self):
        return self.text