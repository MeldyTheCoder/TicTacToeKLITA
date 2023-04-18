import json

from aiogram import types, Bot, Dispatcher
from engine import GameEngine
from keyboards import Keyboards
import config

app = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=app)

game = GameEngine(True)
kbs = Keyboards()

@dp.message_handler(content_types=['text'], commands=['start'])
async def start(message: types.Message):
    player_is_busy = game.is_player_busy(message.from_user.id)
    if player_is_busy:
        text = '♐️ <b>Дурак, ты еще не закончил прошлую игру!</b>'
        return await message.answer(text)

    text = '❔ <b>Начать новую игру?</b>'
    keyboard = kbs.new_game()

@dp.callback_query_handler(lambda query: json.loads(query.data)['action'] == 'new_game')
async def new_game(query: types.CallbackQuery):
    data = json.loads(query.data)
    player_is_busy = game.is_player_busy(query.from_user.id)
    if player_is_busy:
        text = '♐️ Дурак, ты еще не закончил прошлую игру!'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    if 'diag' not in data:
        text = '<b>Выбери размер поля, шакал ебаный</b> ⤵️'
        kb = kbs.new_game_categories()
        return await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)

    text = f'<b>Принять запрос на игру от дебила?</b>\n\n<b>Поле</b>: <code>{data["diag"]}x{data["diag"]}</code>'
    kb = kbs.accept_game_keyboard(board=data['diag'])
    await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)

@dp.callback_query_handler(lambda query: json.loads(query.data)['action'] == 'accept_game')
async def accept_game(query: types.CallbackQuery):
    data = json.loads(query.data)

    if query.from_user.id == query.message.from_user.id:
        text = 'Долбоеб, ты и предложил всем играть...'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    game_object = game.new_game([query.message.from_user.id, query.from_user.id], data['diag'])

    text = f'''
    💬 <b>Игра началась!</b>
    
    ⚰️ <b>Поле</b>: {data['diag']}x{data['diag']}
    
    👤 <b>Игроки</b>:
    ├ {query.message.from_user.first_name}
    └ {query.from_user.first_name}
    '''

    kb = kbs.board_keyboard(0, game_object.board)
    await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)


@dp.callback_query_handler(lambda query: json.loads(query.data)['action'] == 'select')
async def select_cell(query: types.CallbackQuery):
    data = json.loads(query.data)
