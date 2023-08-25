import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from database import sqlite_db
from keyboards import admin_kb
from keyboards import client_kb
from create_bot import bot


class FSMAdmin(StatesGroup):
    """
    Состояние для отправки уведомления
    """
    file_txt = State()
    time_out = State()
    message = State()


async def exit_command(message: types.Message):
    """Выход из Рабочего состояния"""
    await bot.send_message(
        message.from_user.id,
        'До встречи хозяин, возвращайся поскорее!',
        reply_markup=client_kb.kb_client
    )
    await message.delete()


async def cancel_command(message: types.Message, state: FSMContext):
    """Очистка базы данных"""
    await sqlite_db.clear_table()
    await state.finish()
    await message.reply('ОК! Попробуйте заново!')


async def cm_start(message: types.Message):
    """Старт ввода данных для внесения их в таблицу"""
    await FSMAdmin.file_txt.set()
    await message.reply(
        'Загрузи файл-txt',
        reply_markup=admin_kb.button_case_admin
    )


async def load_txt_command(message: types.Message, state: FSMContext):
    """Загрузка данных из файла-txt
       Формат данных данных в файле
       Пример(Файл-txt):
                       13215948653
                       45646545465
                       54545231564
                       ...
    """
    try:
        file_name = message.document.file_name
        await message.document.download(destination_file=file_name)
        with open(file_name) as file:
            for user in file:
                await sqlite_db.add_user(user.replace('\n', ''))
        await FSMAdmin.next()
        await message.reply(
            'Укажите интервал отправки '
            'Сообщения/Уведомления/Рекламы'
        )
    except:
        await message.reply('Недопустимый файл!')
        await sqlite_db.clear_table()
        await state.finish()


async def timeout_command(message: types.Message, state: FSMContext):
    """Заполнение данных:
       Интервал отправки сообщений пользователей
       Целые числа формат в минутах
    """
    if message.text.isdigit():
        await sqlite_db.add_timeout(message.text)
        await FSMAdmin.next()
        await message.reply(
            'Напишите сообщение которое хотите отправить!'
        )
    else:
        await message.reply('Недопустимый тип данных')
        await sqlite_db.clear_table()
        await state.finish()


async def load_message_command(message: types.Message, state: FSMContext):
    """Заполенние данных:
       Какое сообщегие будет отправлятся пользователям
    """
    await sqlite_db.add_message(message.text)
    await bot.send_message(message.from_user.id, 'Данные успещно обработаны!')
    await state.finish()


async def report_user_message_command(message: types.Message):
    """Вывод данных пользователю.
       Данные о активных и не активных пользователей
       Какие сообщения были отправлена
    """
    await sqlite_db.sql_read(message)


async def send_all_command(message: types.Message):
    """Отправка сообщений с интервалом указанным пользователем
       в течении 24-х часов
    """
    users = await sqlite_db.get_user()
    if users:
        send = True
        COUNT_SEND = 0
        timeout = int(users[0][1]) * 60  # интервалы отправки (берется из базы)
        TIMER_END = 24 * 60 * 60  # в течении суток
        await bot.send_message(
            message.from_user.id,
            f'Отправили! Следующая отправка сообщения'
            f' каждые {users[0][1]} минут!',
            reply_markup=admin_kb.button_case_report_admin
        )
        while send:
            COUNT_SEND += 1
            if TIMER_END / timeout >= COUNT_SEND:
                for user in users:
                    try:
                        await bot.send_message(user[0], user[2])
                        if user[3] != 'Активен':
                            await sqlite_db.set_active(user[0], 'Активен')
                    except:
                        await sqlite_db.set_active(user[0], 'Не Активен')
                await asyncio.sleep(timeout)
            else:
                await bot.send_message(
                    message.from_user.id,
                    'Отправка завершена!',
                )
                send = False
    else:
        await bot.send_message(message.from_user.id, 'База данных пустая!')


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(
        cancel_command,
        state='*',
        commands='отмена'
    )
    dp.register_message_handler(
        cancel_command,
        Text(equals='отмена', ignore_case=True),
        state='*'
    )
    dp.register_message_handler(
        exit_command,
        commands=['выход']
    )
    dp.register_message_handler(
        cm_start,
        commands=['Загрузить'],
        state=None
    )
    dp.register_message_handler(
        load_txt_command,
        content_types=['document'],
        state=FSMAdmin.file_txt
    )
    dp.register_message_handler(
        timeout_command,
        state=FSMAdmin.time_out
    )
    dp.register_message_handler(
        load_message_command,
        state=FSMAdmin.message
    )
    dp.register_message_handler(
        report_user_message_command,
        commands=['отчет']
    )
    dp.register_message_handler(
        send_all_command,
        commands=['отправить']
    )
    