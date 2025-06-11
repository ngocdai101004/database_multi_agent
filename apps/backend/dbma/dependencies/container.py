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

def build_sql_generation_graph(llm_service: OpenAILLMService) -> CompiledGraph:
    return SQLGenerationGraph(llm_service=llm_service).get_sql_generation_graph()

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    llm_service = providers.Singleton(OpenAILLMService)
    context_service = providers.Singleton(ContextService)
    sql_database_service = providers.Singleton(SQLDatabaseService)
    postgres_database_service = providers.Singleton(PostgresDatabaseService)
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