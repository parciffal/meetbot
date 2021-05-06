from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import *

welcome_murkup = InlineKeyboardMarkup()
b1 = InlineKeyboardButton(WEllBUTT1, callback_data='wb1')
b2 = InlineKeyboardButton(WELLBUTT2, callback_data='wb2')
b3 = InlineKeyboardButton(WELLBUTTCUSTOM, callback_data='wbc')
welcome_murkup.add(b1, b2)
welcome_murkup.add(b3)
