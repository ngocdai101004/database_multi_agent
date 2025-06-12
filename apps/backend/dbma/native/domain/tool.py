from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict

from dbma.interface.services.schema_storage_service import \
    ISchemaStorageService
from dbma.native.domain.db_schema import DBSchema


class Tool:
    pass

    
class SchemaTool(Tool):
    schema_storage_service: ISchemaStorageService
    
    def __init__(self, schema_storage_service: ISchemaStorageService):
        self.schema_storage_service = schema_storage_service
    
    def get_schema(self, schema_name: str) -> DBSchema:
        return self.schema_storage_service.get_schema(schema_name)
    
    def get_db_description(self) -> str:
        return self.schema_storage_service.get_db_description()
    
    def query_db(self, query: str) -> str:
        return self.schema_storage_service.query_db(query)