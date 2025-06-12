from abc import ABC, abstractmethod
from typing import Any, Dict, List

from dbma.interface.services.sql_database_service import ISQLDatabaseService
from dbma.native.domain.agent_models import (SQLGeneratorAgentInput,
                                             SQLGeneratorAgentResponse)
from langgraph.graph.graph import CompiledGraph


class ISQLGenerationService(ABC):
    @abstractmethod
    async def generate_sql(self, input_data: SQLGeneratorAgentInput) -> SQLGeneratorAgentResponse:
        """
        Generate SQL query from natural language query
        
        Args:
            query: Natural language query
            schema_name: Name of the schema to use
            
        Returns:
            Generated SQL query
        """
        pass