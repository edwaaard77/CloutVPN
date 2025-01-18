from db.models import async_session
from db.models import User
from sqlalchemy import select


async def add_username(new_username=None):
    async with async_session() as session:
        user = User(username=new_username)
        session.add(user)
        await session.commit()


async def set_time(tg_id, last_seen_time=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.last_seen = last_seen_time
        await session.commit()
