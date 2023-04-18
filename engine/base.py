import json
from typing import Union

CIRCLE = 'circle'
CROSS = 'cross'
NONE = 'none'

MIN_DIAGONAL = 3
DIAGONAL_CELLS_ANGLE = 2

BOARD_TYPE = list[dict[str, Union[str, int]]]
COMBINATION_TYPE = list[list[int]]

IN_PROCESS = 0
DRAW = 1
CLOSED = 2

class BaseModel:
    data: Union[list, dict]

    def __getitem__(self, item):
        return self.data[item]

    def __str__(self):
        return f"{self.__class__.__name__} -> {self.data}"

    def __repr__(self):
        return f"{self.__class__.__name__} -> {self.data}"

    @property
    def to_json(self):
        return json.dumps(self.data)

    @property
    def source(self):
        return self.data