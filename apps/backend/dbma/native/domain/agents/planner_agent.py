from typing import Any, Dict, List, Optional

from dbma.interface.services.planner_service import IPlannerService
from dbma.native.domain.agent import Agent
from dbma.native.domain.agent_models import (PlannerAgentInput,
                                             PlannerAgentResponse)


class PlannerAgent(Agent):
    """Agent responsible for understanding user intent and planning the query execution."""
    
    planner_service: IPlannerService
    
    def __init__(
        self, 
        planner_service: IPlannerService,
    ):
        self.planner_service = planner_service
        
    async def execute(self, input_data: PlannerAgentInput) -> PlannerAgentResponse:
        """Process user input to understand intent and plan execution.
        
        Args:
            input_data: Contains user query and context
             - query: str
             - context: Optional[Dict[str, Any]]
            
        Returns:
            Dict containing:
            - detected_language: str
            - intent_type: str
            - entities: List[str]
            - complexity_score: float
        """
        # TODO: Implement language detection
        # TODO: Implement intent classification
        # TODO: Implement entity extraction
        # TODO: Implement complexity estimation
        
        result : PlannerAgentResponse = await self.planner_service.plan(input_data=input_data)
        return result