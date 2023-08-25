from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_load = KeyboardButton('/Загрузить')
button_delete = KeyboardButton('/Отмена')
button_send = KeyboardButton('/Отправить')
button_exit = KeyboardButton('/Выход')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)

button_report = KeyboardButton('/Отчет')
button_case_report_admin = ReplyKeyboardMarkup(resize_keyboard=True)

button_case_admin.row(
    button_load, button_delete).add(
    button_send).add(
    button_exit)

button_case_report_admin.add(button_report).add(button_exit)
