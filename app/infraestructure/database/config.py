#config.py is for asyncronus conection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.infraestructure.database.models import Base
DATABASE_URL = "sqlite+aiosqlite:///./whatsapp_api.db"

engine = create_async_engine(DATABASE_URL, echo=True)#echo=True show queryes on console

SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


#create the database
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def get_db():
    async with SessionLocal() as session:
        yield session
        