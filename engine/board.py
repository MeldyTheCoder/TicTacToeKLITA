import math
from .base import BaseModel, CIRCLE, CROSS, BOARD_TYPE, MIN_DIAGONAL, NONE
from .combination import Combination

class BoardModel(BaseModel):
    def __init__(self, configured_board: BOARD_TYPE = None, diagonal: int = 3):
        self.data = configured_board if configured_board else self.__empty_board(diagonal=diagonal)

    def __empty_board(self, diagonal: int):
        if diagonal < MIN_DIAGONAL:
            raise Exception("Invalid diagonal value!")

        total_cells = int(math.pow(diagonal, 2))
        board = [{"selected": NONE, "id": cell} for cell in range(total_cells)]
        return board

    @property
    def diagonal(self) -> int:
        return int(math.sqrt(len(self.data)))

    @property
    def total_cells(self) -> int:
        return len(self.data)

    def extended_combinations(self, *combinations: Combination) -> Combination:
        combinations_new = []

        for combination in combinations:
            combinations_new.extend(combination)

        return Combination(combinations_new)

    def combinations(self) -> tuple[Combination, Combination, Combination]:
        total_cells, cells_in_row = self.total_cells, self.diagonal

        vertical_combinations = Combination(list([i + row for i in range(0, total_cells, cells_in_row)] for row in range(cells_in_row)))
        horizontal_combinations = Combination(list([i + (cells_in_row * column) for i in range(0, cells_in_row)] for column in range(cells_in_row)))
        diagonal_combinations = Combination(list([combination[pos] for pos, combination in enumerate(horizontal_combinations[::index])] for index in [1, -1]))

        return vertical_combinations, horizontal_combinations, diagonal_combinations

    def select(self, choice: str, id: int):
        if choice not in [CROSS, CIRCLE]:
            raise Exception("Invalid choice option!")

        total_cells, diagonal = self.total_cells, self.diagonal

        if id < 0 or id > total_cells:
            raise Exception(f"There is no cell with position %{id}%!")

        self.data[id]["selected"] = choice
        return BoardModel(self.data)

    def get_winner(self):
        vertical_combinations, horizontal_combinations, diagonal_combinations = self.combinations()
        combinations = self.extended_combinations(vertical_combinations, horizontal_combinations, diagonal_combinations)

        for combination in combinations:
            values = set(self.data[index]['selected'] for index in combination)
            if len(values) == 1 and NONE not in values:
                return values.pop()
            return None