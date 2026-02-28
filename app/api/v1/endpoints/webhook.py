#this is to comunicate to the twilio api

from fastapi import APIRouter, Depends, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.infraestructure.database.config import get_db
from app.infraestructure.repositories.client_repository import ClientRepository
from app.domain.services.message_service import MessageService
from app.domain.services.order_service import OrderService
from app.domain.services.product_service import ProductService
from app.infraestructure.repositories.order_repository import OrderRepository
from app.infraestructure.repositories.product_repository import ProductRepository
router = APIRouter()

@router.post("/twilio")
async def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    ProfileName:str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    wa_id = From.replace("whatsapp:", "")

    client_repo = ClientRepository(session=db)
    product_repo = ProductRepository(session=db)
    order_repo = OrderRepository(session=db)

    #domain services business logic
    product_service = ProductService(repository=product_repo)

    #OrderService need both repositories to validate stock and create orders
    order_service = OrderService(order_repo=order_repo, product_repo=product_repo)

    #

    message_service = MessageService(
        client_repo=client_repo,
        product_service=product_service,
        order_service=order_service
    )



    bot_response = await message_service.process_message(
        wa_id=wa_id,
        first_name=ProfileName or "user",
        last_name="", #we leave this empty for now
        text=Body
    )

    print(f"bot response for {wa_id}: {bot_response}")
    
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>{bot_response}</Message>
    </Response>
    """
    
    return Response(content=xml_response, media_type="application/xml")