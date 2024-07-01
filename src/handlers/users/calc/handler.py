from contextlib import suppress

from aiogram.exceptions import TelegramBadRequest
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _
from aiogram.enums.parse_mode import ParseMode

from db.users_manager import check_subscription
from handlers.users.calc import rates
from keyboards.inline import menu 
from keyboards.inline.subscription import buy_subscription_keyboard
from keyboards.inline.menu import back_to_menu
from keyboards.inline.calc import (
    GeoCallbackData,
    GeoPaginatorCallbackData,
    TransporTypeCallbackData,
    CategoryCallbackData,
    WeightCallbackData,
    ItemPriceCallbackData,
    ItemPaginatorCallbackData,
    geo_paginator,
    inline_transport_type_kb,
    inline_category_kb,
    inline_weight_kb,
    item_price_paginator
)
from states import calc


router = Router()


@router.callback_query(F.data == 'calc_callback')
async def get_calc_cq(callback: CallbackQuery, state: FSMContext):
    check = await check_subscription(userid=callback.from_user.id)
    if not check:
        bad_template = [
            _('Ваша подписка не активна. ❌\n'),
        ]

        await callback.message.edit_text(
            text='\n'.join(bad_template),
            reply_markup=buy_subscription_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return
    await callback.message.edit_text(
        text=_('Выберите страну'),
        reply_markup=geo_paginator(max_page=len(rates.good), page=0)
    )
    await state.set_state(calc.CalcState.geo)


@router.callback_query(GeoCallbackData.filter(), calc.CalcState.geo)
async def get_geo_cq(callback: CallbackQuery, callback_data: GeoCallbackData, state: FSMContext):
    data = str(callback_data.geo)
    await state.update_data(geo=data)
    await callback.message.edit_text(
        text=_('Выберите тип транспортировки'),
        reply_markup=inline_transport_type_kb()
    )
    await state.set_state(calc.CalcState.logistic_type)


@router.callback_query(GeoPaginatorCallbackData.filter())
async def geo_paginator_handler_cq(callback: CallbackQuery, callback_data: GeoPaginatorCallbackData):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else (len(rates.good) - 1)

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(rates.good) - 1) else 0
    
    await callback.message.edit_text(
        text=_('Выберите страну'),
        reply_markup=geo_paginator(max_page=(len(rates.good)), page=page)
    )


@router.callback_query(TransporTypeCallbackData.filter(), calc.CalcState.logistic_type)
async def get_transport_type_cq(callback: CallbackQuery, callback_data: TransporTypeCallbackData, state: FSMContext):
    data = str(callback_data.ttype)
    await state.update_data(transport_type=data)
    await callback.message.edit_text(
        text=_('Выберите категорию'),
        reply_markup=inline_category_kb()
    )
    await state.set_state(calc.CalcState.category)


@router.callback_query(CategoryCallbackData.filter(), calc.CalcState.category)
async def get_category_cq(callback: CallbackQuery, callback_data: CategoryCallbackData, state: FSMContext):
    data = str(callback_data.category_num)
    await state.update_data(category_num=data)
    await callback.message.edit_text(
        text=_('Выберите вес'),
        reply_markup=inline_weight_kb()
    )
    await state.set_state(calc.CalcState.weight)


@router.callback_query(WeightCallbackData.filter(), calc.CalcState.weight)
async def get_weight_cq(callback: CallbackQuery, callback_data: WeightCallbackData, state: FSMContext):
    data = str(callback_data.weight)
    await state.update_data(weight=data)
    await callback.message.edit_text(
        text=_('Выберите стоимость товара'),
        reply_markup=item_price_paginator(max_page=len(rates.item_prices), page=0)
    )
    await state.set_state(calc.CalcState.item_price)


@router.callback_query(ItemPriceCallbackData.filter(), calc.CalcState.item_price)
async def get_item_price_cq(callback: CallbackQuery, callback_data: ItemPriceCallbackData, state: FSMContext):
    data = str(callback_data.price)
    await state.update_data(price=data)
    data_from_state = await state.get_data()
    country = data_from_state['geo']
    transport_type = data_from_state['transport_type']
    category_num = int(data_from_state['category_num'])
    item_weight = int(data_from_state['weight'])
    item_price = int(data_from_state['price'])
    res = await rates.get_data_from_finish_state(geo=country, transport_type=transport_type, category_number=category_num, item_weight=item_weight, item_price=item_price)
    await callback.message.edit_text(
        **res.as_kwargs(),
        reply_markup=menu.calc_again()
    )
    await state.clear()


@router.callback_query(ItemPaginatorCallbackData.filter())
async def item_paginator_handler_cq(callback: CallbackQuery, callback_data: ItemPaginatorCallbackData):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else (len(rates.item_prices) - 1)
    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(rates.item_prices) - 1) else 0
    with suppress(TelegramBadRequest):
        await callback.message.edit_text(
            text=_('Выберите стоимость товара'),
            reply_markup=item_price_paginator(max_page=(len(rates.item_prices)), page=page)
        )
        await callback.answer()