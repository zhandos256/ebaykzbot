from contextlib import suppress

from aiogram import Router, F, types
from aiogram.utils.i18n import gettext as _
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.markdown import hlink
from aiogram.enums.parse_mode import ParseMode

from db.users_manager import get_data_from_db, check_subscription
from keyboards.inline.analyzer import AnalyzerPaginate, analyzer_paginator
from keyboards.inline.menu import back_to_menu
from keyboards.inline.subscription import buy_subscription_keyboard


router = Router()


@router.callback_query(F.data == 'analyzer_callback')
async def get_lang_callback_handler(call: types.CallbackQuery):
    check = await check_subscription(call.from_user.id)
    if not check:
        bad_template = [
            _('Ваша подписка не активна. ❌\n'),
        ]
        await call.message.edit_text(
            text='\n'.join(bad_template),
            reply_markup=buy_subscription_keyboard(),
            parse_mode=ParseMode.HTML
        )
        return

    data = await get_data_from_db()

    content = [
        f'<b>{_("Имя товара")}</b>: {data[0][0]}',
        f'<b>{_("Цена")}</b>: {data[0][1]}',
        f'<b>{_("Отслеживающих")}</b>: {data[0][2]}',
        f'<b>{_("Ссылка")}</b>: <u>{hlink("Ссылка на товар", str(data[0][3]))}</u>',
    ]

    await call.message.edit_text(
        text='\n'.join(content),
        reply_markup=analyzer_paginator(page=0, max_page=len(data)),
        parse_mode=ParseMode.HTML
    )


@router.callback_query(AnalyzerPaginate.filter(F.action.in_(['prev', 'next'])))
async def analyzer_paginate_handler(call: types.CallbackQuery, callback_data: AnalyzerPaginate):
    data = await get_data_from_db()
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else (len(data) - 1)

    if callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(data) - 1) else 0
        
    content = [
        f'<b>{_("Имя товара")}</b>: {data[page][0]}',
        f'<b>{_("Цена")}</b>: {data[page][1]}',
        f'<b>{_("Отслеживающих")}</b>: {data[page][2]}',
        f'<b>{_("Ссылка")}</b>: <u>{hlink("Ссылка на товар", str(data[page][3]))}</u>',
    ]

    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            text='\n'.join(content),
            reply_markup=analyzer_paginator(page=page, max_page=len(data)),
            parse_mode=ParseMode.HTML
        )
    await call.answer()