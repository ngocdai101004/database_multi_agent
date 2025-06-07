from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import Tool

from dbma.interface.services.context_service import IContextService
from dbma.interface.services.llm_service import ILLMService
from dbma.interface.services.schema_storage_service import ISchemaStorageService
from dbma.native.domain.tool import SchemaTool
from langchain_core.tools import Tool

instructions_prompt = """
You are a helpful assistant with expertise in database schema analysis and query understanding.
Your task is to analyze the user's query and database schema information to:
1. Identify the relevant database schema
2. Extract schema details using the provided tool
3. Determine which tables and their relationships are needed
4. Enrich the query description with specific table and column names in the schema. Based on the schema, you can change the request of the user to make it more specific and accurate.
You will receive:
- The user's query
- Information about available database schemas

You have access to a tool that can get schema details by name. Use this tool when you need to get detailed information about a specific schema.

You must return:
- The name of the schema to use
- The full schema description (obtained using the tool)
- List of tables that will be used
- An enriched query description with specific table and column names in the schema.
"""

few_shot_examples = """
Query: Show me the total sales by customer in Hanoi for the last quarter
{
    "schema_name": "sales_schema",
    "schema_description": "The schema contains two tables: customers and sales.
    customers table has the following columns: id, name, location.
    sales table has the following columns: id, customer_id, amount, date.",
    "used_tables": ["customers", "sales"],
    "enrich_query": "how me the total sales (SUM(sales.amount)) by customer (customers.name) in Hanoi (customers.location) for the last quarter (sales.date >= '2023-07-01' AND sales.date <= '2023-09-30')"
}
"""

class ContextOutput(BaseModel):
    schema_name: str
    schema_description: str
    schema_detail: str
    used_tables: List[str]
    enrich_query: str

class ContextService(IContextService):
    llm_service: ILLMService
    schema_storage_service: ISchemaStorageService
    
    def __init__(self, llm_service: ILLMService, schema_storage_service: ISchemaStorageService):
        self.llm_service = llm_service
        self.schema_storage_service = schema_storage_service
        self.get_schema_tool = SchemaTool(schema_storage_service)
        self.get_schema_tool_langchain = self._convert_from_domain_tool_to_langchain_tool(self.get_schema_tool)
        


    async def analyze_context(
        self, 
        query: str, 
    ) -> Dict[str, Any]:
        """
        Analyze the context of the query and determine the relevant schema and tables.
        
        Args:
            query: The user's query
            schema_info: Information about available database schemas
            get_schema_tool: Tool to get schema details by name
            
        Returns:
            Dict containing schema_name, schema details, used tables, and enriched query
        """
        # Create a tool for getting schema details


        # Prepare the context for the LLM
        context = {
            "query": query,
            "schema_info": self.schema_storage_service.get_db_description()
        }

        messages = [
            SystemMessage(content=instructions_prompt),
            HumanMessage(content=few_shot_examples),
            HumanMessage(content=str(context))
        ]

        chain = (
            self.llm_service.llm.bind(tools=[self.get_schema_tool_langchain])
            .with_structured_output(ContextOutput)
        )
        
        result = await chain.ainvoke(messages)
        return result

    async def get_usage_metrics(self) -> Dict[str, Any]:
        return self.llm_service.get_usage_metrics()


    def _convert_from_domain_tool_to_langchain_tool(self, tool: SchemaTool) -> Tool:
        def _get_schema_details(schema_name: str) -> str:
            response = self.schema_storage_service.get_schema(schema_name)
            return str(response)
        
        return Tool(
            name="get_schema_details",
            description="Get detailed information about a database schema by its name",
            func=_get_schema_details
        )