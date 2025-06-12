from datetime import datetime
from typing import List

import pytest
from dbma.implementation.services.gemini_llm_service import GeminiLLMService
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.implementation.services.planner_service import (PlannerOutput,
                                                          PlannerService)
from dbma.native.domain.agent_models import (PlannerAgentInput,
                                             PlannerAgentResponse)
from dbma.native.domain.enum.sender_type import SenderType
from dbma.native.domain.message import Message


class TestPlannerService:
    @pytest.fixture
    def gemini_llm_service(self):
        return GeminiLLMService()
    
    @pytest.fixture
    def openai_llm_service(self):
        return OpenAILLMService()
    
    @pytest.fixture
    def planner_service_gemini(self, gemini_llm_service: GeminiLLMService):
        return PlannerService(gemini_llm_service)
    
    @pytest.fixture
    def planner_service_openai(self, openai_llm_service: OpenAILLMService):
        return PlannerService(openai_llm_service)

    @pytest.fixture
    def sample_chat_history(self) -> List[Message]:
        return [
            Message(
                id="1",
                content="I want to see sales data",
                created_by="user1",
                sender_type=SenderType.USER,
                created_at=datetime.now()
            ),
            Message(
                id="2",
                content="Which region's sales data would you like to see?",
                created_by="agent1",
                sender_type=SenderType.AGENT,
                created_at=datetime.now()
            ),
            Message(
                id="3",
                content="Hanoi region",
                created_by="user1",
                sender_type=SenderType.USER,
                created_at=datetime.now()
            )
        ]
    
    @pytest.mark.asyncio
    async def test_plan_gemini(
        self, 
        planner_service_gemini: PlannerService,
        sample_chat_history: List[Message]
    ):
        input_message = Message(
            id="4",
            content="Show me the total sales for the last quarter",
            created_by="user1",
            sender_type=SenderType.USER,
            created_at=datetime.now()
        )
        
        context = {"history": sample_chat_history}
        input_data = PlannerAgentInput(query=input_message, context=context)
        result : PlannerAgentResponse = await planner_service_gemini.plan(input_data=input_data)
        
        print("\nResult with Gemini: ", result)
        print("Type of result with Gemini: ", type(result))
        assert result is not None
        assert isinstance(result, PlannerAgentResponse)
        assert result.detected_language is not None
        assert result.intent_type is not None
        assert result.entities is not None
        assert result.complexity_score is not None
        assert result.rewritten_query is not None
        assert isinstance(result.entities, list)
        
    @pytest.mark.asyncio
    async def test_plan_openai(
        self, 
        planner_service_openai: PlannerService,
        sample_chat_history: List[Message]
    ):
        input_message = Message(
            id="4",
            content="Show me the total sales for the last quarter",
            created_by="user1",
            sender_type=SenderType.USER,
            created_at=datetime.now()
        )
        
        context = {"history": sample_chat_history}
        input_data = PlannerAgentInput(query=input_message, context=context)
        result : PlannerAgentResponse = await planner_service_openai.plan(input_data=input_data)
        
        print("\nResult with OpenAI: ", result)
        print("Type of result with OpenAI: ", type(result))
        assert result is not None
        assert isinstance(result, PlannerAgentResponse)
        assert result.detected_language is not None
        assert result.intent_type is not None
        assert result.entities is not None
        assert result.complexity_score is not None
        assert result.rewritten_query is not None
        assert isinstance(result.entities, list)
   