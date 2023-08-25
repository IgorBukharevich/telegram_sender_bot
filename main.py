from aiogram.utils import executor

from create_bot import dp
from handlers import client
from handlers import admin
from handlers import other
from database import sqlite_db


async def on_startup(_):
    print('Статус Бота - Онлайн')
    sqlite_db.sql_start()


async def on_shutdown(_):
    print('Статус Бота - Офлайн')


client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)


executor.start_polling(
    dp,
    skip_updates=True,
    on_startup=on_startup,
    on_shutdown=on_shutdown
)
