# import os
# import pytest
# from pathlib import Path
# from typing import Dict, Any

# from dbma.implementation.services.gemini_llm_service import GeminiLLMService
# from dbma.implementation.services.openai_llm_service import OpenAILLMService
# from dbma.implementation.services.context_service import ContextService, ContextOutput
# from dbma.implementation.services.schema_storage_service import SchemaStorageService

# class TestContextService:
#     @pytest.fixture
#     def test_data_dir(self) -> Path:
#         return Path(__file__).parent / "test_data"

#     @pytest.fixture
#     def schema_storage_service(self, test_data_dir: Path):
#         return SchemaStorageService(test_data_dir)

#     @pytest.fixture
#     def gemini_llm_service(self):
#         return GeminiLLMService()
    
#     @pytest.fixture
#     def openai_llm_service(self):
#         return OpenAILLMService()
    
#     @pytest.fixture
#     def context_service_gemini(self, gemini_llm_service: GeminiLLMService, schema_storage_service: SchemaStorageService):
#         return ContextService(gemini_llm_service, schema_storage_service)
    
#     @pytest.fixture
#     def context_service_openai(self, openai_llm_service: OpenAILLMService, schema_storage_service: SchemaStorageService):
#         return ContextService(openai_llm_service, schema_storage_service)
    
#     @pytest.mark.asyncio
#     async def test_analyze_context_gemini(
#         self, 
#         context_service_gemini: ContextService,
#     ):
#         query = "List all products and their average stock quantity in each warehouse where the average stock is below the product's reorder point. Include the product name, warehouse name, and reorder point, and sort the results by average stock quantity in ascending order"
#         result: ContextOutput = await context_service_gemini.analyze_context(
#             query=query,
#         )

#         print("\nResult with Gemini: ", result)
#         print("Type of result: ", type(result))
#         assert result is not None
#         assert isinstance(result, ContextOutput)
#         assert result.schema_description is not None
#         assert result.used_tables is not None
#         assert result.enrich_query is not None
#         assert result.schema_name is not None

#     @pytest.mark.asyncio
#     async def test_analyze_context_openai(
#         self, 
#         context_service_openai: ContextService,
#     ):
#         query = "List all products and their average stock quantity in each warehouse where the average stock is below the product's reorder point. Include the product name, warehouse name, and reorder point, and sort the results by average stock quantity in ascending order"
#         result = await context_service_openai.analyze_context(
#             query=query,
#         )
        
#         print("\nResult with OpenAI: ", result)
#         assert result is not None
#         assert isinstance(result, ContextOutput)
#         assert result.schema_description is not None
#         assert result.used_tables is not None
#         assert result.enrich_query is not None
#         assert result.schema_name is not None
