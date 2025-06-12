from abc import ABC, abstractmethod
from typing import Any, Dict

from dbma.native.domain.db_schema import DBSchema


class ISchemaStorageService(ABC):
    @abstractmethod
    def get_schema(self, schema_name: str) -> DBSchema:
        pass
    
    @abstractmethod
    def get_db_description(self) -> str:
        pass
    
    @abstractmethod
    def query_db(self, query: str) -> str:
        pass