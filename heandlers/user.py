from aiogram import types, Dispatcher
from create_bot import db,dp


async def startBot(msg: types.Message):
    user_id = msg.from_user.id
    if not db.userExists(user_id):
       await msg.reply(f'''Ваш аккаунт успешно создан, дождитесь выдачи роли!''')
       db.addUser(user_id)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        if db.isEmployeeActive(user_id):
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button = types.KeyboardButton("/ASIN")
            keyboard.add(button)
        await msg.reply(f'''Привет <a href='tg://user?id={user_id}'>{msg.from_user.full_name}</a>! Если у тебя не появились кнопки внизу, то дождись выдачи роли!''',
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard
            )
        
async def errorMsg(msg: types.Message):
    await msg.reply(f'''Простите, но у нас нет такой команды, воспользуйтесь командой /start, что бы у вас появились кнопки!''')
    
def heandlersClient(dp: Dispatcher):
    dp.register_message_handler(startBot, commands=["start"], state=None)
    dp.register_message_handler(errorMsg, state=None)