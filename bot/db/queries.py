from db.connection import pool

async def create_user(tg_id):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (telegram_id) VALUES ($1) ON CONFLICT DO NOTHING",
            tg_id
        )

async def get_user_role(tg_id):
    async with pool.acquire() as conn:
        return await conn.fetchval(
            "SELECT role FROM roles WHERE user_id=$1",
            tg_id
        )
