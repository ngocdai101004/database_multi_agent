import logging
from urllib.parse import quote_plus

import uvicorn
from dbma.dependencies.container import init_container
from dbma.protocols.http.text2sql.router import Text2SQLRouter
from fastapi import FastAPI


def config_logging(*args, **kwargs):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            "[%(asctime)s] %(module)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s"
        )
    )
    debug_modules = []

    root_logger.setLevel("INFO")
    root_logger.addHandler(handler)

    for debug_module in debug_modules:
        logger = logging.getLogger(debug_module)
        logger.setLevel(logging.DEBUG)
        logger.propagate = True

def create_app():
    app = FastAPI(
        title="SBF",
        description="SBF API",
        version="1.0.0",
        root_path="/api",
    )
    app.add_event_handler(event_type="startup", func=config_logging)
    app.add_event_handler(event_type="startup", func=init_container_object)
    app.include_router(Text2SQLRouter())
    return app

def init_container_object():
    container = init_container()
    container.llm_service()
    container.planner_service()
    container.context_service()
    container.sql_generation_graph()
    container.sql_generation_service()
    container.schema_storage_service()
    
    

if __name__ == "__main__":
    app = create_app()
    container = init_container()
    container.wire(modules=["dbma.native.controller.multi_agent_controller"])
    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)