from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils.i18n import gettext as _

router = Router()


@router.message(Command('cancel'))
async def cancel_handler(msg: types.Message, state: FSMContext):
    st = await state.get_state()
    if st is not None:
        await msg.answer(text=_('Операция отменена, для вызвать меню - /menu'))
        await state.clear()
    else:
        await msg.answer(text=_('Нечего отменять, для вызова меню - /menu'))