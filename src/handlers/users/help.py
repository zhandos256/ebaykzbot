from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message(Command('help'))
async def bot_help(message: Message):
    template = [
        _('Список всех комманд\n'),
        _('/start - Приветственное сообзение'),
        _('/help - Показать это сообщение помощи\n'),
        _('Если у вас есть вопросы, обращайтесь\n'),
        _('Телеграм: @EBAY_KZ_BOT_SUPPORT'),
    ]
    await message.answer(
        text='\n'.join(template),
        reply_markup=None
    )