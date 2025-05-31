from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IPlannerService(ABC):
    @abstractmethod
    async def plan(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass
