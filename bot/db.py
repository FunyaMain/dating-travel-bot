import aiosqlite
from bot.config import DB_PATH

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            name TEXT,
            age INTEGER,
            city TEXT,
            gender TEXT,
            looking_for TEXT,
            photo TEXT,
            free_questions INTEGER DEFAULT 0
        )
        """)
        await db.commit()

async def get_user(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE id=?", (user_id,)) as cur:
            return await cur.fetchone()

async def user_exists(user_id):
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT 1 FROM users WHERE id=?", (user_id,)) as cur:
            return await cur.fetchone()

async def create_user(user_id, username):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (id, username) VALUES (?, ?)",
            (user_id, username)
        )
        await db.commit()

async def update_user(user_id, **kwargs):
    async with aiosqlite.connect(DB_PATH) as db:
        for k, v in kwargs.items():
            await db.execute(f"UPDATE users SET {k}=? WHERE id=?", (v, user_id))
        await db.commit()
