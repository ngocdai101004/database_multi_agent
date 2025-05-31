import pytest
from unittest.mock import Mock, patch, AsyncMock
from dbma.native.domain.agents.context_retriever_agent import ContextRetrieverAgent

@pytest.fixture
def context_retriever_agent():
    """Fixture for creating a ContextRetrieverAgent instance."""
    return ContextRetrieverAgent(name="Test Context Retriever", description="Test context retriever agent")

@pytest.mark.asyncio
async def test_execute(context_retriever_agent):
    """Test execute method."""
    # Setup
    input_data = {
        'query': 'Show me sales data for last month',
        'intent': 'query',
        'entities': ['sales', 'last month']
    }
    
    # Execute
    result = await context_retriever_agent.execute(input_data)
    
    # Assert
    assert isinstance(result, dict)
    assert 'conversation_history' in result
    assert 'relevant_tables' in result
    assert 'table_relationships' in result
    assert 'schema_info' in result

@pytest.mark.asyncio
async def test_validate_valid_result(context_retriever_agent):
    """Test validate method with valid result."""
    # Setup
    valid_result = {
        'conversation_history': [
            {'role': 'user', 'content': 'Show me sales data'}
        ],
        'relevant_tables': ['sales', 'products'],
        'table_relationships': {
            'sales': ['products', 'customers']
        },
        'schema_info': {
            'sales': {
                'columns': ['id', 'date', 'amount']
            }
        }
    }
    
    # Execute
    is_valid = await context_retriever_agent.validate(valid_result)
    
    # Assert
    assert is_valid is True

@pytest.mark.asyncio
async def test_validate_invalid_result(context_retriever_agent):
    """Test validate method with invalid result."""
    # Setup
    invalid_results = [
        {},  # Empty dict
        {'conversation_history': []},  # Missing fields
        {'relevant_tables': []},  # Missing fields
        {'table_relationships': {}},  # Missing fields
        {'schema_info': {}}  # Missing fields
    ]
    
    # Execute and Assert
    for result in invalid_results:
        is_valid = await context_retriever_agent.validate(result)
        assert is_valid is False

def test_get_name(context_retriever_agent):
    """Test get_name method."""
    assert context_retriever_agent.get_name() == "Test Context Retriever"

def test_get_description(context_retriever_agent):
    """Test get_description method."""
    assert context_retriever_agent.get_description() == "Test context retriever agent"

def test_get_state(context_retriever_agent):
    """Test get_state method."""
    state = context_retriever_agent.get_state()
    assert isinstance(state, dict)

def test_set_state(context_retriever_agent):
    """Test set_state method."""
    # Setup
    new_state = {
        'status': 'running',
        'last_execution': '2024-01-01T00:00:00'
    }
    
    # Execute
    context_retriever_agent.set_state(new_state)
    
    # Assert
    current_state = context_retriever_agent.get_state()
    assert current_state == new_state 