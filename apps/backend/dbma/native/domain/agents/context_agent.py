from typing import Any, Dict, List, Optional

from dbma.interface.services.context_service import IContextService
from dbma.native.domain.agent import Agent
from dbma.native.domain.agent_models import ContextAgentInput, ContextAgentResponse

class ContextRetrieverAgent(Agent):
    """Agent responsible for retrieving relevant context and database schema."""
    
    context_service: IContextService
    
    def __init__(
        self,
        context_service: IContextService,
    ):
        self.context_service = context_service
        
    async def execute(self, input_data: ContextAgentInput) -> ContextAgentResponse:
        """Retrieve relevant context and schema information.
        
        Args:
            input_data: Contains query context and requirements
            
        Returns:
            Dict containing:
            - schema_name: str
            - schema_description: str
            - used_tables: List[str]
            - enrich_query: str
        """
        result: ContextAgentResponse = await self.context_service.analyze_context(input_data=input_data)
        return result
    
    async def validate(self, result: Dict[str, Any]) -> bool:
        """Validate the context retrieval results."""
        required_fields = ['schema_name', 'schema_description', 'used_tables', 'enrich_query']
        return all(field in result for field in required_fields) 