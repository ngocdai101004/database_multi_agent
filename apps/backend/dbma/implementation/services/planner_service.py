from enum import Enum
from typing import Any, Dict, List, Optional
from datetime import datetime

from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.interface.services.planner_service import IPlannerService
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from dbma.native.domain.enum.sender_type import SenderType
from dbma.native.domain.message import Message
from dbma.implementation.utils import convert_message_to_langchain_message

instructions_prompt = """
You are a helpful assistant with knowledge of the database and data analytics.
From the user requirements and chat history, you need to plan the query execution and rewrite the query to be more specific.

You have to:
1. Analyze the chat history to understand the context and user's intent
2. Rewrite the latest query to be more specific and clear, incorporating relevant context from previous messages
3. Detect the language of the rewritten query (English (EN), Vietnamese (VN))
4. Classify the intent of the rewritten query (Report, Statistic, Analysis, Filter)
5. Extract the entities from the rewritten query that need to be retrieved from the database
6. Estimate the complexity of the query (from 0 to 10, with 0 being the easiest and 10 being the hardest)

When rewriting the query:
- Focus on the most recent user messages as they are most relevant
- Include any important context from previous messages
- Make the query more specific and clear
- Maintain the original intent while adding necessary details
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
    rewritten_query: str

class PlannerService(IPlannerService):
    def __init__(self, llm_service: OpenAILLMService):
        self.llm_service = llm_service
        self.parser = PydanticOutputParser(pydantic_object=PlannerOutput)

    async def plan(
        self, 
        input_message: Message,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        format_instructions = self.parser.get_format_instructions()
        full_prompt = instructions_prompt + "\n\n" + format_instructions

        # Prepare chat history for the LLM
        chat_history = []
        if context and "history" in context:
            for message in context["history"]:
                chat_history.append(convert_message_to_langchain_message(message))

        messages = [
            SystemMessage(content=full_prompt),
            *chat_history,
            convert_message_to_langchain_message(input_message)
        ]

        chain = self.llm_service.llm | self.parser
        result = await chain.ainvoke(messages)
        return result