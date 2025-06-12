from typing import Optional

from dependency_injector import containers, providers

from dotenv import load_dotenv

__container: Optional["Container"] = None

load_dotenv()

from dbma.implementation.services.sql_generation_graph import SQLGenerationGraph
from dbma.implementation.services.sql_generation_service import SQLGenerationService
from dbma.implementation.services.context_service import ContextService
from dbma.implementation.services.openai_llm_service import OpenAILLMService
from dbma.implementation.services.sql_database_service import SQLDatabaseService
from dbma.implementation.services.postgres_database_service import PostgresDatabaseService
from langgraph.graph.graph import CompiledGraph
from dbma.implementation.services.schema_storage_service import SchemaStorageService
from pathlib import Path
from dbma.implementation.services.planner_service import PlannerService

def build_sql_generation_graph(llm_service: OpenAILLMService) -> CompiledGraph:
    return SQLGenerationGraph(llm_service=llm_service).get_sql_generation_graph()

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    llm_service = providers.Singleton(OpenAILLMService)
    planner_service = providers.Singleton(PlannerService, llm_service=llm_service)
    schema_storage_service = providers.Singleton(SchemaStorageService)
    context_service = providers.Singleton(ContextService, llm_service=llm_service, schema_storage_service=schema_storage_service)
    sql_generation_graph = providers.Singleton(build_sql_generation_graph, llm_service=llm_service)
    sql_generation_service = providers.Singleton(SQLGenerationService, graph=sql_generation_graph)
    
   
def init_container() -> Container:
    global __container

    if __container:
        return __container
    else:
        container = Container()
        __container = container
        return container