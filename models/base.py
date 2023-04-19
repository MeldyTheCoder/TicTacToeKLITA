import json
from typing import Union

BOARD_TYPE = list[dict[str, Union[str, int]]]
COMBINATION_TYPE = list[list[int]]


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