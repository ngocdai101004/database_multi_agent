from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from dbma.native.domain.agent import Agent


class AgentController(ABC):
    """Interface for controlling and coordinating agent operations."""
    
    @abstractmethod
    async def initialize_agents(self) -> bool:
        """Initialize all required agents.
        
        Returns:
            bool indicating if initialization was successful
        """
        pass
    
    @abstractmethod
    async def process_query(self, 
                          query: str, 
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process a natural language query through the agent pipeline.
        
        Args:
            query: Natural language query
            context: Optional context information
            
        Returns:
            Dict containing processing results
        """
        pass
    
    @abstractmethod
    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Dict containing agent status
        """
        pass
    
    @abstractmethod
    async def update_agent_config(self, 
                                agent_name: str, 
                                config: Dict[str, Any]) -> bool:
        """Update configuration for a specific agent.
        
        Args:
            agent_name: Name of the agent
            config: New configuration parameters
            
        Returns:
            bool indicating if update was successful
        """
        pass
    
    @abstractmethod
    async def get_pipeline_status(self) -> Dict[str, Any]:
        """Get status of the entire agent pipeline.
        
        Returns:
            Dict containing pipeline status
        """
        pass
    
    @abstractmethod
    async def handle_error(self, 
                          error: Exception, 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle errors in the agent pipeline.
        
        Args:
            error: Exception that occurred
            context: Error context information
            
        Returns:
            Dict containing error handling results
        """
        pass 