from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.i18n import gettext as _

from handlers.users.calc import rates


class GeoCallbackData(CallbackData, prefix='geo'):
    geo: str


class GeoPaginatorCallbackData(CallbackData, prefix='geo_pag'):
    action: str
    page: int


class TransporTypeCallbackData(CallbackData, prefix='ttype'):
    ttype: str


class CategoryCallbackData(CallbackData, prefix='category'):
    category_num: int


class WeightCallbackData(CallbackData, prefix='weight'):
    weight: int


class ItemPriceCallbackData(CallbackData, prefix='item_price'):
    price: int


class ItemPaginatorCallbackData(CallbackData, prefix='item_pag'):
    action: str
    page: int


def geo_paginator(max_page: int, page: int = 0):
    builder = InlineKeyboardBuilder()
    for x in rates.good[page]:
        builder.add(InlineKeyboardButton(
            text=x,
            callback_data=GeoCallbackData(geo=x).pack()))
    buttons = [
        InlineKeyboardButton(
            text='<',
            callback_data=GeoPaginatorCallbackData(action='prev' ,page=page).pack()),
        InlineKeyboardButton(
            text=f'{page + 1}/{max_page}', 
            callback_data=' '),
        InlineKeyboardButton(
            text='>',
            callback_data=GeoPaginatorCallbackData(action='next', page=page).pack())
    ]
    builder.adjust(3)
    builder.row(*buttons, width=3)
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


def inline_transport_type_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=_('Наземным транспортом'),
            callback_data=TransporTypeCallbackData(ttype='combined').pack())
    )
    builder.add(
        InlineKeyboardButton(
            text=_('Воздушным транспортом'),
            callback_data=TransporTypeCallbackData(ttype='air').pack())
    )
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


def inline_category_kb():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text=rates.most_category.category_name,
            callback_data=CategoryCallbackData(category_num=rates.most_category.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.book.category_name,
            callback_data=CategoryCallbackData(category_num=rates.book.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.coins_and_papers.category_name,
            callback_data=CategoryCallbackData(category_num=rates.coins_and_papers.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.clothing.category_name,
            callback_data=CategoryCallbackData(category_num=rates.clothing.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.jewerly_and_watches.category_name,
            callback_data=CategoryCallbackData(category_num=rates.jewerly_and_watches.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.jewerly_and_watches_and_parts.category_name,
            callback_data=CategoryCallbackData(category_num=rates.jewerly_and_watches_and_parts.category_number).pack())
        ),
    builder.add(InlineKeyboardButton(
            text=rates.nft.category_name,
            callback_data=CategoryCallbackData(category_num=rates.nft.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.buisness_and_industry.category_name,
            callback_data=CategoryCallbackData(category_num=rates.buisness_and_industry.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.musical_gear.category_name,
            callback_data=CategoryCallbackData(category_num=rates.musical_gear.category_number).pack())
        ),
    builder.add(
        InlineKeyboardButton(
            text=rates.other_category.category_name,
            callback_data=CategoryCallbackData(category_num=rates.other_category.category_number).pack())
        )
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


def inline_weight_kb():
    builder = InlineKeyboardBuilder()
    for x in range(2, 20+1):
        builder.add(
            InlineKeyboardButton(
                text=str(x),
                callback_data=WeightCallbackData(weight=x).pack())
        )
    builder.adjust(5)
    builder.row(InlineKeyboardButton(text=_('Главное меню'), callback_data='main_menu'))
    return builder.as_markup()


def item_price_paginator(max_page: int, page: int = 0):
    builder = InlineKeyboardBuilder()
    for x in rates.item_prices[page]:
        builder.add(InlineKeyboardButton(
            text=str(x),
            callback_data=ItemPriceCallbackData(price=x).pack()))
    buttons = [
        InlineKeyboardButton(
            text='<',
            callback_data=ItemPaginatorCallbackData(action='prev', page=page).pack()),
        InlineKeyboardButton(
            text=f'{page + 1}/{max_page}', 
            callback_data=' '),
        InlineKeyboardButton(
            text='>',
            callback_data=ItemPaginatorCallbackData(action='next', page=page).pack())
    ]
    builder.adjust(3)
    builder.row(*buttons, width=5)
    return builder.as_markup()