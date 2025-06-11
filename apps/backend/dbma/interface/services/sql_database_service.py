from abc import ABC, abstractmethod
from typing import List, Dict, Any
from langchain.tools import BaseTool

class ISQLDatabaseService(ABC):
    """Interface for SQL database service"""

    @abstractmethod
    def get_query_tool(self) -> BaseTool:
        """Get the tool for executing SQL queries"""
        pass
    
    @abstractmethod
    def get_schema_info_tool(self) -> BaseTool:
        """Get the tool for retrieving schema information"""
        pass
    
    @abstractmethod
    def get_list_tables_tool(self) -> BaseTool:
        """Get the tool for listing tables"""
        pass
    
    @abstractmethod
    def get_query_checker_tool(self) -> BaseTool:
        """Get the tool for checking SQL queries"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> Any:
        """Execute a SQL query and return results"""
        pass
    
    @abstractmethod
    def validate_query(self, query: str) -> bool:
        """Validate if a SQL query is valid"""
        pass 