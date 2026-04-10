from fastapi import APIRouter, Depends
from app.domain.services.services import get_message_service
from app.domain.services.message_service import MessageService

router = APIRouter()

@router.post("/validate-client/{wa_id}")
async def validate_client(
    wa_id: str,
    first_name: str | None = None,
    last_name: str | None = None,
    service: MessageService = Depends(get_message_service)
):
    result = await service.process_message(
        wa_id, first_name, last_name, "first register"
    )

    return {"status": "ok", "bot response": result}