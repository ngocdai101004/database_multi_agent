import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from dbma.implementation.services.sql_database_service import SQLDatabaseService
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from langchain_community.utilities import SQLDatabase
from dbma.dependencies.container import Container

@pytest.fixture
def schema_name():
    return "california_schools"

@pytest.fixture
def llm_service(container: Container):
    return container.llm_service()

@pytest.fixture
def sql_database_service(schema_name: str, llm_service: OpenAILLMService):
    return SQLDatabaseService(schema_name, llm_service)

# def test_init_sql_database_service(sql_database_service: SQLDatabaseService):
#     """Test initialization of SQLDatabaseService"""
#     db: SQLDatabase = sql_database_service.db
#     print("--------------------------------")
#     print("test_init_sql_database_service: Test table info: ", db.table_info)
#     print("--------------------------------")
#     # Assert
#     assert sql_database_service.db is not None
#     assert sql_database_service.toolkit is not None

# def test_get_tools(sql_database_service: SQLDatabaseService):
#     """Test getting all tools"""
#     # Arrange
#     expected_tool_count = 4  # query, info, list, checker
    
#     # Act
#     query_tool = sql_database_service.get_query_tool()
#     schema_info_tool = sql_database_service.get_schema_info_tool()
#     list_tables_tool = sql_database_service.get_list_tables_tool()
#     query_checker_tool = sql_database_service.get_query_checker_tool()
    
#     # Assert
#     assert query_tool is not None
#     assert schema_info_tool is not None
#     assert list_tables_tool is not None
#     assert query_checker_tool is not None
#     print("--------------------------------")
#     print("--- test_get_tools: query_tool: ", query_tool.name, query_tool.description, query_tool.args)
#     print("--- test_get_tools: schema_info_tool: ", schema_info_tool.name, schema_info_tool.description, schema_info_tool.args)
#     print("--- test_get_tools: list_tables_tool: ", list_tables_tool.name, list_tables_tool.description, list_tables_tool.args)
#     print("--- test_get_tools: query_checker_tool: ", query_checker_tool.name, query_checker_tool.description, query_checker_tool.args)
#     print("--------------------------------")
#     # Verify tool names
#     assert "sql_db_query" in query_tool.name.lower()
#     assert "sql_db_schema" in schema_info_tool.name.lower()
#     assert "sql_db_list_tables" in list_tables_tool.name.lower()
#     assert "sql_db_query_checker" in query_checker_tool.name.lower()
    
def test_execute_query_valid(sql_database_service: SQLDatabaseService):
    """Test executing a valid query"""
    # Arrange
    valid_query = """SELECT DISTINCT Zip FROM schools WHERE District = 'Fresno County Office of Education' AND Charter = 1"""
    
    # Act
    result = sql_database_service.execute_query(valid_query)
    print("--------------------------------")
    print("test_execute_query_valid: Test result: ", result)
    print("--------------------------------")
    
    # Assert
    assert result is not None
    assert isinstance(result, str)

# def test_execute_query_invalid(sql_database_service: SQLDatabaseService):
#     """Test executing an invalid query"""
#     # Arrange
#     invalid_query = "SELECT * FROM nonexistent_table"
    
#     # Act & Assert
#     with pytest.raises(Exception, match="Error executing query"):
#         sql_database_service.execute_query(invalid_query)

# @pytest.mark.asyncio
# async def test_list_tables_tool(sql_database_service: SQLDatabaseService):
#     """Test list tables"""
#     # Arrange
#     list_tables_tool = sql_database_service.get_list_tables_tool()
    
#     # Action
#     result = await list_tables_tool.arun(tool_input={})
#     print("--------------------------------")
#     print("test_list_tables_tool: Test result: ", result)
#     print("--------------------------------")
#     assert result is not None
#     assert isinstance(result, str)
    
# @pytest.mark.asyncio
# async def test_schema_info_tool(sql_database_service: SQLDatabaseService):
#     """Test schema info"""
#     # Arrange
#     tables = sql_database_service.get_list_tables_tool().run(tool_input={})
#     schema_info_tool = sql_database_service.get_schema_info_tool()
    
#     # Action
#     result = await schema_info_tool.arun(tool_input=tables)
#     print("--------------------------------")
#     print("test_schema_info_tool: Test result: ", result)
#     print("--------------------------------")
    
#     # Assert
#     assert result is not None
#     assert isinstance(result, str)

# @pytest.mark.asyncio
# async def test_query_checker_tool(sql_database_service: SQLDatabaseService):
#     """Test query checker"""
#     # Arrange
#     query = """SELECT T2.Zip FROM frpm AS T1 INNER JOIN schools AS T2 ON T1.CDSCode = T2.CDSCode WHERE T1.`District Name` = 'Fresno County Office of Education' AND T1.`Charter School (Y/N)` = 1"""
#     query_checker_tool = sql_database_service.get_query_checker_tool()
    
#     # Action
#     result = await query_checker_tool.arun(tool_input=query)
#     print("--------------------------------")
#     print("test_query_checker_tool: Test result: ", result)
#     print("--------------------------------")
    
#     # Assert
#     assert result is not None
#     assert isinstance(result, str)
    
# @pytest.mark.asyncio
# async def test_query_tool(sql_database_service: SQLDatabaseService):
#     """Test query tool"""
#     # Arrange
#     query = """SELECT `Free Meal Count (Ages 5-17)` / `Enrollment (Ages 5-17)` FROM frpm WHERE `Educational Option Type` = 'Continuation School' AND `Free Meal Count (Ages 5-17)` / `Enrollment (Ages 5-17)` IS NOT NULL ORDER BY `Free Meal Count (Ages 5-17)` / `Enrollment (Ages 5-17)` ASC LIMIT 3"""
#     query_tool = sql_database_service.get_query_tool()
    
#     # Action
#     result = await query_tool.arun(tool_input={"query": query})
#     print("--------------------------------")
#     print("test_query_tool: Test result: ", result)
#     print("--------------------------------")
    
#     # Assert
#     assert result is not None
#     assert isinstance(result, str)