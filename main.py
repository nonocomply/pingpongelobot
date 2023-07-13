from aiogram import executor

from handlers import admin, user

from bot import dp

def main():
    admin.register_handlers_admin(dp)
    user.register_handlers_user(dp)


if __name__ == "__main__":
    main()
    executor.start_polling(dp, skip_updates=True)
