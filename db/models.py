from sqlalchemy import BigInteger, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///app/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str | None] = mapped_column(String)
    tg_id = mapped_column(BigInteger)
    last_seen: Mapped[str | None] = mapped_column(String)
    nlSS_acc1: Mapped[str | None] = mapped_column(String)
    nlTrojan_acc1: Mapped[str | None] = mapped_column(String)
    finSS_acc1: Mapped[str | None] = mapped_column(String)
    finTrojan_acc1: Mapped[str | None] = mapped_column(String)
    nlSS_acc2: Mapped[str | None] = mapped_column(String)
    nlTrojan_acc2: Mapped[str | None] = mapped_column(String)
    finSS_acc2: Mapped[str | None] = mapped_column(String)
    finTrojan_acc2: Mapped[str | None] = mapped_column(String)
    nlSS_acc3: Mapped[str | None] = mapped_column(String)
    nlTrojan_acc3: Mapped[str | None] = mapped_column(String)
    finSS_acc3: Mapped[str | None] = mapped_column(String)
    finTrojan_acc3: Mapped[str | None] = mapped_column(String)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
