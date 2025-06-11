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
    List the authors along with the number of papers they have written that meet all the following conditions:
    The paper is published in a venue where at least one paper has been cited more than 10 times.
    The paper has itself been cited more than 10 times.
    The paper uses at least one dataset.
    Only include authors who have written more than 2 such papers.
    Sort the results by the number of qualifying papers in descending order.
    """
    schema_name = "cinema"
    
    # Act
    result = await sql_generation_service.generate_sql(query, schema_name)
    print("Query (in natural language): ", query)
    print("Query (in SQL): ", result)
    
    # Assert
    assert result is not None