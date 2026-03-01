import re
import string
from typing import List, Tuple, Optional
import Levenshtein
from app.utils.logger import logger

class NLPService:
    """Natural Language Processing service for message understanding"""
    
    def __init__(self):
        # Cruise-related keywords
        self.cruise_keywords = {
            'price': ['цена', 'стоимость', 'сколько', 'стоит', 'price', 'cost'],
            'booking': ['забронировать', 'бронь', 'booking', 'book', 'reserve'],
            'route': ['маршрут', 'направление', 'куда', 'route', 'destination'],
            'date': ['дата', 'когда', 'date', 'when'],
            'duration': ['длительность', 'сколько дней', 'duration'],
            'cabin': ['каюта', 'номер', 'cabin', 'room'],
            'food': ['еда', 'питание', 'ресторан', 'food', 'restaurant'],
            'children': ['дети', 'ребенок', 'children', 'kids'],
            'discount': ['скидка', 'акция', 'discount', 'sale'],
        }
        
    def preprocess_text(self, text: str) -> str:
        """Clean and normalize text"""
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ' '.join(text.split())
        return text
    
    def extract_intent(self, text: str) -> Tuple[str, float]:
        """Extract user intent from message"""
        text = self.preprocess_text(text)
        intent_scores = {}
        
        for intent, keywords in self.cruise_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text:
                    score += 1
                # Check for similar words using Levenshtein distance
                for word in text.split():
                    if len(word) > 3 and Levenshtein.ratio(word, keyword) > 0.8:
                        score += 0.5
            intent_scores[intent] = score
        
        if not intent_scores:
            return "unknown", 0.0
        
        best_intent = max(intent_scores, key=intent_scores.get)
        return best_intent, intent_scores[best_intent]
    
    def extract_entities(self, text: str) -> dict:
        """Extract entities like dates, numbers, locations"""
        entities = {}
        
        # Extract dates (simplified)
        date_patterns = [
            r'\d{1,2}[./-]\d{1,2}[./-]\d{2,4}',  # DD/MM/YYYY
            r'\d{1,2}\s+(января|февраля|марта|апреля|мая|июня|июля|августа|сентября|октября|ноября|декабря)',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                entities['dates'] = matches
        
        # Extract numbers (people count, duration)
        numbers = re.findall(r'\d+', text)
        if numbers:
            entities['numbers'] = numbers
        
        # Extract locations
        locations = ['средиземное море', 'карибы', 'азия', 'европа']
        for loc in locations:
            if loc in text.lower():
                entities['location'] = loc
        
        return entities