from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

from keyboards.inline.menu import main_menu

router = Router()


@router.message(Command('menu'))
async def menu_msg_handler(msg: types.Message, state: FSMContext):
    st = await state.get_state()
    await state.clear() if st is not None else ...
    template = [
        _('Добро пожаловать в Telegram-бота EBAY_KZ_BOT ⭐️'),
        _('https://t.me/EBAY_KZ_BOT - ссылка на бота\n'),
        _('❤ Главная функция нашего бота - "Топовые ниши"! 📊 Узнайте, какие товары пользуются наибольшей популярностью на Ebay прямо сейчас.\n'),
        _('Кроме того, бот может рассчитать стоимость товаров на Ebay, включая сборы и доставку из Казахстана 🇰🇿 в другие страны 🌎\n'),
        _('Калькулятор доставки рассчитан только на Казпочту\n'),
        _('Бот поддерживает 2 языка:'),
        _(' - Казахский'),
        _(' - Русский\n'),
        _('Если у вас возникли вопросы, пишите мне️'), 
        _('https://t.me/EBAY_KZ_BOT_SUPPORT - админ 👤'),
    ]
    await msg.answer(
        text='\n'.join(template),
        reply_markup=main_menu(has_admin=1 if msg.from_user.id == 6453546962 else 0),
        disable_web_page_preview=1
    )


@router.callback_query(F.data == 'main_menu')
async def menu_cb_handler(call: types.CallbackQuery, state: FSMContext):
    st = await state.get_state()
    await state.clear() if st is not None else ...
    template = [
        _('Добро пожаловать в Telegram-бота EBAY_KZ_BOT ⭐️'),
        _('https://t.me/EBAY_KZ_BOT - ссылка на бота\n'),
        _('❤ Главная функция нашего бота - "Топовые ниши"! 📊 Узнайте, какие товары пользуются наибольшей популярностью на Ebay прямо сейчас.\n'),
        _('Кроме того, бот может рассчитать стоимость товаров на Ebay, включая сборы и доставку из Казахстана 🇰🇿 в другие страны 🌎\n'),
        _('Калькулятор доставки рассчитан только на Казпочту\n'),
        _('Бот поддерживает 2 языка:'),
        _(' - Казахский'),
        _(' - Русский\n'),
        _('Если у вас возникли вопросы, пишите мне️'), 
        _('https://t.me/EBAY_KZ_BOT_SUPPORT - админ 👤'),
    ]
    await call.message.edit_text(
        text='\n'.join(template),
        reply_markup=main_menu(has_admin=1 if call.from_user.id == 6453546962 else 0),
        disable_web_page_preview=1
    )
