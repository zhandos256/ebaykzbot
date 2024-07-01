import asyncio
import logging

from aiogram import Bot, Dispatcher

from core.const import TOKEN
from db.users_manager import init_users_tables
from handlers.users.calc import handler as calc_handler
from handlers.users import help, menu, echo, start, lang, analyzer, subscription, about_us
from handlers.admin import admin
from middleware.i18n import i18n_middleware
from utils import set_bot_commands
from utils.notify import notify_admins_on_shutdown, notify_admins_on_started


async def on_startup(bot: Bot):
    await init_users_tables()
    await notify_admins_on_started(bot=bot)


async def on_shutdown(bot: Bot):
    await notify_admins_on_shutdown(bot=bot)


async def configure():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        start.router,
        help.router,
        menu.router,
        lang.router,
        calc_handler.router,
        analyzer.router,
        subscription.router,
        about_us.router,
        admin.router,
        echo.router,
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware.register(i18n_middleware)

    await set_bot_commands.set_commands(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


def main():
    logging.basicConfig(level=logging.INFO)
    asyncio.run(configure())
