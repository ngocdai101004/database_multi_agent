from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from dbma.native.domain.agent_models import (ContextAgentInput,
                                             ContextAgentResponse)


class IContextService(ABC):
    @abstractmethod
    async def analyze_context(self, input_data: ContextAgentInput) -> ContextAgentResponse:
        pass
