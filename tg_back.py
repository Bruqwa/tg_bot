import logging
import string
import aiohttp
import re
import calendar
import datetime
from random import choices, shuffle
from config import TG_TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



HELP = """
Hi!

You can use these commands:

/psw - will generate a password of 10 symbols;

/info - to receive info about your acc in Telegram;

psw5 - will generate a password 5 symbols length;

You can enter the length you need but no more then 999.

/weather - weather in Antalya for now

/calendar - shows current month calendar

/help - will show you this info message.

Have a nice day!
"""


#logging.basicConfig(level=logging.INFO)

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup(resize_keyboard=True)
psw_button = KeyboardButton(text='/psw')
info_button = KeyboardButton(text='/info')
help_button = KeyboardButton(text='/help')
weather_button = KeyboardButton(text='/weather')
clndr_button = KeyboardButton(text='/calendar')
kb.add(psw_button, info_button).add(weather_button, clndr_button).add(help_button)



@dp.message_handler(commands=['psw'])
async def generate_password(message: types.Message):
    chars = string.ascii_letters + string.digits
    psw = choices(chars, k=10)
    shuffle(psw)    
    await message.answer(''.join(psw),
                         reply_markup=kb)


@dp.message_handler(commands=['info'])
async def info(message: types.Message):
    user = types.User.get_current()
    chat = types.Chat.get_current()
    await message.answer(f'USER_INFO:\n{user}\n\nCHAT_INFO:\n{chat}',
                         reply_markup=kb)


@dp.message_handler(commands=['help', 'start'])
async def help(message: types.Message):    
    await message.answer(HELP,
                         reply_markup=kb)


@dp.message_handler(commands=['weather'])
async def help(message: types.Message):
    url = 'https://weather.com/weather/today/l/Muratpa%C5%9Fa+Antalya+T%C3%BCrkiye?canonicalCityId=00b4ccb282f34924cf80a2fd7b2eb21dc98c9b2d1fe6ff7410607253460ea45b'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            html = await response.text()
            #html = json.dumps(html, indent=4)
            t = html.find('TemperatureValue')
            #print(t)
            c = html.find('wxPhrase')
            #print(c)
            temp = html[t+62:t+64]
            tempC = (int(temp) - 32) * (5/9)
            verb = html[c+55:c+100] #was c+70
            pat = r">(.*?)<"
            verb_pat = re.findall(pat, verb)
            now = datetime.datetime.now()
            
    await message.answer(f"Now in Antalya\n{int(tempC)}°C\n{verb_pat[0]}\n\nToday is {now}", reply_markup=kb)


@dp.message_handler(commands=['calendar'])
async def cal(message: types.Message):
    now = datetime.datetime.now()
    await message.answer(f'<code>{calendar.month(now.year, now.month)}</code>', reply_markup=kb, parse_mode='html')
    

@dp.message_handler()
async def echo(message: types.Message):
    if 'psw' in message.text:
        chars = string.ascii_letters + string.digits
        psw = choices(chars, k=int(message.text[3:6]))
        shuffle(psw)
        await message.reply(''.join(psw))
    else:
        await message.reply(message.text)
    print(f'{types.User.get_current()}\n{message.text}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
