from aiogram import Router, F, types
from aiogram.utils.i18n import gettext as _

from keyboards.inline.lang import chose_lang_keyboard
from keyboards.inline.menu import back_to_menu
from db.users_manager import update_user_language

router = Router()


@router.callback_query(F.data == 'lang_callback')
async def get_lang_callback_handler(call: types.CallbackQuery):
    await call.message.edit_text(
        text=_('Выберите язык интерфейса'),
        reply_markup=chose_lang_keyboard()
    )


@router.callback_query(F.data == 'kk_lang_callbackdata')
async def change_user_language_kk(call: types.CallbackQuery):
    await update_user_language(userid=call.from_user.id, language='kk')
    await call.message.edit_text(
        text=_('Интерфейс тілі қазақ тіліне жаңартылды'),
        reply_markup=back_to_menu()
    )


@router.callback_query(F.data == 'ru_lang_callbackdata')
async def change_user_language_kk(call: types.CallbackQuery):
    await update_user_language(userid=call.from_user.id, language='ru')
    await call.message.edit_text(
        text=_('Язык интерфейса обновлен на русский'),
        reply_markup=back_to_menu()
    )
