from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _

from keyboards.inline.lang import chose_lang_keyboard
from keyboards.inline.menu import back_to_menu
from db.users_manager import update_user_language


router = Router()


@router.callback_query(F.data == 'lang_callback')
async def get_lang_callback_handler(callback: CallbackQuery):
    await callback.message.edit_text(
        text=_('Выберите язык интерфейса'),
        reply_markup=chose_lang_keyboard()
    )


@router.callback_query(F.data == 'kk_lang_callbackdata')
async def change_user_language_kk(callback: CallbackQuery):
    await update_user_language(userid=callback.from_user.id, language='kk')
    await callback.message.edit_text(
        text=_('Интерфейс тілі қазақ тіліне жаңартылды'),
        reply_markup=back_to_menu()
    )


@router.callback_query(F.data == 'ru_lang_callbackdata')
async def change_user_language_kk(callback: CallbackQuery):
    await update_user_language(userid=callback.from_user.id, language='ru')
    await callback.message.edit_text(
        text=_('Язык интерфейса обновлен на русский'),
        reply_markup=back_to_menu()
    )
