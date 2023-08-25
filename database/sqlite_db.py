import sqlite3 as sq
from create_bot import bot


def sql_start():
    """Создание таблицы базы данных"""
    global base, cur

    base = sq.connect('hunter_send_db')
    cur = base.cursor()
    if base:
        print('Database connected OK!')
    base.execute(
        'CREATE TABLE IF NOT EXISTS list_sender('
        ' list_users TEXT PRIMARY KEY,'
        ' timeout TEXT,'
        ' message TEXT,  '
        ' active TEXT NONE)'
    )

    base.commit()


async def add_user(user_id):
    """Добавление пользователей в базу данных"""
    cur.execute(
        "INSERT INTO list_sender (list_users, active) VALUES (?, 'Активен')",
        (user_id,)
    )
    base.commit()


async def add_timeout(timeout):
    """Добавление интервалов для отправления сообщений
       в базу данных
    """
    cur.execute(
        "UPDATE list_sender SET timeout = ?",
        (timeout,)
    )
    base.commit()


async def add_message(message):
    """Добавление сообщения для отправки
       в базу данных
    """
    cur.execute(
        "UPDATE list_sender SET message = ?",
        (message,)
    )
    base.commit()


async def set_active(user_id, active):
    """Установка Активен ли пользователь или Неактивен"""
    cur.execute(
        "UPDATE list_sender SET active = ? WHERE list_users = ?",
        (active, user_id)
    )
    base.commit()


async def get_user():
    """Получание пользователей из базы даннх"""
    return cur.execute(
        "SELECT list_users, timeout, message, active FROM list_sender"
    ).fetchall()


async def sql_read(message):
    """Получение отчета о пользователях кто получил сообщения а кто нет"""
    for ret in cur.execute(
            'SELECT list_users, active FROM list_sender'
    ).fetchall():

        await bot.send_message(message.from_user.id,
                               f'{ret[0]}\n{ret[1]}')


async def clear_table():
    """Очистка таблицы базы данных"""
    cur.execute(
        "DELETE FROM list_sender"
    )
    base.commit()
