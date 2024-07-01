from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.i18n import gettext as _
from aiogram.utils.i18n import lazy_gettext as __
from aiogram.enums.parse_mode import ParseMode

from db.users_manager import check_subscription
from keyboards.inline.menu import back_to_menu


router = Router()


@router.callback_query(F.data == 'subscription_callback')
async def subscription(callback: CallbackQuery):
    sub = await check_subscription(userid=callback.from_user.id)
    if sub:
        good_template = [
            _('Ваша подписка активна! ✅'),
        ]
        await callback.message.edit_text(
            text='\n'.join(good_template),
            reply_markup=back_to_menu()
        )
    else:
        bad_template = [
            _('Ваша подписка не активна. ❌\n'),
            _('Стоимость безлимитной подписки - 15000 тг.'),
            _('При покупке подписки, подписка действует НАВСЕГДА!\n'),
            _('- 1) Переведите на <b>Kaspi</b> + 7 775 998 4304 - <b>15000 тг</b>\n'),
            _('- 2) Отправьте ваш чек Kaspi админу - @EBAY_KZ_BOT_SUPPORT\n'),
            _('- 3) После того как отправили ID и чек об оплате, ждите активации в течение 1-3 минут.\n'),
            _('- 4) Подписка активирована, пользуйтесь и зарабатывайте деньги 😉'),
        ]

        await callback.message.edit_text(
            text='\n'.join(bad_template),
            reply_markup=back_to_menu(),
            parse_mode=ParseMode.HTML
        )