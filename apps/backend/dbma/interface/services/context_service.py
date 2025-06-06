from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class IContextService(ABC):
    @abstractmethod
    async def analyze_context(self, query: str, schema_info: Dict[str, Any], get_schema_tool: Any) -> Dict[str, Any]:
        pass
