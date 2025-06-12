import logging
import random
from typing import Any, Dict, List, Optional, TypedDict

from dbma.implementation.services.sql_database_service import \
    SQLDatabaseService
from dbma.interface.services.llm_service import ILLMService
from dbma.interface.services.sql_database_service import ISQLDatabaseService
from dbma.interface.services.sql_generation_service import \
    ISQLGenerationService
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
                                     SystemMessage)
from langgraph.graph import END, StateGraph
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field

logger = logging.getLogger("dbma")

MSSQL_SQL_GENERATION_PROMPT = """
You are an agent designed to generate SQL queries for a Microsoft SQL Server (T-SQL) database.

## Schema Information:
{schema_info}

## Instructions:
- Given a natural language question, your task is to output 3 syntactically correct T-SQL SQL candidates (ANSI SQL syntax).
- Only output the SQL query and the confidence score. Do not include explanations or any additional text.
- NEVER include markdown syntax or backticks.
- Only use table names and column names provided in the schema information above.
- Should use the alias to avoid ambiguity when there are columns with the same name
- Unless specified otherwise, LIMIT the number of returned rows to 100 using TOP syntax.
- Focus only on relevant columns needed to answer the question.
- Do NOT perform any DML operations such as INSERT, UPDATE, DELETE, or DROP.
- You MUST double-check the correctness of the SQL query before outputting it.
- The confidence score is the confidence score of the SQL query, from 0 to 100, 100 is the highest confidence.

## Output Format:
- List of three SQL queries, each with a different approach to the problem.
- List of three confidence scores, each with a different approach to the problem.

"""

class SQLGenerationState(TypedDict):
    messages: List[BaseMessage]
    query: str
    schema_name: str
    database_service: Optional[ISQLDatabaseService]
    schema_info: Optional[str]
    table_list: Optional[List[str]]
    candidates: List[str]
    confidence_scores: List[float]
    final_query: Optional[str]
    final_confidence_score: Optional[float]
    iteration_count: int
    max_iterations: int
    
class SQLGenerationCandidate(BaseModel):
    sql_query: str = Field(description="The SQL query in natural language to be executed, explain the query with the schema information")
    sql_candidate: List[str] = Field(description="List of 3 SQL syntax candidates, using ANSI SQL syntax")
    confidence_score_list: List[float] = Field(description=" List of three confidence scores, each with a different approach to the problem, from 0 to 100, 100 is the highest confidence. The scores are different because the candidates are different approaches to the problem.")

class SQLGenerationGraph:
    def __init__(self, llm_service: ILLMService):
        """
        Initialize SQL generation service
        
        Args:
            llm_service: Language model for generating SQL
        """
        self.llm_service: ILLMService = llm_service
        self.graph = self._create_graph()
    
    def _create_graph(self) -> CompiledGraph:
        """Create the LangGraph workflow"""
        # Define the graph
        workflow = StateGraph(SQLGenerationState)
        
        # Add nodes
        workflow.add_node("init_node", self._init_node)
        workflow.add_node("prepare_node", self._prepare_node)
        workflow.add_node("llm_node", self._llm_node)
        workflow.add_node("validate_node", self._validate_node)
        
        # Define edges
        workflow.set_entry_point("init_node")
        workflow.add_edge("init_node", "prepare_node")
        workflow.add_edge("prepare_node", "llm_node")
        workflow.add_edge("llm_node", "validate_node")
        
        # Conditional edge from validate_node
        workflow.add_conditional_edges(
            "validate_node",
            self._should_retry,
            {
                "retry": "llm_node",
                "end": END
            }
        )
        
        return workflow.compile()
    
    def _init_node(self, state: SQLGenerationState) -> SQLGenerationState:
        """Initialize the database service based on schema name"""
        # This would be implemented based on your database service factory
        # For now, assuming you have a way to create database_service from schema_name
        database_service = self._create_database_service(state["schema_name"])
        state["database_service"] = database_service
        state["iteration_count"] = 0
        state["candidates"] = []
        state["confidence_scores"] = []
        state["final_confidence_score"] = None
        state["final_query"] = None
        state["messages"] = []
        return state
    
    def _prepare_node(self, state: SQLGenerationState) -> SQLGenerationState:
        """Prepare schema information by getting table list and schema details"""
        # Prepare schema information
        database_service = state["database_service"]
        
        # Get list of tables
        list_tables_tool = database_service.get_list_tables_tool()
        table_list_result: str = list_tables_tool.run("")
        
        # Get schema information using the table list
        schema_info_tool = database_service.get_schema_info_tool()
        schema_info = schema_info_tool.run(table_list_result)
        
        state["table_list"] = [table.strip() for table in table_list_result.split(",")]
        state["schema_info"] = schema_info
        
        # Prepare prompt
        prompt_template = PromptTemplate(
            input_variables=["schema_info"],
            template=MSSQL_SQL_GENERATION_PROMPT
        )
        
        state["messages"].append(SystemMessage(content=prompt_template.format(schema_info=state["schema_info"])))
        state["messages"].append(HumanMessage(content=state["query"]))
        
        return state

    
    async def _llm_node(self, state: SQLGenerationState) -> SQLGenerationState:
        response: SQLGenerationCandidate = await self.llm_service.llm.with_structured_output(SQLGenerationCandidate).ainvoke(state["messages"])
        candidates = []
        for candidate in response.sql_candidate:
            candidates.append(self._clean_sql_query(candidate))
            
        state["candidates"] = candidates
        state["confidence_scores"] = response.confidence_score_list
        state["iteration_count"] = state["iteration_count"] + 1
        state["messages"].append(AIMessage(content=str(response)))
        return state
    
    async def _validate_node(self, state: SQLGenerationState) -> SQLGenerationState:
        """Validate SQL candidates and select the best one"""
        database_service = state["database_service"]
        query_checker_tool = database_service.get_query_checker_tool()
        query_tool = database_service.get_query_tool()
        
        
        new_candidates = []
        new_confidence_scores = []
        if len(state["confidence_scores"]) == 0:
            state["confidence_scores"] = [0.0] * len(state["candidates"])
        for candidate, confidence_score in zip(state["candidates"], state["confidence_scores"]):
            # First check syntax with query checker
            checked_query = await query_checker_tool.arun(candidate)
            processed_query = self._clean_sql_query(checked_query)

            # Execute the query
            result = await query_tool.arun(processed_query)
            
            if "error" in result.lower():
                state["messages"].append(AIMessage(content=f"Error: {result}"))
                print("Error: ", result)
                continue
            
            new_candidates.append(candidate)
            new_confidence_scores.append(confidence_score)
            
                
        # Select final query based on results
        if len(new_candidates) > 0:
            # Sort candidates by confidence score
            sorted_candidates = sorted(zip(new_candidates, new_confidence_scores), key=lambda x: x[1], reverse=True)
            state["final_query"] = sorted_candidates[0][0]
            state["final_confidence_score"] = sorted_candidates[0][1]
        else:
            state["final_query"] = None
            state["final_confidence_score"] = None
        
        return state
    
    def _should_retry(self, state: SQLGenerationState) -> str:
        """Determine if we should retry or end"""
        # If we have a valid query, end
        if state["final_query"]:
            return "end"
        
        # If we've exceeded max iterations, end (even without valid query)
        if state["iteration_count"] >= state["max_iterations"]:
            return "end"
        
        # Otherwise, retry
        return "retry"
    
    def _clean_sql_query(self, sql_query: str) -> str:
        """Clean SQL query by removing markdown, backticks, etc."""
        # Remove markdown code blocks
        if sql_query.startswith("```sql"):
            sql_query = sql_query[6:]
        elif sql_query.startswith("```"):
            sql_query = sql_query[3:]
        
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        
        # Remove single backticks
        sql_query = sql_query.replace("`", "")
        
        return sql_query.strip()
    
    def _create_database_service(self, schema_name: str) -> ISQLDatabaseService:
        """Create database service instance for given schema"""
        return SQLDatabaseService(schema_name, self.llm_service)
    
    async def generate_sql(self, query: str, schema_name: str) -> str:
        """
        Generate SQL query from natural language query
        
        Args:
            query: Natural language query
            schema_name: Name of the schema to use
            
        Returns:
            Generated SQL query
        """
        # Initial state
        initial_state: SQLGenerationState = {
            "query": query,
            "schema_name": schema_name,
            "database_service": None,
            "schema_info": None,
            "table_list": None,
            "candidates": [],
            "confidence_scores": [],
            "final_confidence_score": None,
            "final_query": None,
            "iteration_count": 0,
            "max_iterations": 5
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Return the final query or empty string if none found
        return final_state.get("final_query", "")
    
    def get_sql_generation_graph(self) -> CompiledGraph:
        """Get the SQL generation graph"""
        return self.graph