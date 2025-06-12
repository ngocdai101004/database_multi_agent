from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class Agent(ABC):
    """Abstract base class defining the interface for all agents in the system."""
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality.
        
        Args:
            input_data: Input data for the agent's execution
            
        Returns:
            Dict containing the execution results
        """
        pass
   