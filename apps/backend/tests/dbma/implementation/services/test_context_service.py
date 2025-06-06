# import os
# import pytest
# from pathlib import Path
# from typing import Dict, Any

# from dbma.implementation.services.gemini_llm_service import GeminiLLMService
# from dbma.implementation.services.openai_llm_service import OpenAILLMService
# from dbma.implementation.services.context_service import ContextService, ContextOutput

# class TestContextService:
#     @pytest.fixture
#     def test_data_dir(self) -> Path:
#         return Path(__file__).parent / "test_data"

#     @pytest.fixture
#     def schema_descriptions(self, test_data_dir: Path) -> Dict[str, str]:
#         descriptions = {}
#         with open(test_data_dir / "schema_descriptions.txt", "r") as f:
#             current_schema = None
#             current_description = []
            
#             for line in f:
#                 if line.startswith("## "):
#                     if current_schema:
#                         descriptions[current_schema] = "\n".join(current_description)
#                     current_schema = line[3:].strip()
#                     current_description = []
#                 elif current_schema and line.strip():
#                     current_description.append(line.strip())
            
#             if current_schema:
#                 descriptions[current_schema] = "\n".join(current_description)
        
#         return descriptions

#     @pytest.fixture
#     def get_schema_tool(self, test_data_dir: Path):
#         def _get_schema(schema_name: str) -> str:
#             schema_file = test_data_dir / f"{schema_name}.txt"
#             if not schema_file.exists():
#                 raise ValueError(f"Schema {schema_name} not found")
            
#             with open(schema_file, "r") as f:
#                 return f.read()
        
#         return _get_schema

#     @pytest.fixture
#     def gemini_llm_service(self):
#         return GeminiLLMService()
    
#     @pytest.fixture
#     def openai_llm_service(self):
#         return OpenAILLMService()
    
#     @pytest.fixture
#     def context_service_gemini(self, gemini_llm_service: GeminiLLMService):
#         return ContextService(gemini_llm_service)
    
#     @pytest.fixture
#     def context_service_openai(self, openai_llm_service: OpenAILLMService):
#         return ContextService(openai_llm_service)
    
#     @pytest.mark.asyncio
#     async def test_analyze_context_gemini(
#         self, 
#         context_service_gemini: ContextService,
#         schema_descriptions: Dict[str, str],
#         get_schema_tool: Any
#     ):
#         query = "Top 3 customers has the most sales in Hanoi"
#         result: ContextOutput = await context_service_gemini.analyze_context(
#             query=query,
#             schema_info=schema_descriptions,
#             get_schema_tool=get_schema_tool
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
#         schema_descriptions: Dict[str, str],
#         get_schema_tool: Any
#     ):
#         query = "Top 3 customers has the most sales in Hanoi"
#         result = await context_service_openai.analyze_context(
#             query=query,
#             schema_info=schema_descriptions,
#             get_schema_tool=get_schema_tool
#         )
        
#         print("\nResult with OpenAI: ", result)
#         assert result is not None
#         assert isinstance(result, ContextOutput)
#         assert result.schema_description is not None
#         assert result.used_tables is not None
#         assert result.enrich_query is not None
#         assert result.schema_name is not None
