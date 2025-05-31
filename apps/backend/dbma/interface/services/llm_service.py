from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from langchain_core.messages import BaseMessage


class ILLMService(ABC):
    """Interface for Language Model operations."""
    
    @abstractmethod
    async def ainvoke(self, messages: List[BaseMessage]) -> BaseMessage:
        raise NotImplementedError("ainvoke method must be implemented")
    
    @abstractmethod
    def get_usage_metrics(self) -> Dict[str, Any]:
        raise NotImplementedError("get_usage_metrics method must be implemented")
