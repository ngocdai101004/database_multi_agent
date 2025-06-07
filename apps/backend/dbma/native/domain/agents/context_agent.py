from typing import Any, Dict, List, Optional

from dbma.interface.services.context_service import IContextService
from dbma.native.domain.agent import Agent


class ContextRetrieverAgent(Agent):
    """Agent responsible for retrieving relevant context and database schema."""
    
    context_service: IContextService
    
    def __init__(
        self,
        context_service: IContextService,
    ):
        self.context_service = context_service
        
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant context and schema information.
        
        Args:
            input_data: Contains query context and requirements
            
        Returns:
            Dict containing:
            - conversation_history: List[Dict]
            - relevant_tables: List[str]
            - table_relationships: Dict
            - schema_info: Dict
        """
        result = await self.context_service.analyze_context(input_data['query'], input_data['context'])
        return {}
    
    async def validate(self, result: Dict[str, Any]) -> bool:
        """Validate the context retrieval results."""
        required_fields = ['conversation_history', 'relevant_tables', 'table_relationships', 'schema_info']
        return all(field in result for field in required_fields) 