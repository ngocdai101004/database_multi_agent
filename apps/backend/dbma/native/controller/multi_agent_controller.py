import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from dbma.dependencies.container import Container
from dbma.interface.services.context_service import IContextService
from dbma.interface.services.planner_service import IPlannerService
from dbma.interface.services.sql_generation_service import \
    ISQLGenerationService
from dbma.native.controller.agent_controller import AgentController
from dbma.native.domain.agent_models import (ContextAgentInput,
                                             ContextAgentResponse,
                                             MultiAgentResponse,
                                             PlannerAgentInput,
                                             PlannerAgentResponse,
                                             SQLGeneratorAgentInput,
                                             SQLGeneratorAgentResponse)
from dbma.native.domain.agents import (ContextRetrieverAgent, ExecutorAgent,
                                       MonitorAgent, PlannerAgent,
                                       ReporterAgent, SQLGeneratorAgent,
                                       VerifierAgent)
from dependency_injector.wiring import Provide, inject


class MultiAgentController:
    """Concrete implementation of AgentController for coordinating multiple agents."""
    @inject
    async def process_query(
        self,
        query: str,
        planner_service: IPlannerService = Provide[Container.planner_service],
        context_service: IContextService = Provide[Container.context_service],
        sql_generation_service: ISQLGenerationService = Provide[Container.sql_generation_service],
    ) -> MultiAgentResponse:
        
        planner_agent = PlannerAgent(planner_service)
        context_agent = ContextRetrieverAgent(context_service)
        sql_generator_agent = SQLGeneratorAgent(sql_generation_service)
        
        input_data = PlannerAgentInput(query=query, context=None)
        planner_agent_response: PlannerAgentResponse = await planner_agent.execute(input_data)
        
        context_agent_input = ContextAgentInput(query=planner_agent_response.rewritten_query)
        context_agent_response: ContextAgentResponse = await context_agent.execute(context_agent_input) 
        
        
        sql_generator_agent_input = SQLGeneratorAgentInput(
            query=context_agent_response.enrich_query, 
            schema_name=context_agent_response.schema_name,
            schema_description=context_agent_response.schema_description,
            used_tables=context_agent_response.used_tables
        )
        
        sql_generator_agent_response: SQLGeneratorAgentResponse = await sql_generator_agent.execute(sql_generator_agent_input)
        
        return sql_generator_agent_response

        
        
        
    

    
    