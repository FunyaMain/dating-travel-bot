from db.queries import get_user_role
from config import ADMIN_IDS

async def is_admin(user_id):
    return user_id in ADMIN_IDS

async def is_moderator(user_id):
    role = await get_user_role(user_id)
    return role == "moderator"
