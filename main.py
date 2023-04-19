import asyncio
import json
import config
import filters
from aiogram import types, Bot, Dispatcher, executor
from engine import GameEngine
from models import exceptions
from keyboards import Keyboards
from debug import Debug

app = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot=app)

game = GameEngine(True)
kbs = Keyboards()
debugger = Debug()

@dp.message_handler(filters.isPublic(), content_types=['text'], commands=['start'])
async def start(message: types.Message):
    player_is_busy = game.is_player_busy(message.from_user.id)
    if player_is_busy:
        text = '♐️ <b>Дурак, ты еще не закончил прошлую игру!</b>'
        return await message.reply(text)

    text = '❔ <b>Начать новую игру?</b>'
    kb = kbs.new_game()
    await message.reply(text, reply_markup=kb)

@dp.callback_query_handler(filters.query('new_game'), filters.isPublicQuery())
async def new_game(query: types.CallbackQuery):
    data = json.loads(query.data)
    player_is_busy = game.is_player_busy(query.from_user.id)
    if player_is_busy:
        text = '♐️ Дурак, ты еще не закончил прошлую игру!'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    if not query.message.reply_to_message.from_user.id == query.from_user.id:
        text = '🚫 Не твоя кнопка, ишак ебаный!'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    if 'diag' not in data:
        text = '<b>Выбери размер поля, шакал ебаный</b> ⤵️'
        kb = kbs.new_game_categories()
        return await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)

    text = f'❔ <b>Принять запрос на игру от дебила?</b>\n\n<b>Поле</b>: <code>{data["diag"]}x{data["diag"]}</code>'
    kb = kbs.accept_game_keyboard(board=data['diag'])
    await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)

@dp.callback_query_handler(filters.query('accept_game'), filters.isPublicQuery())
async def accept_game(query: types.CallbackQuery):
    data = json.loads(query.data)

    if query.message.reply_to_message.from_user.id == query.from_user.id:
        text = '🚫 Долбоеб, ты и предложил всем играть...'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    game_object, database_id = game.new_game([query.from_user.id, query.message.reply_to_message.from_user.id], data['diag'])

    text = f'''
💬 <b>Игра началась!</b>
    
⚰️ <b>Поле</b>: <code>{data['diag']}x{data['diag']}</code>
    
👤 <b>Игроки</b>:
├ {query.message.reply_to_message.from_user.first_name}
└ {query.from_user.first_name}
    '''

    kb = kbs.board_keyboard(database_id, game_object.board)
    await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=kb)


@dp.callback_query_handler(filters.query('select'), filters.isPublicQuery())
async def select_cell(query: types.CallbackQuery):
    data = json.loads(query.data)
    await asyncio.sleep(1.2)

    try:
        game_data = game.get_game_from_database(id=data['id'])
        game.select(game_data.game_id, query.from_user.id, data['pos'])
        winner = game.get_winner(game_data.game_id)

        if winner:
            winner_chat = (await app.get_chat(winner))
            text = f'💬 <b>Выиграл</b>: {winner_chat.first_name}'
            return await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=None)

        is_draw = game.is_draw(game_data.game_id)
        if is_draw:
            text = "🤷🏿‍♂️ <b>Ну ебать ничья, хули...</b>\n\nС дороги шлендры!"
            return await app.edit_message_text(text, query.message.chat.id, query.message.message_id, reply_markup=None)

        game_data = game.get_game(game_data.game_id)
        kb = kbs.board_keyboard(data['id'], game_data.board)
        return await app.edit_message_reply_markup(query.message.chat.id, query.message.message_id, reply_markup=kb)

    except exceptions.BoardCellAlreadySelected:
        text = '🚫 Ячейка уже выбрана, мракобес!'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    except exceptions.BoardCellNotFound:
        text = '🚫 Нет такой ячейки, додик...'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    except exceptions.PlayerAlreadySteppedException:
        text = '🚫 Ты уже походил, ишак!'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    except exceptions.PlayerNotInGameException:
        text = '🚫 Ты не играешь в эту катку, дебил...'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    except exceptions.GameNotFoundException:
        text = '🚫 Игра не найдена! Упси вупси, ублюдок...'
        return await app.answer_callback_query(query.id, text, show_alert=True)

    except Exception as e:
        debugger.exception(e)
        text = '🚫 Ошибочка вышла... Ну потом повтори попытку ('
        return await app.answer_callback_query(query.id, text, show_alert=True)

if __name__ == "__main__":
    executor.start_polling(dp, fast=True)
