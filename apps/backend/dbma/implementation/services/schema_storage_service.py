from dbma.interface.services.schema_storage_service import ISchemaStorageService
from pathlib import Path
from dbma.native.domain.db_schema import DBSchema
from typing import Dict, List
import re

class SchemaStorageService(ISchemaStorageService):
    __storage_dir: Path
    db_description: Dict[str, str]
    list_schemas: List[str]
   
    def __init__(self, storage_dir: Path):
        self.__storage_dir = storage_dir
        self.db_description = {}
        self.list_schemas = []
        self._load_db_document()

    def _load_db_document(self):
        schema_description_file = self.__storage_dir / "schema_descriptions.txt"
        if not schema_description_file.exists():
            raise FileNotFoundError("Schema descriptions file not found")
        
        with open(schema_description_file, "r") as f:
            content = f.read()
            
        # Split content by schema sections
        schema_sections = content.split("## ")
        
        for section in schema_sections[1:]:  # Skip first empty split
            lines = section.strip().split("\n")
            schema_name = lines[0].strip()
            description = "\n".join(lines[1:]).strip()
            
            self.db_description[schema_name] = description
            self.list_schemas.append(schema_name)
            
    def get_schema(self, schema_name: str) -> DBSchema:
        if schema_name not in self.list_schemas:
            raise ValueError(f"Schema {schema_name} is not valid")
            
        schema_file = self.__storage_dir / f"{schema_name}_schema.txt"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file for {schema_name} not found")
        
        with open(schema_file, "r") as f:
            schema_detail = f.read()
            
        # Extract table names from CREATE TABLE statements
        table_names = []
        create_table_pattern = r"CREATE TABLE\s+(\w+)"
        matches = re.finditer(create_table_pattern, schema_detail, re.IGNORECASE)
        for match in matches:
            table_names.append(match.group(1))
            
        return DBSchema(
            schema_name=schema_name,
            schema_description=self.db_description[schema_name],
            schema_tables=table_names,
            schema_detail=schema_detail
        )
    
    def get_db_description(self) -> str:
        return str(self.db_description)

    def query_db(self, query: str) -> str:
        pass