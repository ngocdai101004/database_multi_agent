import random
from typing import List, Dict, Any, TypedDict, Optional
from pydantic import Field, BaseModel
from langgraph.graph import StateGraph, END
from langgraph.graph.graph import CompiledGraph
from langchain.prompts import PromptTemplate
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage, SystemMessage
from dbma.interface.services.sql_generation_service import ISQLGenerationService
from dbma.interface.services.sql_database_service import ISQLDatabaseService
from dbma.interface.services.llm_service import ILLMService
from dbma.implementation.services.sql_database_service import SQLDatabaseService

MSSQL_SQL_GENERATION_PROMPT = """
You are an agent designed to generate SQL queries for a Microsoft SQL Server (T-SQL) database.

## Schema Information:
{schema_info}

## Instructions:
- Given a natural language question, your task is to output 3 syntactically correct T-SQL SQL candidates (ANSI SQL syntax).
- Only output the SQL query. Do not include explanations or any additional text.
- NEVER include markdown syntax or backticks.
- Only use table names and column names provided in the schema information above.
- Unless specified otherwise, LIMIT the number of returned rows to 100 using TOP syntax.
- Focus only on relevant columns needed to answer the question.
- Do NOT perform any DML operations such as INSERT, UPDATE, DELETE, or DROP.
- You MUST double-check the correctness of the SQL query before outputting it.

## Output Format:
- List of three SQL queries, each with a different approach to the problem.
- Each SQL query should be a valid T-SQL query.
- Each SQL query should be a different approach to the problem.
"""

class SQLGenerationState(TypedDict):
    messages: List[BaseMessage]
    query: str
    schema_name: str
    database_service: Optional[ISQLDatabaseService]
    schema_info: Optional[str]
    table_list: Optional[List[str]]
    candidates: List[str]
    final_query: Optional[str]
    iteration_count: int
    max_iterations: int
    
class SQLGenerationCandidate(BaseModel):
    sql_query: str = Field(description="The SQL query in natural language to be executed, explain the query with the schema information")
    sql_candidate: List[str] = Field(description="List of 3 SQL syntax candidates, using ANSI SQL syntax")

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
        state["max_iterations"] = 3
        state["candidates"] = []
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
        response: AIMessage = await self.llm_service.llm.with_structured_output(SQLGenerationCandidate).ainvoke(state["messages"])
        candidates = []
        for candidate in response.sql_candidate:
            candidates.append(self._clean_sql_query(candidate))
            
        state["candidates"] = candidates
        state["iteration_count"] = state["iteration_count"] + 1
        state["messages"].append(AIMessage(content=str(response)))
        return state
    
    async def _validate_node(self, state: SQLGenerationState) -> SQLGenerationState:
        """Validate SQL candidates and select the best one"""
        database_service = state["database_service"]
        query_checker_tool = database_service.get_query_checker_tool()
        query_tool = database_service.get_query_tool()
        
        candidate_results = {}
        
        new_candidates = []
        for candidate in state["candidates"]:
            # First check syntax with query checker
            checked_query = await query_checker_tool.arun(candidate)
            processed_query = self._clean_sql_query(checked_query)

            # Execute the query
            result = await query_tool.arun(processed_query)
            
            if "error" in result.lower():
                state["messages"].append(AIMessage(content=f"Error: {result}"))
                continue
            
            new_candidates.append(candidate)
            candidate_results[candidate] = str(result)
                
        # Select final query based on results
        if len(new_candidates) > 0:
            final_query = random.choice(new_candidates)
            state["final_query"] = final_query
        else:
            state["final_query"] = None
        
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
            "final_query": None,
            "iteration_count": 0,
            "max_iterations": 3
        }
        
        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        
        # Return the final query or empty string if none found
        return final_state.get("final_query", "")
    
    def get_sql_generation_graph(self) -> CompiledGraph:
        """Get the SQL generation graph"""
        return self.graph