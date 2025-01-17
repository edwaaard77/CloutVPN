from CloutVPN_bot.db.models import async_session
from CloutVPN_bot.db.models import User


async def add_username(new_username=None):
    async with async_session() as session:
        user = User(username=new_username)
        session.add(user)
        await session.commit()

