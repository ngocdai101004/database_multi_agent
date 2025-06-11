from typing import TypedDict, List, Optional
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage
from langgraph.graph.graph import CompiledGraph
from dbma.interface.services.sql_generation_service import ISQLGenerationService

class SQLGenerationService(ISQLGenerationService):
    def __init__(self, graph: CompiledGraph):
        self.graph = graph
        
    async def generate_sql(self, query: str, schema_name: str) -> str:
        initial_state = {
            "messages": [],
            "query": query,
            "schema_name": schema_name,
            "database_service": None,
            "schema_info": None,
            "table_list": None,
            "candidates": [],
            "final_query": None,
            "iteration_count": 0,
            "max_iterations": 3,
        }
        
        final_state = await self.graph.ainvoke(initial_state)
        print("Final state: \n", final_state)
        
        return final_state["final_query"]
        
        
        