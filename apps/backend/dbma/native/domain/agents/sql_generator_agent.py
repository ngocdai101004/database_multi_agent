from typing import Any, Dict, List, Optional

from dbma.interface.services.sql_generation_service import \
    ISQLGenerationService
from dbma.native.domain.agent import Agent
from dbma.native.domain.agent_models import (SQLGeneratorAgentInput,
                                             SQLGeneratorAgentResponse)


class SQLGeneratorAgent(Agent):
    """Agent responsible for generating SQL queries from natural language."""
    def __init__(self, sql_generation_service: ISQLGenerationService):
        self.sql_generation_service = sql_generation_service
        
    async def execute(self, input_data: SQLGeneratorAgentInput) -> SQLGeneratorAgentResponse:
        """Generate SQL queries from natural language input.
        
        Args:
            input_data: Contains natural language query and context
            
        Returns:
            Dict containing:
            - sql_candidates: List[str]
            - selected_sql: str
            - confidence_score: float
        """
        # TODO: Implement SQL generation
        # TODO: Implement candidate selection
        # TODO: Implement confidence scoring
        result : SQLGeneratorAgentResponse = await self.sql_generation_service.generate_sql(input_data=input_data)
        return result
    
    async def validate(self, result: Dict[str, Any]) -> bool:
        """Validate the generated SQL."""
        required_fields = ['sql_candidates', 'selected_sql', 'confidence_score']
        return all(field in result for field in required_fields) 