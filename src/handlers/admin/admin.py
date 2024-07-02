import logging
import asyncio
import aiosqlite

from datetime import datetime
from contextlib import suppress

from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.enums.parse_mode import ParseMode
from aiogram.exceptions import TelegramBadRequest

from core.const import USERS_DB
from db.users_manager import get_all_users, update_user_subscription
from filters.AdminCheck import IsAdmin
from keyboards.inline.admin import users_paginator, UsersPaginate
from keyboards.inline.menu import admin_main_menu
from utils.notify import notify_user, notify_all_users

class A(StatesGroup):
    id = State()


router = Router()


@router.message(Command('update'))
async def date_updated(msg: types.Message):
    async with aiosqlite.connect(USERS_DB) as conn:
        async with conn.execute('SELECT userid FROM Users WHERE subscription = 1') as res:
            result = await res.fetchall()
            users = [user[0] for user in result]
            await notify_all_users(bot=msg.bot, users=users, text='Данные в базе обновлены, новые товары загружены.')
    await msg.answer(text='DONE')


@router.message(IsAdmin(), Command('acti'))
async def acti(msg: types.Message, state: FSMContext):
    await msg.answer(text='Get ID')
    await state.set_state(A.id)


@router.message(A.id, F.text.isdigit())
async def acti_st(msg: types.Message, state: FSMContext):
    async with aiosqlite.connect(USERS_DB) as conn:
        await conn.execute("UPDATE Users SET subscription = ? WHERE userid = ?", (1, int(msg.text)))
        await conn.commit()
    today = datetime.now()
    now = today.now()
    template_text_for_user = [
        'Спасибо за покупку!',
        f'Ваша подписка успешно активирована ✅',
        f'Дата активации: {now}',
        'С наилучшими пожеланиями, команда EBAY_KZ_BOT ⭐️'
    ]
    try:
        await msg.bot.send_message(chat_id=int(msg.text), text='\n'.join(template_text_for_user))
    except Exception as e:
        logging.exception(e)
    await msg.answer('DONE !')
    await state.clear()


@router.message(IsAdmin(), Command('send_promo'))
async def send_users_message_without_sub(msg: types.Message):
    template = [
    '🔥 Керемет мүмкіндік! 🔥',
    'Тек <b>бүгін соңғы күн</b>! Шексіз жазылым бар болғаны <b>2000 тг</b>, бұрынғы <s>15000 тг</s> орнына! 🎉',
    'Мүмкіндікті жіберіп алмаңыз және барлық артықшылықтарға ие болыңыз! 🌟',
    '⏰ Жеңілдік аяқталуына 6 сағат қалды! Қапы қалмаңыз! ⏰\n',
    '- - - - - - - - -\n',
    '🔥 Воспользуйтесь невероятной скидкой! 🔥',
    'Только <b>сегодня последний день</b>! Безлимитная подписка всего за <b>2000 тг</b> вместо <s>15000 тг</s>! 🎉',
    'Не упустите шанс сэкономить и получать все преимущества! 🌟',
    '⏰ Осталось 6 часов до завершения скидки! Поторопитесь! ⏰',
    ]
    async with aiosqlite.connect(USERS_DB) as conn:
        u = []
        async with conn.execute("SELECT userid FROM Users WHERE subscription = 0") as result:
            res = await result.fetchall()
            for j in res:
                u.append(j[0])
        for user in u:
            try:
                with suppress(TelegramBadRequest):
                    await msg.bot.send_message(
                        chat_id=user,
                        # chat_id=727014481,
                        text='\n'.join(template),
                        parse_mode=ParseMode.HTML
                    )
                    await asyncio.sleep(.05)
            except Exception:
                continue


@router.message(IsAdmin(), Command('admin'))
async def admin_panel(msg: types.Message):
    tempate = [
        'Administrator super panel ⚙️',
    ]
    await msg.answer(
        text='\n'.join(tempate),
        reply_markup=admin_main_menu()
    )


@router.callback_query(IsAdmin(), F.data == 'admin_menu_callback')
async def admin_menu_cb_handler(cb: types.CallbackQuery):
    tempate = [
        'Панель администратора ⚙️',
    ]
    await cb.message.edit_text(
        text='\n'.join(tempate),
        reply_markup=admin_main_menu()
    )


@router.callback_query(IsAdmin(), F.data == 'show_users_callback')
async def show_users(cb: types.CallbackQuery):
    users = await get_all_users()

    content = [
        f'<b>ID</b>: {users[0][0]}',
        f'<b>Дата регистрации</b>: {users[0][1]}',
        f'<b>ID пользователя</b>: {users[0][2]}',
        f'<b>Имя пользователя</b>: {users[0][3]}',
        f'<b>Имя</b>: {users[0][4]}',
        f'<b>Фамилия</b>: {users[0][5]}',
        f'<b>Язык</b>: {users[0][6]}',
        f'<b>Подписка</b>: {"👍🏻" if users[0][7] else "👎🏿"}',
    ]

    with suppress(TelegramBadRequest):
        await cb.message.edit_text(
            text='\n'.join(content),
            reply_markup=users_paginator(page=0, max_page=len(users)),
            parse_mode=ParseMode.HTML
        )
    await cb.answer()


@router.callback_query(IsAdmin(), UsersPaginate.filter(F.action.in_(['prev', 'next', 'activate', 'deactivate', 'ban_user'])))
async def show_users_paginate_handler(cb: types.CallbackQuery, callback_data: UsersPaginate):
    users = await get_all_users()
    page_num = int(callback_data.page)
    page = page_num
    today = datetime.now()
    now = today.now()

    if callback_data.action == 'prev':
        page = page_num - 1 if page_num > 0 else (len(users) - 1)
    elif callback_data.action == 'next':
        page = page_num + 1 if page_num < (len(users) - 1) else 0
    elif callback_data.action == 'activate':
        if users[page][7] == 1:
            await cb.answer(text=f'Подписка пользователя {users[page][3]} {users[page][4]} уже активна ❕')
        else:
            template_text_for_user = [
                'Спасибо за покупку!',
                f'Ваша подписка успешно активирована ✅',
                f'Дата активации: {now}',
                'С наилучшими пожеланиями, команда EBAY_KZ_BOT ⭐️'
            ]
            await update_user_subscription(value=1, userid=users[page][2]) # activate users subscription
            await cb.answer(text=f'Подписка пользователя {users[page][3]} {users[page][4]} успешно активирована ✅')
            await notify_user(bot=cb.bot, chat_id=users[page][2], text='\n'.join(template_text_for_user)) # notify user
    elif callback_data.action == 'deactivate':
        if users[page][7] == 0:
            await cb.answer(text=f'Подписка пользователя {users[page][3]} {users[page][4]} уже деактивирована ❕')
        else:
            template_text_for_user = [
                'Ваша подписка деактивирована админом ❌',
                f'Дата деактивации: {now}',
                'Если у вас есть вопросы, свяжитесь с админом @EBAY_KZ_BOT_SUPPORT',
            ]
            await update_user_subscription(value=0, userid=users[page][2]) # deactivate users subscription
            await cb.answer(text=f'Подписка пользователя {users[page][3]} {users[page][4]} успешно деактивирована ❌')
            await notify_user(bot=cb.bot, chat_id=users[page][2], text='\n'.join(template_text_for_user)) # notify user
    
    users = await get_all_users()
    
    content = [
        f'<b>ID</b>: {users[page][0]}',
        f'<b>Дата регистрации</b>: {users[page][1]}',
        f'<b>ID пользователя</b>: {users[page][2]}',
        f'<b>Имя пользователя</b>: {users[page][3]}',
        f'<b>Имя</b>: {users[page][4]}',
        f'<b>Фамилия</b>: {users[page][5]}',
        f'<b>Язык</b>: {users[page][6]}',
        f'<b>Подписка</b>: {"👍🏻" if users[page][7] else "👎🏿"}',
    ]

    with suppress(TelegramBadRequest):
        await cb.message.edit_text(
            text='\n'.join(content),
            reply_markup=users_paginator(page=page, max_page=len(users)),
            parse_mode=ParseMode.HTML
        )
    await cb.answer()