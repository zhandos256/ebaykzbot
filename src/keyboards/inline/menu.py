from typing import Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.i18n import gettext as _

def main_menu(has_admin: Optional[bool]):
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=_('Калькулятор Ebay'), callback_data='calc_callback'))
    builder.add(InlineKeyboardButton(text=_('Топ ниши Ebay'), callback_data='analyzer_callback'))
    builder.add(InlineKeyboardButton(text=_('Подписка'), callback_data='subscription_callback'))
    builder.add(InlineKeyboardButton(text=_('Язык'), callback_data='lang_callback'))
    builder.add(InlineKeyboardButton(text=_('О боте'), callback_data='about_us_callback'))
    if has_admin:
        builder.add(InlineKeyboardButton(text='Панель администратора', callback_data='admin_menu_callback'))
    builder.adjust(1)
    return builder.as_markup()


def back_to_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


def calc_again():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=_('Расчитать заново'), callback_data='calc_callback'))
    builder.add(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


# ADMIN 
def admin_main_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text='Показать всех пользователей', callback_data='show_users_callback'))
    builder.adjust(1)
    return builder.as_markup()

