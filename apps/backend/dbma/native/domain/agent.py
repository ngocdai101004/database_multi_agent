from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class Agent(ABC):
    """Abstract base class defining the interface for all agents in the system."""
    
    def __init__(self, name: str, description: str):
        """Initialize the agent with name and description.
        
        Args:
            name: Name of the agent
            description: Description of the agent's purpose
        """
        self.name = name
        self.description = description
        self._state: Dict[str, Any] = {}
    
    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's main functionality.
        
        Args:
            input_data: Input data for the agent's execution
            
        Returns:
            Dict containing the execution results
        """
        pass
    
    @abstractmethod
    async def validate(self, result: Dict[str, Any]) -> bool:
        """Validate the execution results.
        
        Args:
            result: Results to validate
            
        Returns:
            bool indicating if validation passed
        """
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current state of the agent.
        
        Returns:
            Dict containing the agent's current state
        """
        return self._state
    
    def set_state(self, state: Dict[str, Any]) -> None:
        """Set the agent's state.
        
        Args:
            state: New state to set
        """
        self._state = state
    
    def get_name(self) -> str:
        """Get the agent's name.
        
        Returns:
            str: Agent's name
        """
        return self.name
    
    def get_description(self) -> str:
        """Get the agent's description.
        
        Returns:
            str: Agent's description
        """
        return self.description 