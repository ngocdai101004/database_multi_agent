from enum import Enum
from typing import Any, Dict, List, Optional

from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.interface.services.planner_service import IPlannerService
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser

instructions_prompt = """
You are a helpful assistant with knowledge of the database and data analytics.
From the user requirements, you need to plan the query execution
Define the insights that you will extract from the database.
You have to:
- Detect the language of the user query (English (EN), Vietnamese (VN))
- Classify the intent of the user query (Report, Statistic, Analysis, Filter)
- Extract the entities from the user query, that need to be retrieved from the database
- Estimate the complexity of the query, if only select, from, where basic task, or if it involves joins, group by, order by, etc. (from 0 to 10, with 0 being the easiest and 10 being the hardest)
"""
class IntentType(Enum):
    REPORT = "Report"
    STATISTIC = "Statistic"
    ANALYSIS = "Analysis"
    FILTER = "Filter"

class LanguageType(Enum):
    ENGLISH = "EN"
    VIETNAMESE = "VN"

class PlannerOutput(BaseModel):
    detected_language: LanguageType
    intent_type: IntentType
    entities: List[str]
    complexity_score: int

class PlannerService(IPlannerService):

    def __init__(self, llm_service: OpenAILLMService):
        self.llm_service = llm_service
        self.parser = PydanticOutputParser(pydantic_object=PlannerOutput)

    async def plan(self, query: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        # TODO: Implement language detection
        # TODO: Implement intent classification
        # TODO: Implement entity extraction
        # TODO: Implement complexity estimation

        format_instructions = self.parser.get_format_instructions()
        full_prompt = instructions_prompt + "\n\n" + format_instructions
        messages = [
            SystemMessage(content=full_prompt),
            HumanMessage(content=query)
        ]

        chain = self.llm_service.llm | self.parser
        result = await chain.ainvoke(messages)
        return result

    async def get_usage_metrics(self) -> Dict[str, Any]:
        return self.llm_service.get_usage_metrics()