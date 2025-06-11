import os
import sys
import pytest_asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dbma.dependencies.container import Container

@pytest_asyncio.fixture(scope="function")
async def container():
    container = Container()
    
    yield container
    shutdown = container.shutdown_resources()

    if shutdown:
        await shutdown 