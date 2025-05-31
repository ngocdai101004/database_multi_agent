import pytest
from unittest.mock import Mock, patch, AsyncMock
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from dbma.implementation.services.openai_llm_service import OpenAILLMService

@pytest.fixture
def mock_llm():
    """Fixture for mocking the ChatOpenAI instance."""
    with patch('dbma.implementation.services.openai_llm_service.ChatOpenAI') as mock:
        mock_instance = Mock()
        mock_instance.agenerate = AsyncMock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def llm_service(mock_llm):
    """Fixture for creating an OpenAILLMService instance."""
    return OpenAILLMService(api_key="test_key", model="gpt-4")

@pytest.mark.asyncio
async def test_generate_text(llm_service, mock_llm):
    """Test text generation functionality."""
    # Setup
    test_prompt = "Test prompt"
    expected_response = "Generated response"
    mock_llm.agenerate.return_value.generations = [[Mock(text=expected_response)]]
    
    # Execute
    result = await llm_service.generate_text(test_prompt)
    
    # Assert
    assert result == expected_response
    mock_llm.agenerate.assert_called_once()
    messages = mock_llm.agenerate.call_args[0][0][0]
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == test_prompt

@pytest.mark.asyncio
async def test_classify_intent(llm_service, mock_llm):
    """Test intent classification functionality."""
    # Setup
    test_text = "I want to query the database"
    expected_result = {
        'intent': 'query',
        'confidence': 0.95,
        'categories': ['database', 'query']
    }
    mock_llm.agenerate.return_value.generations = [[Mock(text=str(expected_result))]]
    
    # Execute
    result = await llm_service.classify_intent(test_text)
    
    # Assert
    assert result == expected_result
    mock_llm.agenerate.assert_called_once()
    messages = mock_llm.agenerate.call_args[0][0][0]
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == test_text

@pytest.mark.asyncio
async def test_extract_entities(llm_service, mock_llm):
    """Test entity extraction functionality."""
    # Setup
    test_text = "Find sales data for New York in 2023"
    expected_entities = [
        {'text': 'sales', 'type': 'metric', 'start': 5, 'end': 10},
        {'text': 'New York', 'type': 'location', 'start': 20, 'end': 29},
        {'text': '2023', 'type': 'date', 'start': 33, 'end': 37}
    ]
    mock_llm.agenerate.return_value.generations = [[Mock(text=str(expected_entities))]]
    
    # Execute
    result = await llm_service.extract_entities(test_text)
    
    # Assert
    assert result == expected_entities
    mock_llm.agenerate.assert_called_once()
    messages = mock_llm.agenerate.call_args[0][0][0]
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == test_text

@pytest.mark.asyncio
async def test_translate_text(llm_service, mock_llm):
    """Test text translation functionality."""
    # Setup
    test_text = "Hello world"
    target_language = "Spanish"
    expected_translation = "Hola mundo"
    mock_llm.agenerate.return_value.generations = [[Mock(text=expected_translation)]]
    
    # Execute
    result = await llm_service.translate_text(test_text, target_language)
    
    # Assert
    assert result == expected_translation
    mock_llm.agenerate.assert_called_once()
    messages = mock_llm.agenerate.call_args[0][0][0]
    assert isinstance(messages[0], SystemMessage)
    assert isinstance(messages[1], HumanMessage)
    assert messages[1].content == test_text
    assert target_language in messages[0].content

@pytest.mark.asyncio
async def test_get_usage_metrics(llm_service):
    """Test usage metrics functionality."""
    # Execute
    metrics = await llm_service.get_usage_metrics()
    
    # Assert
    assert isinstance(metrics, dict)
    assert 'total_tokens' in metrics
    assert 'total_requests' in metrics
    assert 'last_reset' in metrics
    assert 'quota_remaining' in metrics
    assert metrics['total_tokens'] == 0
    assert metrics['total_requests'] == 0

@pytest.mark.asyncio
async def test_error_handling(llm_service, mock_llm):
    """Test error handling in the service."""
    # Setup
    mock_llm.agenerate.side_effect = Exception("API Error")
    
    # Execute and Assert
    with pytest.raises(Exception) as exc_info:
        await llm_service.generate_text("test")
    assert str(exc_info.value) == "API Error"

@pytest.mark.asyncio
async def test_parameters_handling(llm_service, mock_llm):
    """Test handling of generation parameters."""
    # Setup
    test_prompt = "Test prompt"
    parameters = {
        'temperature': 0.7,
        'max_tokens': 100,
        'top_p': 0.9
    }
    mock_llm.agenerate.return_value.generations = [[Mock(text="Response")]]
    
    # Execute
    await llm_service.generate_text(test_prompt, parameters)
    
    # Assert
    assert llm_service.llm.temperature == 0.7
    assert llm_service.llm.max_tokens == 100
    assert llm_service.llm.top_p == 0.9 