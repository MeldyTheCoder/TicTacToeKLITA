from engine.base import BaseModel, CIRCLE, CROSS
from engine.board import BoardModel
from typing import Union

class PlayerModel(BaseModel):
    def __init__(self, id: int, mark_symbol: Union[CIRCLE, CROSS]):
        if mark_symbol not in [CIRCLE, CROSS]:
            raise Exception(f"No such mark symbol %{mark_symbol}%")

        self.mark_symbol = mark_symbol
        self.id = id
        self.data = {'id': id, 'mark_symbol': mark_symbol}

