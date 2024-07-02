from aiogram import Router, F, types
from keyboards.inline.menu import back_to_menu
from aiogram.utils.i18n import gettext as _

router = Router()


@router.callback_query(F.data == 'about_us_callback')
async def get_lang_callback_handler(call: types.CallbackQuery):
    template = [
        _('О нас\n'),
        _('Наш бот создан для того, чтобы помочь вам зарабатывать деньги на Ebay.\n'),
        _('С помощью EBAY_KZ_BOT вы сможете экономить время на поиске нишевых товаров и калькуляции доставки.'),
        _('Наши клиенты вышли на новый уровень заработка при помощи нашего бота.\n'),
        _('Основные функции нашего бота:\n'),
        _(' - "Топ ниши" 📊: Узнайте, какие товары наиболее популярны на Ebay прямо сейчас.\n'),
        _(' - Калькулятор стоимости товаров на Ebay, включая сборы и доставку из Казахстана 🇰🇿 в другие страны 🌎.\n'),
        _(' - Наш калькулятор доставки рассчитан исключительно на Казпочту.'),
    ]
    await call.message.edit_text(
        text='\n'.join(template),
        reply_markup=back_to_menu()
    )
