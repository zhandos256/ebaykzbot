from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from db.users_manager import register_on_start
from keyboards.inline.menu import main_menu


router = Router()


@router.message(Command('start'))
async def bot_start(message: Message):
    await register_on_start(
        userid=message.from_user.id, 
        username=message.from_user.username, 
        firstname=message.from_user.first_name,
        lastname=message.from_user.last_name,
        language='ru'
    )
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

    await message.answer(
        text='\n'.join(template),
        reply_markup=main_menu(has_admin=1 if message.from_user.id == 6453546962 else 0),
        disable_web_page_preview=1
    )