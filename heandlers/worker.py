from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ContentType
from create_bot import db,dp,bot
import os
import pandas as pd

class StateWorker(StatesGroup):
    foundAsin = State()


async def ASIN(msg: types.Message):
    user_id = msg.from_user.id
    if db.isEmployeeActive(user_id):
        await StateWorker.foundAsin.set()
        await msg.reply(f'''Отправьте мне ASIN для поиска!''')
    else:
        await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')


async def found(msg: types.Message, state: StateWorker):
    user_id = msg.from_user.id
    await state.finish()
    asin_list = msg.text.splitlines()
    if bool(len(db.foundAsin(asin_list))):
        await msg.reply(f'''ASIN успешно найден, мы формируем файл с информацией он нем''')
        file_path = 'result.xlsx'
        with open(file_path, 'rb') as file:
            await bot.send_document(user_id, file, caption='Результат вашего запроса')
        os.remove(file_path)
    else:
        await msg.reply(f'''ASIN не найден в бд, проверьте корректность ввода''')


async def addItem(msg: types.Message):
    # Проверяем, что это файл Excel (xlsx)
    if msg.document.mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        user_id = msg.from_user.id
        if db.isEmployeeActive(user_id):

            # Получаем информацию о файле
            file_info = await bot.get_file(msg.document.file_id)
            file_path = file_info.file_path

            # Скачиваем файл
            downloaded_file = await bot.download_file(file_path)

            # Генерируем путь для сохранения файла в текущей директории
            save_path = os.path.join(os.getcwd(), msg.document.file_name)

            # Сохраняем файл
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file.read())
            
            # Сохраняем таблицу в бд!
            df = pd.read_excel(msg.document.file_name)
            db.readExcelToDb(df)
            os.remove(save_path)
            await msg.reply(f'''Ваши данные успешно перенесены в нашу БД!''')
        else:
            await msg.reply(f'''Отказано в доступе! Вы не являетесь действующим сотрудником, либо у вас нет полходящей роли! Дождитесь выдачи и попробуйте еще раз.''')
    else:
        await msg.reply(f'''Мы не можем загрузить ваш файл!''')


def heandlersWorker(dp: Dispatcher):
    dp.register_message_handler(ASIN, commands=["ASIN"], state=None)
    dp.register_message_handler(found, state=StateWorker.foundAsin)
    dp.register_message_handler(addItem, content_types=ContentType.DOCUMENT)