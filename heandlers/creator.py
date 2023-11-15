from aiogram import types, Dispatcher
from create_bot import db,dp,bot
import os

async def getDB(msg: types.Message):
    user_id = msg.from_user.id
    if db.isCreator(user_id):
        await msg.reply(f'''Вот ваша база данных!''')
        file_path = 'tables.db'
        with open(file_path, 'rb') as file:
            await bot.send_document(user_id, file, caption='Результат вашего запроса')
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')

async def changerole(msg: types.Message):
    user_id = msg.from_user.id
    if db.isCreator(user_id):
        try:
            user_id_to_change = int(msg.text.split()[1])
            new_role = msg.text.split()[2]
        except (IndexError, ValueError):
            await msg.reply(f'''Неправильный формат команды. Используйте /change <user_id> <new_role>''')
            return
        if new_role not in ['WORKER', 'CREATOR', 'USER']:
            await msg.reply(f'''Неправильная роль. Допустимые роли: WORKER, CREATOR, USER.''')
            return
        
        if not db.userExists(user_id_to_change):
            await msg.reply(f'''Пользователь с таким telegram id не найден!!!''')
            return
        
        db.changeRole(user_id_to_change,new_role)
        await msg.reply(f'''Роль пользователя успешно изменена!''')
    
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')


def heandlerCreator(dp: Dispatcher):
    dp.register_message_handler(getDB, commands=["get"])
    dp.register_message_handler(changerole, commands=["change"])