from typing import Any

from fastapi import APIRouter
from dbma.protocols.http.text2sql.controller import Text2SQLController
from dbma.protocols.models.sql_generation import Text2SQLRequest, Text2SQLResponse


class Text2SQLRouter(APIRouter):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.controller = Text2SQLController()
        self.add_api_route(
            "/text2sql",
            self.text2sql,
            methods=["POST"],
            status_code=200,
            tags=["Chat"],
            description="Text to SQL generation",
        )
        
    async def text2sql(
        self,
        request: Text2SQLRequest,
    ) -> Text2SQLResponse:
        return await self.controller.text2sql(
            request=request
        )