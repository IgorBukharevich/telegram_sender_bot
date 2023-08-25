from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import kb_client, admin_kb


async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Здравствуйте! Я бот, '
        'который поможет вам '
        'отправлять рассылку ('
        'Рекламу/Уведомления): '
        'группам/каналам/пользователям!',
        reply_markup=kb_client
    )
    await message.delete()


async def help_command(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Начало работы!\n'
        'Введите команду перехода в рабочий режим -> "/Начать"\n'
        'Далее нажмите кнопку или введите команду -> "Загрузить"\n'
        'Следуйте моим инструкциям!\n'
        '-----------------------------------------------------\n'
        'В случае если вы передумали или допустили ошибку при \n'
        'заполнении данных, введите команду ------------> "/Отмена"\n'
        'Если вы решили совершить повторуную отправку, повторите \n'
        'предыдущие действия!\n'
        'Спасибо за внимание! =)'
    )


async def activate_command(message: types.Message):
    await bot.send_message(
        message.from_user.id, 'Что хозяин надо???',
        reply_markup=admin_kb.button_case_admin
    )

    await message.delete()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(help_command, commands=['помощь'])
    dp.register_message_handler(activate_command, commands=['начать'])
    