#this code use the session sqlalchemy that we configure on config.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.infraestructure.database.models import Client

# se encarga de la logica de acceso y manipulacion de datos para una entidad especifica
class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_wa_id(self, wa_id: str) -> Client | None:
        query = select(Client).where(Client.wa_id == wa_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    async def create_client(self, wa_id: str, name:str | None = None) -> Client:
        new_client= Client(wa_id=wa_id, name = name)
        self.session.add(new_client)
        await self.session.commit()
        return new_client
