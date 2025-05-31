from typing import Any, Dict, List, Optional
import asyncio
import logging
from datetime import datetime

from dbma.native.controller.agent_controller import AgentController
from dbma.native.domain.agents import (
    PlannerAgent,
    ContextRetrieverAgent,
    SQLGeneratorAgent,
    ExecutorAgent,
    VerifierAgent,
    ReporterAgent,
    MonitorAgent
)

class MultiAgentController(AgentController):
    """Concrete implementation of AgentController for coordinating multiple agents."""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._logger = logging.getLogger(__name__)
        self._pipeline_status = {
            'last_updated': None,
            'active_agents': [],
            'current_task': None,
            'error_count': 0
        }
    
    async def initialize_agents(self) -> bool:
        """Initialize all required agents in the pipeline."""
        try:
            # Initialize each agent with appropriate configuration
            self.agents = {
                'planner': PlannerAgent("Query Planner", "Plans query execution"),
                'context': ContextRetrieverAgent("Context Retriever", "Retrieves relevant context"),
                'sql_generator': SQLGeneratorAgent("SQL Generator", "Generates SQL queries"),
                'executor': ExecutorAgent("Query Executor", "Executes SQL queries"),
                'verifier': VerifierAgent("Result Verifier", "Verifies query results"),
                'reporter': ReporterAgent("Result Reporter", "Formats and delivers results"),
                'monitor': MonitorAgent("System Monitor", "Monitors system performance")
            }
            
            # Initialize agent states
            for agent in self.agents.values():
                agent.set_state({
                    'initialized_at': datetime.now().isoformat(),
                    'status': 'ready',
                    'last_execution': None,
                    'error_count': 0
                })
            
            self._update_pipeline_status()
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to initialize agents: {str(e)}")
            return False
    
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
        try:
            self._update_pipeline_status(task=f"Processing query: {query[:50]}...")
            
            # Step 1: Plan the query execution
            planner_result = await self._execute_agent(
                'planner',
                {'query': query, 'context': context}
            )
            
            # Step 2: Retrieve relevant context
            context_result = await self._execute_agent(
                'context',
                {
                    'query': query,
                    'intent': planner_result.get('intent_type'),
                    'entities': planner_result.get('entities', [])
                }
            )
            
            # Step 3: Generate SQL
            sql_result = await self._execute_agent(
                'sql_generator',
                {
                    'query': query,
                    'schema': context_result.get('schema_info'),
                    'context': context_result.get('conversation_history', [])
                }
            )
            
            # Step 4: Execute the query
            execution_result = await self._execute_agent(
                'executor',
                {
                    'sql': sql_result.get('selected_sql'),
                    'params': sql_result.get('parameters', {})
                }
            )
            
            # Step 5: Verify results
            verification_result = await self._execute_agent(
                'verifier',
                {
                    'results': execution_result.get('execution_result'),
                    'query_context': context_result
                }
            )
            
            # Step 6: Format and deliver results
            report_result = await self._execute_agent(
                'reporter',
                {
                    'results': execution_result.get('execution_result'),
                    'verification': verification_result,
                    'query_context': context_result
                }
            )
            
            # Step 7: Monitor and update metrics
            await self._execute_agent(
                'monitor',
                {
                    'pipeline_results': {
                        'planner': planner_result,
                        'context': context_result,
                        'sql': sql_result,
                        'execution': execution_result,
                        'verification': verification_result,
                        'report': report_result
                    }
                }
            )
            
            self._update_pipeline_status()
            return report_result
            
        except Exception as e:
            await self.handle_error(e, {'query': query, 'context': context})
            raise
    
    async def _execute_agent(self, agent_name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a specific agent with input data.
        
        Args:
            agent_name: Name of the agent to execute
            input_data: Input data for the agent
            
        Returns:
            Dict containing agent execution results
        """
        try:
            agent = self.agents.get(agent_name)
            if not agent:
                raise ValueError(f"Agent {agent_name} not found")
            
            # Update agent state
            agent_state = agent.get_state()
            agent_state.update({
                'status': 'running',
                'last_execution': datetime.now().isoformat()
            })
            agent.set_state(agent_state)
            
            # Execute agent
            result = await agent.execute(input_data)
            
            # Validate result
            if not await agent.validate(result):
                raise ValueError(f"Agent {agent_name} validation failed")
            
            # Update agent state
            agent_state.update({
                'status': 'completed',
                'last_success': datetime.now().isoformat()
            })
            agent.set_state(agent_state)
            
            return result
            
        except Exception as e:
            # Update agent state on error
            if agent_name in self.agents:
                agent_state = self.agents[agent_name].get_state()
                agent_state.update({
                    'status': 'error',
                    'last_error': datetime.now().isoformat(),
                    'error_count': agent_state.get('error_count', 0) + 1
                })
                self.agents[agent_name].set_state(agent_state)
            
            self._logger.error(f"Error executing agent {agent_name}: {str(e)}")
            raise
    
    async def get_agent_status(self, agent_name: str) -> Dict[str, Any]:
        """Get status of a specific agent."""
        agent = self.agents.get(agent_name)
        if not agent:
            return {'error': f"Agent {agent_name} not found"}
        
        return {
            'name': agent.name,
            'description': agent.description,
            'state': agent.get_state()
        }
    
    async def update_agent_config(self, 
                                agent_name: str, 
                                config: Dict[str, Any]) -> bool:
        """Update configuration for a specific agent."""
        try:
            agent = self.agents.get(agent_name)
            if not agent:
                return False
            
            # Update agent configuration
            agent_state = agent.get_state()
            agent_state.update(config)
            agent.set_state(agent_state)
            
            self._update_pipeline_status()
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to update agent config: {str(e)}")
            return False
    
    async def get_pipeline_status(self) -> Dict[str, Any]:
        """Get status of the entire agent pipeline."""
        return {
            'pipeline_status': self._pipeline_status,
            'agents': {
                name: agent.get_state()
                for name, agent in self.agents.items()
            }
        }
    
    async def handle_error(self, 
                          error: Exception, 
                          context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle errors in the agent pipeline."""
        try:
            error_info = {
                'error_type': type(error).__name__,
                'error_message': str(error),
                'context': context,
                'timestamp': datetime.now().isoformat()
            }
            
            # Update pipeline status
            self._pipeline_status['error_count'] += 1
            self._pipeline_status['last_error'] = error_info
            
            # Log error
            self._logger.error(f"Pipeline error: {error_info}")
            
            # Notify monitoring agent
            if 'monitor' in self.agents:
                await self._execute_agent('monitor', {
                    'error': error_info,
                    'pipeline_status': self._pipeline_status
                })
            
            return error_info
            
        except Exception as e:
            self._logger.error(f"Error handling pipeline error: {str(e)}")
            return {'error': 'Failed to handle error'}
    
    def _update_pipeline_status(self, task: Optional[str] = None):
        """Update the pipeline status."""
        self._pipeline_status.update({
            'last_updated': datetime.now().isoformat(),
            'active_agents': [
                name for name, agent in self.agents.items()
                if agent.get_state().get('status') == 'running'
            ],
            'current_task': task or self._pipeline_status.get('current_task')
        }) 