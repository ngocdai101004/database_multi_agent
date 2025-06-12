import pytest
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.language_models import BaseChatModel
from dbma.implementation.services.sql_database_service import SQLDatabaseService
from dbma.implementation.services.sql_generation_service import SQLGenerationService
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from langchain_core.prompts import PromptTemplate
from dbma.dependencies.container import Container
from langgraph.graph.graph import CompiledGraph
from dbma.native.domain.agent_models import SQLGeneratorAgentInput
@pytest.fixture
def sql_generation_graph(container: Container):
    return container.sql_generation_graph()

@pytest.fixture
def sql_generation_service(sql_generation_graph: CompiledGraph):
    return SQLGenerationService(graph=sql_generation_graph)

@pytest.mark.asyncio
async def test_sql_generation_service(sql_generation_service: SQLGenerationService):
    # Arrange
    query = """
    Please list the zip code (schools.zip_code) of all the charter schools (schools.type = 'charter') in Fresno County Office of Education (schools.district = 'Fresno County Office of Education')"""
    schema_name = "california_schools"
    used_tables = []
    schema_description = ""
    input_data = SQLGeneratorAgentInput(query=query, schema_name=schema_name, schema_description=schema_description, used_tables=used_tables)
    
    # Act
    result = await sql_generation_service.generate_sql(input_data=input_data)
    print("Query (in natural language): ", query)
    print("Query (in SQL): ", result)
    
    # Assert
    assert result is not None