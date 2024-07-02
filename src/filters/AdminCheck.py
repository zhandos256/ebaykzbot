from aiogram import types
from aiogram.filters import BaseFilter

admins = (6453546962,)

class IsAdmin(BaseFilter):
    async def __call__(self, msg: types.Message):
        return True if msg.from_user.id in admins else False
        