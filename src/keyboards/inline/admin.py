from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class UsersPaginate(CallbackData, prefix='userspag'):
    page: int
    action: str


def users_paginator(page: int, max_page: int):
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text='<', callback_data=UsersPaginate(page=page, action='prev').pack()),
        InlineKeyboardButton(text=f'{page + 1}/{max_page}', callback_data=' '),
        InlineKeyboardButton(text='>', callback_data=UsersPaginate(page=page, action='next').pack()),
    ]
    builder.row(*buttons, width=3)
    builder.row(InlineKeyboardButton(text='Активировать подписку', callback_data=UsersPaginate(page=page, action='activate').pack()))
    builder.row(InlineKeyboardButton(text='Деактивировать подписку', callback_data=UsersPaginate(page=page, action='deactivate').pack()))
    builder.row(InlineKeyboardButton(text='Админ меню', callback_data='admin_menu_callback'))
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()
