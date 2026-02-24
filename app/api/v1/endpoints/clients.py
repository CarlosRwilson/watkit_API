from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository
from app.domain.services.message_service import MessageService

router = APIRouter()

@router.post("/validate-client/{wa_id}")
async def validate_client(wa_id:str, first_name:str | None = None,
                          last_name:str| None = None, db:AsyncSession= Depends(get_db)):
    
    repo = ClientRepository(db)
    
    service = MessageService(repo)

    #call business logic
    result = await service.process_messsage(wa_id, first_name, last_name, "first register")

    return {"status": "ok", "bot response": result}