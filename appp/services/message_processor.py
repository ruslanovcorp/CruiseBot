from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.services.faq_service import FAQService
from app.services.nlp_service import NLPService
from app.utils.logger import logger
from app.config import settings

class MessageProcessor:
    """Main message processing service"""
    
    def __init__(self, db: Session):
        self.db = db
        self.faq_service = FAQService(db)
        self.nlp = NLPService()
    
    def process_message(self, message: str, platform: str, user_id: str) -> str:
        """Process incoming message and generate response"""
        try:
            logger.info(f"Processing {platform} message from {user_id}: {message[:50]}...")
            
            # Extract intent and entities
            intent, confidence = self.nlp.extract_intent(message)
            entities = self.nlp.extract_entities(message)
            
            # Try to find FAQ match
            faq_match = self.faq_service.find_best_match(message)
            
            if faq_match:
                response = faq_match.answer
            else:
                # Get fallback response based on intent
                response = self.faq_service.get_fallback_response(intent)
            
            # Add context if available
            if entities:
                response = self._enhance_response_with_entities(response, entities)
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return "Извините, произошла техническая ошибка. Наш специалист свяжется с вами в ближайшее время."
    
    def _enhance_response_with_entities(self, response: str, entities: Dict) -> str:
        """Enhance response with extracted entities"""
        if 'dates' in entities:
            response += f"\n\nВы упомянули дату: {entities['dates'][0]}"
        
        if 'location' in entities:
            response += f"\n\nОтличный выбор! {entities['location'].title()} - прекрасное направление."
        
        return response