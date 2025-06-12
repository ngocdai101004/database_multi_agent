from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dbma.native.domain.agent_models import PlannerAgentInput, PlannerAgentResponse


class IPlannerService(ABC):
    @abstractmethod
    async def plan(self, input_data: PlannerAgentInput) -> PlannerAgentResponse:
        pass
