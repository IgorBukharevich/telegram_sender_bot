from aiogram import types, Dispatcher
from create_bot import bot


async def echo_send(message: types.Message):
    await bot.send_message(message.from_user.id, 'Ошибка! Нет такой команды!')


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
