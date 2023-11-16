from aiogram import types, Dispatcher
from create_bot import db,dp,bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import os

class StateCreator(StatesGroup):
    Store = State()
    Provider = State()

async def getDB(msg: types.Message):
    user_id = msg.from_user.id
    if await db.isCreator(user_id):
        await msg.reply(f'''Вот ваша база данных!''')
        file_path = 'tables.db'
        with open(file_path, 'rb') as file:
            await bot.send_document(user_id, file, caption='Результат вашего запроса')
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')

async def changerole(msg: types.Message):
    user_id = msg.from_user.id
    if await db.isCreator(user_id):
        try:
            user_id_to_change = int(msg.text.split()[1])
            new_role = msg.text.split()[2]
        except (IndexError, ValueError):
            await msg.reply(f'''Неправильный формат команды. Используйте /change <user_id> <new_role>''')
            return
        if new_role not in ['WORKER', 'CREATOR', 'USER']:
            await msg.reply(f'''Неправильная роль. Допустимые роли: WORKER, CREATOR, USER.''')
            return
        
        if not await db.userExists(user_id_to_change):
            await msg.reply(f'''Пользователь с таким telegram id не найден!!!''')
            return
        
        await db.changeRole(user_id_to_change,new_role)
        await msg.reply(f'''Роль пользователя успешно изменена!''')
    
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')


async def getExcel(msg: types.Message):
    user_id = msg.from_user.id
    if await db.isCreator(user_id):
        try:
            name = msg.text.split()[1]
        except (IndexError, ValueError):
            await msg.reply(f'''Неправильный формат команды. Используйте /sku <название магазина>''')
            return
        if bool(len(await db.getExcel(name))):
            await msg.reply(f'''Магазин успешно найден, мы формируем файл с информацией он нем''')
            file_path = 'tables.xlsx'
            with open(file_path, 'rb') as file:
                await bot.send_document(user_id, file, caption='Результат вашего запроса')
            os.remove(file_path)
        else:
            await msg.reply(f'''Магазин не найден в бд, проверьте корректность ввода''')
        
    
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')


async def recount(msg: types.Message):
    user_id = msg.from_user.id
    if await db.isCreator(user_id):
        await msg.reply(f'''Введите название магазина:''')
        await StateCreator.Store.set()
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')


async def getStore(msg: types.Message, state: StateCreator):
    name = msg.text
    if bool(len(await db.checkStore(name))):
        await msg.reply(f'''Магазин успешно найден, укажите преп для пересчета цен''')
        await StateCreator.next()
        await state.update_data(store=name)
    else:
        await msg.reply(f'''Магазин не найден в бд, проверьте корректность ввода''')
        await state.finish()

async def prep(msg: types.Message, state: StateCreator):
    prep = msg.text.splitlines()
    await msg.reply(f'''Мы получили от вас информацию, ожидайте обновления цен!''')
    data = await state.get_data()  # Await get_data() first
    name = data.get('store')
    print(name)
    print(prep)
    await state.finish()
    

def heandlerCreator(dp: Dispatcher):
    dp.register_message_handler(getDB, commands=["get"])
    dp.register_message_handler(changerole, commands=["change"])
    dp.register_message_handler(getExcel, commands=["sku"])
    dp.register_message_handler(recount, commands=["recount"])
    dp.register_message_handler(getStore, state=StateCreator.Store)
    dp.register_message_handler(prep, state=StateCreator.Provider)