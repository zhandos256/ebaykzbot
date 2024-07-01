from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _


router = Router()


@router.message()
async def echo_all(message: Message, state: FSMContext):
    template = [
        _('К сожалению, я не смог распознать команду'),
        _('Воспользуйтесь командой /help'),
    ]
    if await state.get_state() is None:
        await message.answer(
            text='\n'.join(template),
            reply_markup=None
        )