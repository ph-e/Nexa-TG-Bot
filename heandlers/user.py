from aiogram import types, Dispatcher
from create_bot import db,dp


async def startBot(msg: types.Message):
    user_id = msg.from_user.id
    if not await db.userExists(user_id):
       await msg.reply(f'''Ваш аккаунт успешно создан, дождитесь выдачи роли!''')
       await db.addUser(user_id)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if await db.isEmployeeActive(user_id):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("/help")
            keyboard.add(button)
        await msg.reply(f'''Привет <a href='tg://user?id={user_id}'>{msg.from_user.full_name}</a>! Если у вас не появились кнопки внизу, то дождитесь выдачи роли!''',
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard
            )
        
async def errorMsg(msg: types.Message):
    await msg.reply(f'''Простите, но у нас нет такой команды, воспользуйтесь командой /help''')

async def help(msg: types.Message):
    user_id = msg.from_user.id
    if await db.isEmployeeActive(user_id):
        if await db.isCreator(user_id):
            await msg.reply(f'''
                            Вы можете получить информацию по ASIN, используйте /ASIN
                            \nВы можете Загрузить вашу таблицу в бд, просто загрузите её в бота
                            \nВы можете получить нашу бд, используйте /get
                            \nВы можете получить таблицу магазина, используйте /sku
                            \nВы можете сменить роль других участников, используйте /change
                            \nВы можете запустить пересчет цен, используйте команду /recount
                            ''')
        else:
            await msg.reply(f'''
                            Вы можете получить информацию по ASIN, используйте /ASIN
                            \nВы можете Загрузить вашу таблицу в бд, просто загрузите её в бота
                            ''')
    else:
        await msg.reply(f'''Вам еще не выдана роль!''')
    
def heandlersClient(dp: Dispatcher):
    dp.register_message_handler(startBot, commands=["start"], state=None)
    dp.register_message_handler(help, commands=["help"])
    dp.register_message_handler(errorMsg, state=None)