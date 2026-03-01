from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import re

from app.models.faq import FAQ
from app.services.nlp_service import NLPService
from app.utils.logger import logger

class FAQService:
    def __init__(self, db: Session):
        self.db = db
        self.nlp = NLPService()
    
    def find_best_match(self, user_text: str) -> Optional[FAQ]:
        """Find the best matching FAQ using multiple strategies"""
        try:
            # Clean text
            clean_text = self.nlp.preprocess_text(user_text)
            
            # Strategy 1: Exact match
            faqs = self.db.query(FAQ).filter(
                FAQ.is_active == True
            ).all()
            
            # Strategy 2: Keyword matching
            best_match = None
            best_score = 0
            
            for faq in faqs:
                score = self._calculate_match_score(clean_text, faq)
                if score > best_score and score > 0.6:  # Threshold
                    best_score = score
                    best_match = faq
            
            if best_match:
                # Increment usage count
                best_match.usage_count += 1
                self.db.commit()
                logger.info(f"FAQ match found: '{best_match.question}' (score: {best_score})")
            
            return best_match
            
        except Exception as e:
            logger.error(f"Error finding FAQ match: {e}")
            return None
    
    def _calculate_match_score(self, text: str, faq: FAQ) -> float:
        """Calculate matching score between user text and FAQ"""
        score = 0.0
        
        # Check question match
        if faq.question.lower() in text:
            score += 0.8
        
        # Check keyword match
        if faq.keywords:
            keywords = [k.strip().lower() for k in faq.keywords.split(',')]
            for keyword in keywords:
                if keyword in text:
                    score += 0.3
        
        # Category bonus
        if faq.category and faq.category.lower() in text:
            score += 0.2
        
        return min(score, 1.0)  # Cap at 1.0
    
    def get_fallback_response(self, intent: str) -> str:
        """Get appropriate fallback response based on intent"""
        fallbacks = {
            'price': "Для получения точной информации о ценах, пожалуйста, укажите желаемый маршрут и даты круиза.",
            'booking': "Для бронирования, пожалуйста, укажите:\n• Желаемые даты\n• Количество человек\n• Предпочитаемый маршрут",
            'route': "Мы предлагаем круизы по следующим направлениям:\n• Средиземное море\n• Карибский бассейн\n• Азия\n• Северная Европа",
            'unknown': "Здравствуйте! Я бот-помощник круизной компании. Я могу помочь с:\n• Информацией о ценах\n• Маршрутами\n• Бронированием\n• Ответами на частые вопросы\n\nЧем я могу вам помочь?"
        }
        
        return fallbacks.get(intent, fallbacks['unknown'])