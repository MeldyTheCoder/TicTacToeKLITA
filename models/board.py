import math
from models.base import BaseModel, BOARD_TYPE
from models.constants import CIRCLE, CROSS, NONE, MIN_BOARD_DIAGONAL
from models.combination import Combination
from models import exceptions
from typing import Union
from collections import Counter

class BoardModel(BaseModel):
    MARKS_TO_WIN = 3

    def __init__(self, configured_board: BOARD_TYPE = None, diagonal: int = 3):
        self.data = configured_board if configured_board else self.__empty_board(diagonal=diagonal)

    def __empty_board(self, diagonal: int):
        if diagonal < MIN_BOARD_DIAGONAL:
            raise exceptions.InvalidBoardDiagonalException(MIN_BOARD_DIAGONAL)

        total_cells = int(math.pow(diagonal, 2))
        board = [{"selected": NONE, "id": cell} for cell in range(total_cells)]
        return board

    def get_cell_diagonal_neighbours(self, cell_id: int):
        diagonal = self.diagonal
        combinations = []

        cell_in_row_pos = cell_id % diagonal
        cells_in_row_left = diagonal - cell_in_row_pos
        row_index = cell_id // diagonal
        rows_left = diagonal - row_index

        # Up Left
        if (cell_in_row_pos >= self.MARKS_TO_WIN) and (row_index > self.MARKS_TO_WIN):
            combinations.append([cell_id - (diagonal + 1) * point for point in range(self.MARKS_TO_WIN)])

        # Up Right
        if (cell_in_row_pos < self.MARKS_TO_WIN) and (row_index > self.MARKS_TO_WIN):
            combinations.append([cell_id - (diagonal - 1) * point for point in range(self.MARKS_TO_WIN)])

        # Down Right
        if (cells_in_row_left >= self.MARKS_TO_WIN) and (row_index < self.MARKS_TO_WIN):
            combinations.append([cell_id + (diagonal + 1) * point for point in range(self.MARKS_TO_WIN)])

        # Down Left
        if (cell_in_row_pos >= self.MARKS_TO_WIN - 1) and (row_index < self.MARKS_TO_WIN):
            combinations.append([cell_id + (diagonal - 1) * point for point in range(self.MARKS_TO_WIN)])

        combinations = list(filter(lambda comb: max(comb) <= diagonal ** 2 - 1, combinations))
        return combinations

    @property
    def diagonal(self) -> int:
        return int(math.sqrt(len(self.data)))

    @property
    def total_cells(self) -> int:
        return len(self.data)

    def extended_combinations(self) -> Combination:
        combinations_new = self.vertical_combinations.source\
                           + self.horizontal_combinations.source\
                           + self.diagonal_combinations.source

        return Combination(combinations_new)

    @property
    def diagonal_combinations(self) -> Combination:
        combinations = []
        for cell in range(self.total_cells):
            combinations += self.get_cell_diagonal_neighbours(cell)
        return Combination(combinations)

    @property
    def horizontal_combinations(self) -> Combination:
        diagonal = self.diagonal

        board_combinations = []
        board_columns = [self.data[diagonal * row:diagonal * (row + 1)] for row in range(diagonal)]

        for board_column in board_columns:
            board_combinations += [[cell["id"] for cell in board_column[from_index:from_index + self.MARKS_TO_WIN]] for
                                   from_index in range(diagonal)]

        board_combinations = list(filter(lambda combination: len(combination) == self.MARKS_TO_WIN, board_combinations))
        return Combination(board_combinations)

    @property
    def vertical_combinations(self) -> Combination:
        diagonal = self.diagonal

        board_combinations = []
        board_rows = [[self.data[cell + row] for cell in range(0, self.total_cells, diagonal)] for row in range(diagonal)]
        for board_row in board_rows:
            board_combinations += [[cell["id"] for cell in board_row[from_index:from_index + self.MARKS_TO_WIN]] for
                                   from_index in range(diagonal)]

        board_combinations = list(filter(lambda combination: len(combination) == self.MARKS_TO_WIN, board_combinations))
        return Combination(board_combinations)


    def select(self, choice: str, id: int):
        if choice not in [CROSS, CIRCLE]:
            raise exceptions.MarkSymbolException(choice)

        total_cells, diagonal = self.total_cells, self.diagonal

        if id < 0 or id > total_cells:
            raise exceptions.BoardCellNotFound(id)

        if self.data[id]['selected'] not in [NONE]:
            raise exceptions.BoardCellAlreadySelected(id)

        self.data[id]["selected"] = choice
        return BoardModel(self.data)

    @property
    def all_cells_selected(self) -> bool:
        return len(list(filter(lambda cell: cell['selected'] in [CROSS, CIRCLE], self.data))) == self.total_cells

    def get_winner(self) -> Union[CROSS, CIRCLE, NONE]:
        combinations = self.extended_combinations()

        for combination in combinations:
            values = list(self.data[index]['selected'] for index in combination)
            points = Counter(values).most_common(3)
            if points[0][1] == self.MARKS_TO_WIN and points[0][0] in [CROSS, CIRCLE]:
                return points[0][0]
        return NONE