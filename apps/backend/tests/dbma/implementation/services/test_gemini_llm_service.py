# from unittest.mock import AsyncMock, Mock, patch

# import pytest
# from dbma.implementation.services.gemini_llm_service import GeminiLLMService
# from langchain_core.messages import (AIMessage, BaseMessage, HumanMessage,
#                                      SystemMessage)


# class TestGeminiLLMService:
#     @pytest.fixture
#     def llm_service(self):
#         return GeminiLLMService()
    
#     @pytest.mark.asyncio
#     async def test_ainvoke(self, llm_service: GeminiLLMService):
#         messages = [
#             SystemMessage(content="You are a helpful assistant."),
#             HumanMessage(content="What is the capital of Vietnam")
#         ]
#         response = await llm_service.ainvoke(messages)
#         print("Response: ", response)
#         assert response is not None
        
#     @pytest.mark.asyncio
#     async def test_get_usage_metrics(self, llm_service: GeminiLLMService):
#         metrics = llm_service.get_usage_metrics()
#         print("Metrics: ", metrics)
#         assert metrics is not None