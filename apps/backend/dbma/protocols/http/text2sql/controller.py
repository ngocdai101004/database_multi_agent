import logging
import time
import uuid
from typing import Any, Optional, Tuple

from dbma.dependencies.container import Container
from dbma.native.controller.multi_agent_controller import MultiAgentController
from dbma.native.domain.agent_models import SQLGeneratorAgentResponse
from dbma.native.domain.message import Message
from dbma.protocols.models.sql_generation import (Text2SQLRequest,
                                                  Text2SQLResponse)
from dependency_injector.wiring import Provide, inject
from fastapi import Request

logger = logging.getLogger("sbf")

class Text2SQLController:
    def __init__(self):
        self.native_controller = MultiAgentController()
    
    async def text2sql(
        self,
        request: Text2SQLRequest,
    ) -> Text2SQLResponse:
        start_time = time.time()
        logger.info(f"Text2SQL request received for query {request.query}")
        response: SQLGeneratorAgentResponse=  await self.native_controller.process_query(
            query=request.query,
        )
        logger.info(f"Text2SQL response received for query {request.query} in {time.time() - start_time} seconds")
        print(response)
        return Text2SQLResponse(
            sql_query=request.query,
            sql_candidates=response.sql_candidates,
            sql_candidates_confidence_scores=response.sql_candidates_confidence_scores,
            selected_sql=response.selected_sql,
            confidence_score=response.confidence_score
        )