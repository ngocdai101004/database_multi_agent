from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class LLMService(ABC):
    """Interface for Language Model operations."""
    
    @abstractmethod
    async def generate_text(self, prompt: str, parameters: Optional[Dict[str, Any]] = None) -> str:
        """Generate text using the language model.
        
        Args:
            prompt: Input prompt for generation
            parameters: Optional generation parameters
            
        Returns:
            Generated text
        """
        pass
    
    @abstractmethod
    async def classify_intent(self, text: str) -> Dict[str, Any]:
        """Classify the intent of input text.
        
        Args:
            text: Input text to classify
            
        Returns:
            Dict containing intent classification results
        """
        pass
    
    @abstractmethod
    async def extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from text.
        
        Args:
            text: Input text to process
            
        Returns:
            List of extracted entities
        """
        pass
    
    @abstractmethod
    async def translate_text(self, text: str, target_language: str) -> str:
        """Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code
            
        Returns:
            Translated text
        """
        pass
    
    @abstractmethod
    async def get_usage_metrics(self) -> Dict[str, Any]:
        """Get current usage metrics for the LLM service.
        
        Returns:
            Dict containing usage metrics
        """
        pass 