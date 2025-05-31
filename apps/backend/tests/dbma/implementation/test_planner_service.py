import pytest
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.implementation.services.planner_service import PlannerService

class TestPlannerService:
    @pytest.fixture
    def llm_service(self):
        return OpenAILLMService()
    
    @pytest.fixture
    def planner_service(self, llm_service):
        return PlannerService(llm_service)
    
    @pytest.mark.asyncio
    async def test_plan(self, planner_service: PlannerService):
        query = "Give me the list of customers in Hanoi"
        result = await planner_service.plan(query)
        print("Result: ", result)
        assert result is not None
    
    @pytest.mark.asyncio
    async def test_get_usage_metrics(self, planner_service: PlannerService):
        metrics = await planner_service.get_usage_metrics()
        print("Metrics: ", metrics)
        assert metrics is not None
    
