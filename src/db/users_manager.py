import aiosqlite

from datetime import datetime

from core.const import USERS_DB, DATA_DB


async def init_users_tables():
    async with aiosqlite.connect(USERS_DB) as conn:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            registration_data DATETIME DEFAULT (DATETIME(CURRENT_TIMESTAMP, 'LOCALTIME')),
            userid INTEGER NOT NULL,
            username TEXT NOT NULL DEFAULT '-',
            firstname TEXT NOT NULL DEFAULT '-',
            lastname TEXT NOT NULL DEFAULT '-',
            language TEXT NOT NULL DEFAULT 'ru',
            subscription INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        await conn.commit()


async def register_on_start(userid: int, username: str = None, firstname: str = None, lastname: str = None, language: str = None):
    async with aiosqlite.connect(USERS_DB) as conn:
        cursor = await conn.cursor()

        # Check if user in the database do nothing
        await cursor.execute("SELECT userid FROM Users WHERE userid = ?", (userid,))
        result = await cursor.fetchone()
        if result is not None and result[0] is not None:
            return

        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        u_name = username if username else '-'
        f_name = firstname if firstname else '-'
        l_name = lastname if lastname else '-'
        lang = language if language else 'ru'

        await cursor.execute(
            """
            INSERT INTO Users (registration_data, userid, username, firstname, lastname, language, subscription)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (formatted_time, userid, u_name, f_name, l_name, lang, 0)
        )
        await conn.commit()


async def get_user_language(userid: int):
    async with aiosqlite.connect(USERS_DB) as conn:
        async with conn.execute("SELECT language FROM Users WHERE userid = ?", (userid,)) as cursor:
            result = await cursor.fetchone()
            return result[0] if result is not None and result[0] else 'ru'


async def update_user_language(userid: int, language: str):
    async with aiosqlite.connect(USERS_DB) as conn:
        await conn.execute("UPDATE Users SET language = ? WHERE userid = ?", (language, userid))
        await conn.commit()


async def check_subscription(userid: int):
    async with aiosqlite.connect(USERS_DB) as conn:
        async with conn.execute("SELECT subscription FROM Users WHERE userid = ?", (userid,)) as cursor:
            result = await cursor.fetchone()
            return result[0]


async def update_user_subscription(userid: int, value: int):
    async with aiosqlite.connect(USERS_DB) as conn:
        await conn.execute("UPDATE Users SET subscription = ? WHERE userid = ?", (value, userid))
        await conn.commit()



async def get_all_users():
    async with aiosqlite.connect(USERS_DB) as conn:
        async with conn.execute("SELECT * FROM Users ORDER BY registration_data DESC") as cursor:
            result = await cursor.fetchall()
            return result


async def get_data_from_db():
    async with aiosqlite.connect(DATA_DB) as conn:
        async with conn.execute("SELECT * FROM Data GROUP BY title ORDER BY watch_count DESC") as cursor:
            result = await cursor.fetchall()
            return result
