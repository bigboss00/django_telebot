import logging
import requests

from aiogram import Bot, Dispatcher, executor, types

TOKEN = '2022904049:AAHl05mEnSLHurgt1YSw93l6d1p5byoYCzw'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

activation_code = []

@dp.message_handler(commands=['register',])
async def register(message: types.Message):
    a = requests.post('http://127.0.0.1:8000/account/register/', 
    data={
        'email': f'{message.chat.username}@gmail',
        'password': '89216754',
        'password_confirm': '89216754',
        'name': f'{message.chat.first_name}'
    })
    activation_code.append(a.text)

if __name__ == '__main__':
    executor.start_polling(dp,skip_updates=True)
    