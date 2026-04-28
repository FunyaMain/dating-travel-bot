import asyncpg
from bot.config import DATABASE_URL

pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)

    async with pool.acquire() as conn:
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT PRIMARY KEY,
            username TEXT,
            name TEXT,
            age INT,
            city TEXT,
            gender TEXT,
            looking_for TEXT,
            photo TEXT,
            free_questions INT DEFAULT 0
        )
        """)

async def user_exists(user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT id FROM users WHERE id=$1", user_id)

async def create_user(user_id: int, username: str):
    async with pool.acquire() as conn:
        await conn.execute("""
            INSERT INTO users (id, username)
            VALUES ($1, $2)
            ON CONFLICT (id) DO NOTHING
        """, user_id, username)

async def update_user(user_id: int, **kwargs):
    async with pool.acquire() as conn:
        for k, v in kwargs.items():
            await conn.execute(
                f"UPDATE users SET {k}=$1 WHERE id=$2",
                v, user_id
            )

async def get_user(user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM users WHERE id=$1", user_id)
