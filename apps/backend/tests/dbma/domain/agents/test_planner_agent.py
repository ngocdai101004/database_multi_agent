# import pytest
# from unittest.mock import Mock, patch, AsyncMock
# from dbma.native.domain.agents.planner_agent import PlannerAgent

# @pytest.fixture
# def planner_agent():
#     """Fixture for creating a PlannerAgent instance."""
#     return PlannerAgent(name="Test Planner", description="Test planner agent")

# @pytest.mark.asyncio
# async def test_execute(planner_agent):
#     """Test execute method."""
#     # Setup
#     input_data = {
#         'query': 'Show me sales data for last month',
#         'context': {'user_id': '123'}
#     }
    
#     # Execute
#     result = await planner_agent.execute(input_data)
    
#     # Assert
#     assert isinstance(result, dict)
#     assert 'detected_language' in result
#     assert 'intent_type' in result
#     assert 'entities' in result
#     assert 'complexity_score' in result

# @pytest.mark.asyncio
# async def test_validate_valid_result(planner_agent):
#     """Test validate method with valid result."""
#     # Setup
#     valid_result = {
#         'detected_language': 'en',
#         'intent_type': 'query',
#         'entities': ['sales', 'last month'],
#         'complexity_score': 0.5
#     }
    
#     # Execute
#     is_valid = await planner_agent.validate(valid_result)
    
#     # Assert
#     assert is_valid is True

# @pytest.mark.asyncio
# async def test_validate_invalid_result(planner_agent):
#     """Test validate method with invalid result."""
#     # Setup
#     invalid_results = [
#         {},  # Empty dict
#         {'detected_language': 'en'},  # Missing fields
#         {'intent_type': 'query'},  # Missing fields
#         {'entities': []},  # Missing fields
#         {'complexity_score': 0.5}  # Missing fields
#     ]
    
#     # Execute and Assert
#     for result in invalid_results:
#         is_valid = await planner_agent.validate(result)
#         assert is_valid is False

# def test_get_name(planner_agent):
#     """Test get_name method."""
#     assert planner_agent.get_name() == "Test Planner"

# def test_get_description(planner_agent):
#     """Test get_description method."""
#     assert planner_agent.get_description() == "Test planner agent"

# def test_get_state(planner_agent):
#     """Test get_state method."""
#     state = planner_agent.get_state()
#     assert isinstance(state, dict)

# def test_set_state(planner_agent):
#     """Test set_state method."""
#     # Setup
#     new_state = {
#         'status': 'running',
#         'last_execution': '2024-01-01T00:00:00'
#     }
    
#     # Execute
#     planner_agent.set_state(new_state)
    
#     # Assert
#     current_state = planner_agent.get_state()
#     assert current_state == new_state 