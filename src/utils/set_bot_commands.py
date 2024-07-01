from aiogram import Bot
from aiogram.types import BotCommand


async def set_commands(bot: Bot):
    main_menu = [
        BotCommand(
            command="/start",
            description='Приветсвтенное сообщение'
        ),
        BotCommand(
            command="/help",
            description='Получить справку'
        ),
    ]
    await bot.set_my_commands(main_menu)
