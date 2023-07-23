from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from users.models import User
import asyncio
from asgiref.sync import sync_to_async


bot = Bot(token="6503653218:AAEq4laa7R5Zf7pQUYJhrEWcmf7HrVriGnE")
dp = Dispatcher(bot)

async def send_telegram_message(chat_id, text):
    await bot.send_message(chat_id, text)

async def handle_start(message: types.Message):
    await message.reply("Введите ваш секретный код")

async def handle_change(message: types.Message):
    await message.reply("Введите новый секретный код")

async def handle_code(message: types.Message):
    user_message = message.text
    chat_id = message.chat.id
    try:
        old_user = await sync_to_async(User.objects.get, thread_sensitive=True)(chat_id=chat_id)
        old_user.chat_id = None
        await sync_to_async(old_user.save, thread_sensitive=True)()
    except User.DoesNotExist:
        pass

    try:
        user = await sync_to_async(User.objects.get, thread_sensitive=True)(access_code=user_message)        
        user.chat_id = chat_id
        await sync_to_async(user.save, thread_sensitive=True)()
        if user.choice == '3':
            await message.reply(f'А вы, {user.username}, админ! Вам оповещения не положены')    
        else:
            await message.reply(f'Добро пожаловать, {user.username}! Вы успешно подписались на оповещения!')
    except User.DoesNotExist:
        await message.reply('Введен не корректный код! Проверьте код в вашем профиле http://13.50.99.201:8000/profile/')

@dp.message_handler(commands=['start'])
async def handle_start_command(message: types.Message):
    await handle_start(message)

@dp.message_handler(commands=['change'])
async def handle_change_command(message: types.Message):
    await handle_change(message)

@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def handle_text_message(message: types.Message):
    await handle_code(message)

async def main():
    await dp.start_polling()


