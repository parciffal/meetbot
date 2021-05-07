from time import sleep

from aiogram import Bot, Dispatcher, executor
from aiogram import types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from stages.stage import User
from keyboards.inline.inline_murkup import welcome_murkup
from config import *
import logging
from datetime import date
from whitelist.database import DataConnector

today = date.today()
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)
user_info = {'username': '',
             'user_id': '',
             'quantity': '',
             'price': '',
             'date': '',
             'latitude': '',
             'longitude': ''}
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )


@dp.callback_query_handler(lambda call: call.data in ['accept', 'addnew'])
async def call_accept(call: types.CallbackQuery):
    try:
        if call.data == 'accept':
            markup = types.InlineKeyboardMarkup()
            b1 = types.InlineKeyboardButton('Add new order', callback_data='addnew')
            markup.add(b1)
            await bot.send_message(int(user_info['user_id']), ACCEPTION_MESSAGE_FROM_GROUP, reply_markup=markup)
            await bot.send_message(call.message.chat.id, user_info['username']+' order Accepted')
        elif call.data == 'addnew':
            markup = welcome_murkup
            await call.message.answer(REPIT_MESSAGE, reply_markup=markup)
            user_info['username'] = user_info['username']
            user_info['user_id'] = user_info['user_id']
            await User.S1.set()
    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: call.data in ['confirm', 'repit'],state=User.S5)
async def call_confirm(call: types.CallbackQuery):
    try:
        if call.data == 'confirm':
            d2 = today.strftime("%B, %Y")
            await bot.send_message(call.message.chat.id, CONFIRMMESSAGE_ALERT)
            markup = types.InlineKeyboardMarkup()
            b = types.InlineKeyboardButton(ACCEPTBUTTONTEXT, callback_data='accept')
            markup.add(b)
            await bot.send_message(GROUP_ID, GROUP_SEND_MESSAGE.format(username=user_info['username'],
                                                                       quantity=user_info['quantity'],
                                                                       price=user_info['price'],
                                                                       date=user_info['date'],
                                                                       todey=d2,
                                                                       latitude=user_info['latitude'],
                                                                       longitude=user_info['longitude']),
                                                                       reply_markup=markup)
            await dp.storage.close()
        elif call.data == 'repit':
            markup = welcome_murkup
            await call.message.answer(REPIT_MESSAGE, reply_markup=markup)
            user_info['username'] = user_info['username']
            user_info['user_id'] = user_info['user_id']
            await User.S1.set()
    except Exception as e:
        print(repr(e))


@dp.callback_query_handler(lambda call: call.data in ['wb1', 'wb2', 'wbc'], state=User.S1)
async def wellcome_murkup_callback(call: types.CallbackQuery):
    try:
        if call.data == 'wb1':
            user_info['quantity'] = 1
            user_info['price'] = X
            await call.message.answer(LOCATION_MESSAGE_TEXT)
            await User.S3.set()
        elif call.data == 'wb2':
            user_info['quantity'] = 2
            user_info['price'] = 2*X
            await call.message.answer(LOCATION_MESSAGE_TEXT)
            await User.S3.set()
        elif call.data == 'wbc':
            await call.message.answer('Send quantity from 1.5 to 10\nit shell be ration number or number with.5')
            await User.next()
    except Exception as e:
        print(repr(e))


@dp.message_handler(state=User.S2)
async def quantity_step(message: types.Message):
    try:
        i = 1.5
        bool_cheak = False
        while i < 11:
            if message.text == str(i):
                bool_cheak = True
            i = i + 0.5
        if bool_cheak:
            user_info['quantity'] = message.text
            user_info['price'] = float(message.text) * X
            await message.answer(LOCATION_MESSAGE_TEXT)
            await User.S3.set()
        else:
            await message.answer(QUANTITY_ERROR)
            await User.S2.set()
    except Exception as e:
        print(repr(e))


@dp.message_handler(content_types=types.ContentType.LOCATION, state=User.S3)
async def location_step(location: types.Location):
    try:
        user_info['latitude'] = location['location']['latitude']
        user_info['longitude'] = location['location']['longitude']
        d2 = today.strftime("%B %d, %Y")
        await bot.send_message(location['chat']['id'], DATE_ERROR_LOC_STEP.format(date = d2))
        await User.next()
    except Exception as e:
        print(repr(e))


@dp.message_handler(state=User.S4)
async def date_step(message: types.Message):
    try:
        split_date = message.text.split(' ')
        spl_date_day = split_date[0].split('.')
        cloak = split_date[1]
        split_cloak = cloak.split(':')
        if 0 <= int(split_cloak[0]) <= 24 and int(today.day) <= int(spl_date_day[0]) < 32:
            if 0 <= float(split_cloak[1]) <= 60:
                user_info['date'] = message.text
                markup = types.InlineKeyboardMarkup()
                b1 = types.InlineKeyboardButton(CONFIRMBUTT, callback_data='confirm')
                b2 = types.InlineKeyboardButton(REPITBUTT, callback_data='repit')
                markup.add(b1)
                markup.add(b2)
                d2 = today.strftime("%B, %Y")
                await bot.send_message(message.chat.id, CONFIRMMESSAGE_TEXT.format(quantity=user_info['quantity'],
                                                                                   price=user_info['price'],
                                                                                   date=user_info['date'],
                                                                                   todey=d2,
                                                                                   latitude=user_info['latitude'],
                                                                                   longitude=user_info['longitude']),
                                       reply_markup=markup)
                await User.next()
                print(user_info)
            else:
                await bot.send_message(message.chat.id, DATE_ERROR_WRONG)
                await User.S4.set()
        else:
            await bot.send_message(message.chat.id, DATE_ERROR_WRONG)
            await User.S4.set()
    except Exception as e:
        print(repr(e))


@dp.message_handler(commands='start')
async def start_message(message: types.Message):
    try:
        if message.chat.id > 0:
            db = DataConnector()
            cheak_bool = False
            for i in db.get_all_ids():
                if int(message.from_user.id) == int(i):
                    cheak_bool = True
            if cheak_bool:
                markup = welcome_murkup
                await message.answer(WELCOME_MESSAGE, reply_markup=markup)
                user_info['username'] = message.from_user.username
                user_info['user_id'] = message.from_user.id
                await User.S1.set()
            else:
                await message.answer(WELCOME_ERROR_WHITELIST)
        else:
            await message.answer(WELCOME_ERROR_GROUPCHAT)
    except Exception as e:
        print(repr(e))

if __name__ == '__main__':
    while True:
        try:
            executor.start_polling(dp)
        except Exception as e:
            print(repr(e))
            sleep(10)