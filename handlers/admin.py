import os

from dotenv import load_dotenv

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from app.keyboards import (
    players_keyboard,
    start_keyboard,
    admin_keyboard,
    new_game_keyboard,
)
from app.rating_module import Rating
from app.game_module import Game

from bot import dp

load_dotenv()


class ClientState(StatesGroup):
    """Contains current states"""

    START_STATE = State()
    PLAYER_INFO_SELECT = State()
    CREATE_MATCH = State()
    CHOOSED_PLAYER_A = State()
    CHOOSED_PLAYER_B = State()
    SCORE_PLAYER_A = State()
    SCORE_PLAYER_B = State()
    MATCH_COMPLETE = State()
    NEW_MATCH = State()


stats = Rating()


@dp.message_handler(state="*", text="🏓Create a game🏓")
async def choose_player_a(message: types.Message, state: FSMContext):
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        msg = "Choose player A"

        await message.answer(msg, reply_markup=players_keyboard())
        await state.set_state(ClientState.CREATE_MATCH)

    else:
        msg = "You don't have roots for that"

        await message.answer(msg)


@dp.message_handler(
    lambda message: message.text not in stats.get_players_list(),
    state=ClientState.CREATE_MATCH,
)
async def invalid_player_a(message: types.Message, state: FSMContext):
    msg = "Invalid player"

    await state.finish()
    return await message.answer(msg)


@dp.message_handler(state=ClientState.CREATE_MATCH)
async def choose_player_b(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(PLAYER_A=user_msg)

    msg = "Choose player B"
    await message.answer(msg, reply_markup=players_keyboard())
    await state.set_state(ClientState.CHOOSED_PLAYER_A)


@dp.message_handler(
    lambda message: message.text not in stats.get_players_list()
    and message.text != "/start",
    state=ClientState.CHOOSED_PLAYER_A,
)
async def invalid_player_b(message: types.Message, state: FSMContext):
    msg = "Invalid player"

    return await message.answer(msg)


@dp.message_handler(state=ClientState.CHOOSED_PLAYER_A)
async def select_score_a(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(PLAYER_B=user_msg)

    match_info = await state.get_data()
    player_a = match_info["PLAYER_A"]

    msg = f"Enter the score of {player_a}"
    await message.answer(msg, reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(ClientState.SCORE_PLAYER_A)


@dp.message_handler(
    lambda message: not message.text.isdigit(), state=ClientState.SCORE_PLAYER_A
)
async def invalid_score_a(message: types.Message):
    msg = "Счет должен быть числом"
    return await message.reply(msg)


@dp.message_handler(state=ClientState.SCORE_PLAYER_A)
async def select_score_b(message: types.Message, state: FSMContext):
    user_msg = message.text

    await state.update_data(SCORE_A=user_msg)

    match_info = await state.get_data()
    player_b = match_info["PLAYER_B"]

    msg = f"Enter the score of {player_b}"
    await message.answer(msg)
    await state.set_state(ClientState.SCORE_PLAYER_B)


@dp.message_handler(
    lambda message: not message.text.isdigit(), state=ClientState.SCORE_PLAYER_B
)
async def invalid_score_b(message: types.Message):
    msg = "Счет должен быть числом"
    return await message.reply(msg)


@dp.message_handler(state=ClientState.SCORE_PLAYER_B)
async def update_match(message: types.Message, state: FSMContext):
    user_msg = message.text
    await state.update_data(SCORE_B=user_msg)

    stats = Rating()

    match_info = await state.get_data()

    player_a = match_info["PLAYER_A"]
    player_a_id = stats.message_to_player_id(player_a)

    player_b = match_info["PLAYER_B"]
    player_b_id = stats.message_to_player_id(player_b)

    score_a = int(match_info["SCORE_A"])
    score_b = int(match_info["SCORE_B"])

    game = Game(player_a_id, player_b_id, score_a, score_b)

    winner = game.winner_name()
    elo_gained = game.winner_elo_gain()
    winner_elo = game.winner_points()

    loser = game.loser_name()
    elo_lost = game.loser_elo_lost()
    loser_elo = game.loser_points()

    game.update_elo()
    game.update_stats()

    msg = f"""{player_a} : {score_a} - {score_b} : {player_b}\n
    🏆Победитель - <b>{winner}</b>🏆\n 
    Рейтинга получено <b>{elo_gained}</b>
    Текущий рейтинг {winner} - {winner_elo}\n
    ❌Проигравший - <b>{loser}</b>❌\n 
    Рейтинга потеряно <b>{elo_lost}</b>
    Текущий рейтинг {loser} - {loser_elo}"""

    await message.answer(
        msg, parse_mode=types.ParseMode.HTML, reply_markup=new_game_keyboard()
    )
    # await bot.send_message(chat_id=int(os.getenv("CHANNEL_CHAT_ID")), text=msg, parse_mode=types.ParseMode.HTML)
    await state.set_state(ClientState.NEW_MATCH)


@dp.message_handler(state=ClientState.NEW_MATCH)
async def new_match(message: types.Message, state: FSMContext):
    user_msg = message.text

    if user_msg == "⬅️ Back":
        await state.finish()


@dp.message_handler(Text(equals="⬅️ Back"), state="*")
async def back_to_start_menu(message: types.Message, state: FSMContext):
    """Start menu handler"""
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        msg = """Here's admin start menu"""

        await message.answer(msg, reply_markup=admin_keyboard())
    else:
        msg = """Here's start menu"""

        await message.answer(msg, reply_markup=start_keyboard())

    await state.set_state(ClientState.START_STATE)


# Register handlers
def register_handlers_admin(dp: Dispatcher) -> None:
    dp.register_message_handler(
        choose_player_a, Text(equals="🏓Create a game🏓"), state="*"
    )
    dp.register_message_handler(choose_player_b, state=ClientState.CREATE_MATCH)
    dp.register_message_handler(select_score_a, state=ClientState.CHOOSED_PLAYER_A)
    dp.register_message_handler(select_score_b, state=ClientState.SCORE_PLAYER_A)
    dp.register_message_handler(update_match, state=ClientState.SCORE_PLAYER_B)
    dp.register_message_handler(new_match, state=ClientState.NEW_MATCH)
    dp.register_message_handler(
        invalid_score_a,
        lambda message: not message.text.isdigit(),
        state=ClientState.SCORE_PLAYER_A,
    )
    dp.register_message_handler(
        invalid_score_b,
        lambda message: not message.text.isdigit(),
        state=ClientState.SCORE_PLAYER_B,
    )
    dp.register_message_handler(back_to_start_menu, Text(equals="⬅️ Back"), state="*")
