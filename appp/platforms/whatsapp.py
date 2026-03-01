import requests
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import settings
from app.utils.logger import logger

class WhatsAppService:
    """WhatsApp Business API service"""
    
    def __init__(self):
        self.base_url = f"https://graph.facebook.com/v19.0/{settings.PHONE_NUMBER_ID}"
        self.headers = {
            "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def send_message(self, to: str, message: str) -> bool:
        """Send WhatsApp message with retry logic"""
        try:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "text",
                "text": {"body": message}
            }
            
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.info(f"WhatsApp message sent to {to}")
                return True
            else:
                logger.error(f"WhatsApp API error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp request failed: {e}")
            raise  # Allow retry
    
    def send_template_message(self, to: str, template_name: str, components: Optional[dict] = None):
        """Send template message for business use cases"""
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {"code": "ru"}
            }
        }
        
        if components:
            data["template"]["components"] = components
        
        try:
            response = requests.post(
                f"{self.base_url}/messages",
                headers=self.headers,
                json=data,
                timeout=10
            )
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Template message error: {e}")
            return False