from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('/Помощь')
b2 = KeyboardButton('/Начать')

kb_client = ReplyKeyboardMarkup(
    resize_keyboard=True,
    one_time_keyboard=True
)

kb_client.add(b1).add(b2)
