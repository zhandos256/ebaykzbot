from aiogram import Bot
import logging
import asyncio

admins = (6453546962,)


async def notify_admins(bot: Bot, text: str):
    for admin in admins:
        await bot.send_message(chat_id=admin, text=text)


async def notify_admins_on_started(bot: Bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот EBAY_KZ_BOT запущен!')


async def notify_admins_on_shutdown(bot: Bot):
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Работа бота EBAY_KZ_BOT завершена!')
    await bot.session.close()


async def notify_user(bot: Bot, chat_id: int, text: str):
    await bot.send_message(
        chat_id=chat_id,
        text=text
    )


async def notify_all_users(bot: Bot, users: list[int], text: str):
    for user in users:
        try:
            await bot.send_message(
                chat_id=user,
                text=text
            )
            await asyncio.sleep(.05)
        except Exception as e:
            logging.info(e)
