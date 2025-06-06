import os
from typing import Any, Dict, List, Optional

from dbma.interface.services.llm_service import ILLMService
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

class GeminiLLMService(ILLMService):
    """Gemini implementation of the LLM service using LangChain."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-2.0-flash"):
        """Initialize the Gemini LLM service.
        
        Args:
            api_key: Google API key (for Gemini)
            model: Model name to use (default: gemini-2.0-flash)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = model
        self.llm = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=self.api_key,
            temperature=0.3
        )
        self._usage_metrics = {
            'total_tokens': 0,
            'total_cost': 0
        }
    
    async def ainvoke(self, messages: List[BaseMessage]) -> BaseMessage:
        response = await self.llm.ainvoke(messages)
        return response
        
    def _update_usage_metrics(self, response: BaseMessage):
        pass
        
    def get_usage_metrics(self) -> Dict[str, Any]:
        return self._usage_metrics