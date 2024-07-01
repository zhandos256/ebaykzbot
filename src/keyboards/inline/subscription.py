from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def buy_subscription_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=_('Купить подписку'), callback_data='subscription_callback'))
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    builder.adjust(1)
    return builder.as_markup()
