from models.base import BaseModel, COMBINATION_TYPE

class Combination(BaseModel):
    def __init__(self, configured_combination: COMBINATION_TYPE):
        self.data = configured_combination
