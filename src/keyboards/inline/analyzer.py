from aiogram.utils.i18n import gettext as _
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class AnalyzerPaginate(CallbackData, prefix='anapag'):
    page: int
    action: str


def analyzer_paginator(page: int, max_page: int):
    builder = InlineKeyboardBuilder()
    buttons = [
        InlineKeyboardButton(text='<', callback_data=AnalyzerPaginate(page=page, action='prev').pack()),
        InlineKeyboardButton(text=f'{page + 1}/{max_page}', callback_data=' '),
        InlineKeyboardButton(text='>', callback_data=AnalyzerPaginate(page=page, action='next').pack()),
    ]
    builder.row(*buttons, width=3)
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()
