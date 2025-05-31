from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class DatabaseService(ABC):
    """Interface for database operations."""
    
    @abstractmethod
    async def connect(self, connection_params: Dict[str, Any]) -> bool:
        """Connect to the database.
        
        Args:
            connection_params: Database connection parameters
            
        Returns:
            bool indicating if connection was successful
        """
        pass
    
    @abstractmethod
    async def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a SQL query.
        
        Args:
            query: SQL query to execute
            params: Optional query parameters
            
        Returns:
            Query results
        """
        pass
    
    @abstractmethod
    async def get_schema(self) -> Dict[str, Any]:
        """Get database schema information.
        
        Returns:
            Dict containing schema information
        """
        pass
    
    @abstractmethod
    async def validate_query(self, query: str) -> bool:
        """Validate a SQL query.
        
        Args:
            query: SQL query to validate
            
        Returns:
            bool indicating if query is valid
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the database connection."""
        pass 