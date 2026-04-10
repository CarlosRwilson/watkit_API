from fastapi import APIRouter, Depends, Form, Response
from app.domain.services.services import get_message_service
from app.domain.services.message_service import MessageService
import html

router = APIRouter()

@router.post("/twilio")
async def twilio_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    ProfileName: str = Form(None),
    message_service: MessageService = Depends(get_message_service)
):
    # Clean the ID (Twilio sends whatsapp:+123456789)
    wa_id = From.replace("whatsapp:", "")


    # Process Logic
    bot_response = await message_service.process_message(
        wa_id=wa_id,
        first_name=ProfileName or "User",
        text=Body
    )
    #if user send >, &, etc, break XML
    safe_response = html.escape(bot_response)
    # Return TwiML (XML)
    # We use a TwiML format so Twilio knows how to send the message back to WhatsApp
    xml_response = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>{safe_response}</Message>
    </Response>"""
    
    return Response(content=xml_response, media_type="application/xml")