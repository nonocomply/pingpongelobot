from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types
from app.rating_module import Rating


class Buttons:
    """Contains buttons"""

    stats_btn = KeyboardButton("Show player stats📊")
    leaderboard_btn = KeyboardButton("Show leaderboard🏆")
    match_btn = KeyboardButton("🏓Create a game🏓")
    back_btn = KeyboardButton("⬅️ Back")


# Start menu keyboard


def start_keyboard() -> types.ReplyKeyboardMarkup:
    stats_btn = Buttons.stats_btn
    leaderboard_btn = Buttons.leaderboard_btn

    start_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    # start_keyboard.row(match_btn)
    start_keyboard.row(stats_btn, leaderboard_btn)

    return start_keyboard


# Admin menu keyboard


def admin_keyboard() -> types.ReplyKeyboardMarkup:
    stats_btn = Buttons.stats_btn
    leaderboard_btn = Buttons.leaderboard_btn
    match_btn = Buttons.match_btn

    admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    admin_keyboard.row(match_btn)
    admin_keyboard.row(stats_btn, leaderboard_btn)

    return admin_keyboard


# Players menu keyboard


def players_keyboard() -> types.ReplyKeyboardMarkup:
    players_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

    stats = Rating()
    player_names = stats.get_players_list()

    back_btn = Buttons.back_btn

    keys = [KeyboardButton(item) for item in player_names]
    keys.append(back_btn)
    keys = tuple(keys)

    players_keyboard.add(*keys)

    return players_keyboard


# New game menu


def new_game_keyboard() -> types.ReplyKeyboardMarkup:
    match_btn = Buttons.match_btn
    back_btn = Buttons.back_btn

    new_game_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    new_game_keyboard.add(match_btn, back_btn)

    return new_game_keyboard
