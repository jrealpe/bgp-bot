import logging
import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor

from tabulate import tabulate

API_TOKEN = 'YOUR_API_KEY'


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def bgp_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm BGPBot!\nPowered by Julio Realpe.")


@dp.message_handler(filters.RegexpCommandsFilter(regexp_commands=['ip ((?:\d{1,3}\.){3}\d{1,3})']))
async def bgp_list(message: types.Message, regexp_command):
    msg = f'You have requested an bgp of ip: {regexp_command.group(1)}\n\n'

    r = requests.get(f'http://127.0.0.1:5000/bgp/?ip={regexp_command.group(1)}')
    r = r.json()

    _header = ['IP', 'Network', 'Next Hop', 'Path (AS)', 'Origin']
    _table = []
    for i in r:
        _table.append([i['ip'], i['network'], i['next_hop'], i['path'], i['origin']])

    msg += str(tabulate(_table, headers=_header))
    await message.reply(msg)


@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)

    await message.reply('No entiendo :c')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
