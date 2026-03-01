from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
import hashlib
import hmac

from app.config import settings
from app.database import get_db_dependency
from app.services.message_processor import MessageProcessor
from app.platforms.whatsapp import WhatsAppService
from app.utils.logger import logger

router = APIRouter()

@router.get("/webhook")
async def verify_webhook(request: Request):
    """Webhook verification endpoint"""
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == settings.VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return int(challenge)

    logger.warning("Webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")

@router.post("/webhook")
async def receive_webhook(request: Request, db: Session = Depends(get_db_dependency)):
    """Main webhook endpoint for receiving messages"""
    try:
        # Verify signature in production
        # await verify_signature(request)
        
        data = await request.json()
        logger.debug(f"Webhook received: {data}")
        
        processor = MessageProcessor(db)
        whatsapp = WhatsAppService()
        
        # Process WhatsApp messages
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    
                    if "messages" in value:
                        message = value["messages"][0]
                        phone = message["from"]
                        text = message["text"]["body"]
                        
                        # Process message
                        response = processor.process_message(
                            message=text,
                            platform="whatsapp",
                            user_id=phone
                        )
                        
                        # Send response
                        await whatsapp.send_message(phone, response)
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return {"status": "error", "message": str(e)}

async def verify_signature(request: Request):
    """Verify webhook signature for security"""
    signature = request.headers.get("x-hub-signature-256")
    if not signature:
        raise HTTPException(status_code=401, detail="No signature")
    
    body = await request.body()
    expected = hmac.new(
        key=settings.WHATSAPP_TOKEN.encode(),
        msg=body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if not hmac.compare_digest(f"sha256={expected}", signature):
        raise HTTPException(status_code=401, detail="Invalid signature")