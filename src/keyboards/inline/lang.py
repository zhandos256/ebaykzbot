from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _


def chose_lang_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Қазақша 🇰🇿', callback_data='kk_lang_callbackdata'))
    builder.add(InlineKeyboardButton(text='Русскиий 🇷🇺', callback_data='ru_lang_callbackdata'))
    builder.add(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    builder.adjust(1)
    return builder.as_markup()
