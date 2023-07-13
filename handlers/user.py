import os

from dotenv import load_dotenv

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text

from app.keyboards import start_keyboard, players_keyboard, admin_keyboard
from app.rating_module import Rating

from bot import dp


load_dotenv()


class ClientState(StatesGroup):
    """Contains current states"""

    START_STATE = State()
    PLAYER_INFO_SELECT = State()


@dp.message_handler(text="⬅️ Back")
@dp.message_handler(commands=["start"])
async def start_menu(message: types.Message, state: FSMContext) -> None:
    """Start menu handler"""
    if message.from_user.id == int(os.getenv("ADMIN_ID")):
        msg = """Here's admin start menu"""

        await message.answer(msg, reply_markup=admin_keyboard())
    else:
        msg = """Here's start menu"""

        await message.answer(msg, reply_markup=start_keyboard())

    await state.set_state(ClientState.START_STATE)


@dp.message_handler(state="*", commands=["id"])
async def check_id(message: types.Message):
    """Shows your id"""
    await message.answer(f"ur id: {message.from_user.id}")


@dp.message_handler(state="*", text="Show leaderboard🏆")
async def show_leaderboard(message: types.Message):
    stats = Rating()
    leaderboard = stats.show_elo_sorted_list()

    await message.answer(leaderboard, parse_mode=types.ParseMode.HTML)


@dp.message_handler(state="*", text="Show player stats📊")
async def select_player_menu(message: types.Message, state: FSMContext):
    msg = "Select player"

    await message.answer(msg, reply_markup=players_keyboard())
    await state.set_state(ClientState.PLAYER_INFO_SELECT)


@dp.message_handler(state=ClientState.PLAYER_INFO_SELECT)
async def show_player_stats(message: types.Message, state: FSMContext):
    stats = Rating()

    player_id = stats.message_to_player_id(message.text)
    player_stats = stats.player_stats_to_message(player_id)

    await message.answer(player_stats, parse_mode=types.ParseMode.HTML)

    if message.text == "⬅️ Back" or player_id == -1:
        await state.finish()


# Register handlers
def register_handlers_user(dp: Dispatcher) -> None:
    dp.register_message_handler(
        start_menu, Text(equals="⬅️ Back"), commands=["start"], state="*"
    )
    dp.register_message_handler(check_id, state="*", commands=["id"])
    dp.register_message_handler(
        show_leaderboard, Text(equals="Show leaderboard🏆"), state="*"
    )
    dp.register_message_handler(
        select_player_menu, Text(equals="Show player stats📊"), state="*"
    )
    dp.register_message_handler(show_player_stats, state=ClientState.PLAYER_INFO_SELECT)
