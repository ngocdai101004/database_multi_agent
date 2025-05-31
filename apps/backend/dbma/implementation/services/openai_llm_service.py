import os
from typing import Any, Dict, List, Optional

from dbma.interface.services.llm_service import ILLMService
from dotenv import load_dotenv
from langchain.schema import HumanMessage, SystemMessage
from langchain_community.callbacks.manager import get_openai_callback
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langchain_openai import ChatOpenAI

load_dotenv()

class OpenAILLMService(ILLMService):
    """OpenAI implementation of the LLM service using LangChain."""
    
    def __init__(self, api_key: str = None, model: str = "gpt-4o-mini"):
        """Initialize the OpenAI LLM service.
        
        Args:
            api_key: OpenAI API key
            model: Model name to use (default: gpt-4)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,
            temperature=0.3
        )
        self._usage_metrics = {
            'total_tokens': 0,
            'total_cost': 0
        }
   
    async def ainvoke(self, messages: List[BaseMessage]) -> BaseMessage:
        with get_openai_callback() as cb:
            response = await self.llm.ainvoke(messages)
            self._update_usage_metrics(cb)
            return response
    def _update_usage_metrics(self, cb: get_openai_callback):
        self._usage_metrics['total_tokens'] += cb.total_tokens
        self._usage_metrics['total_cost'] += cb.total_cost
        
    def get_usage_metrics(self) -> Dict[str, Any]:
        return self._usage_metrics