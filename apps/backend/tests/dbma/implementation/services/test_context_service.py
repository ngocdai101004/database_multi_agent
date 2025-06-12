import os
from pathlib import Path
from typing import Any, Dict

import pytest
from dbma.dependencies.container import Container
from dbma.implementation.services.context_service import (ContextOutput,
                                                          ContextService)
from dbma.implementation.services.gemini_llm_service import GeminiLLMService
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.implementation.services.schema_storage_service import \
    SchemaStorageService
from dbma.native.domain.agent_models import (ContextAgentInput,
                                             ContextAgentResponse)


class TestContextService:
    @pytest.fixture
    def schema_storage_service(self):
        return SchemaStorageService()

    @pytest.fixture
    def gemini_llm_service(self):
        return GeminiLLMService()
    
    @pytest.fixture
    def openai_llm_service(self):
        return OpenAILLMService()
    
    @pytest.fixture
    def context_service_gemini(self, gemini_llm_service: GeminiLLMService, schema_storage_service: SchemaStorageService):
        return ContextService(gemini_llm_service, schema_storage_service)
    
    @pytest.fixture
    def context_service_openai(self, openai_llm_service: OpenAILLMService, schema_storage_service: SchemaStorageService):
        return ContextService(openai_llm_service, schema_storage_service)
    
    

    
    @pytest.mark.asyncio
    async def test_analyze_context_gemini(
        self, 
        context_service_gemini: ContextService,
    ):
        query = "Please list the zip code of all the charter schools in Fresno County Office of Education."
        input_data = ContextAgentInput(query=query)
        result: ContextAgentResponse = await context_service_gemini.analyze_context(
            input_data=input_data,
        )

        print("\nResult with Gemini: ", result)
        print("Type of result: ", type(result))
        assert result is not None
        assert isinstance(result, ContextAgentResponse)
        assert result.schema_description is not None
        assert result.used_tables is not None
        assert result.enrich_query is not None
        assert result.schema_name is not None

    @pytest.mark.asyncio
    async def test_analyze_context_openai(
        self, 
        context_service_openai: ContextService,
    ):
        query = "Please list the zip code of all the charter schools in Fresno County Office of Education."
        input_data = ContextAgentInput(query=query)
        result = await context_service_openai.analyze_context(
            input_data=input_data,
        )
        
        print("\nResult with OpenAI: ", result)
        assert result is not None
        assert isinstance(result, ContextAgentResponse)
        assert result.schema_description is not None
        assert result.used_tables is not None
        assert result.enrich_query is not None
        assert result.schema_name is not None
    
    @pytest.fixture
    def context_service(self, container: Container):
        return container.context_service()

    @pytest.mark.asyncio
    async def test_context_service(self, context_service: ContextService):
        # Arrange
        query = "Please list the zip code of all the charter schools in Fresno County Office of Education."
        input_data = ContextAgentInput(query=query)
        # Act
        result = await context_service.analyze_context(input_data=input_data)
        print("\nResult with Container Context Service: ", result)
        
        # Assert
        assert result is not None
        assert isinstance(result, ContextAgentResponse)
        assert result.schema_description is not None
        assert result.used_tables is not None