from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.graph import CompiledGraph
from dbma.interface.services.sql_generation_service import ISQLGenerationService
from dbma.native.domain.agent_models import MultiAgentResponse, SQLGeneratorAgentInput

class SQLGenerationService(ISQLGenerationService):
    def __init__(self, graph: CompiledGraph):
        self.graph = graph
        
    async def generate_sql(self, input_data: SQLGeneratorAgentInput) -> str:
        initial_state = {
            "messages": [],
            "query": input_data.query,
            "schema_name": input_data.schema_name,
            "database_service": None,
            "schema_info": None,
            "table_list": None,
            "candidates": [],
            "confidence_scores": [],
            "final_confidence_score": None,
            "final_query": None,
            "iteration_count": 0,
            "max_iterations": 5,
        }
        
        final_state = await self.graph.ainvoke(initial_state)
        print("Final state: \n", final_state)
        
        return MultiAgentResponse(
            sql_query=final_state["final_query"],
            sql_candidates=final_state["candidates"],
            sql_candidates_confidence_scores=final_state["confidence_scores"],
            selected_sql=final_state["final_query"],
            confidence_score=final_state["final_confidence_score"]
           
        )
        
        
        