import json
from models.board import BoardModel
from models.base import NONE, CIRCLE, CROSS
from config import BOARD_DIAGONALS_AVAILABLE
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class Keyboards:
    def __init__(self):
        pass

    def new_game(self):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton(text='➕ Новая игра', callback_data=json.dumps({'action': 'new_game'})))
        return kb

    def new_game_categories(self):
        kb = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton(text=f"{diagonal}x{diagonal}",
                                 callback_data=json.dumps({'action': 'new_game', 'diag': diagonal}))
            for diagonal in BOARD_DIAGONALS_AVAILABLE
        ]
        kb.add(*buttons)
        return kb

    def board_keyboard(self, game_id: int, board: BoardModel):
        kb = InlineKeyboardMarkup(row_width=board.diagonal)
        icons = {CROSS: "❌", CIRCLE: "⭕️", NONE: "⬜️"}
        buttons = [
            InlineKeyboardButton(text=icons[cell['selected']], callback_data=json.dumps({"action": "select", "id": game_id, "pos": cell['id']}))
            for cell in board.source
        ]

        kb.add(*buttons)
        return kb

    def accept_game_keyboard(self, board: int):
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(InlineKeyboardButton(text='✅ Принять', callback_data=json.dumps({'action': 'accept_game', 'diag': board})))
        return kb