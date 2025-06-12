import csv
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

from dbma.interface.services.schema_storage_service import \
    ISchemaStorageService
from dbma.native.domain.db_schema import DBSchema

# Add data directory to sys.path
sys.path.append(os.getcwd())

STORAGE_DIR = Path("D:/NgocDai/ViettelRecords/Miniproject/database_multi_agent/apps/backend/dbma/data/bird")
# STORAGE_DIR = Path(__file__).parent.parent.parent / "data" / "bird"
class SchemaStorageService(ISchemaStorageService):
    __storage_dir: Path
    db_description: Dict[str, str]
    list_schemas: List[str]
   
    def __init__(self, storage_dir: Path = STORAGE_DIR):
        self.__storage_dir = storage_dir
        self.db_description = {}
        self.list_schemas = []
        self._load_db_document()

    def _load_db_document(self):
        schema_description_file = self.__storage_dir / "schema_descriptions.txt"
        print("Schema description file: ", schema_description_file)
        if not schema_description_file.exists():
            raise FileNotFoundError("Schema descriptions file not found")
        
        with open(schema_description_file, "r") as f:
            line = f.readline()
            while line:
                if line.startswith("##"):
                    schema_name = line.strip().split("##")[1].strip()
                    self.list_schemas.append(schema_name)
                else:
                    self.db_description[schema_name] = line.strip()
                line = f.readline()
            
    def get_schema(self, schema_name: str) -> DBSchema:
        if schema_name not in self.list_schemas:
            raise ValueError(f"Schema {schema_name} is not valid")
            
        schema_file = self.__storage_dir / "schemas" / f"{schema_name}.txt"
        if not schema_file.exists():
            raise FileNotFoundError(f"Schema file for {schema_name} not found")
        
        with open(schema_file, "r") as f:
            schema_detail = f.read()
            
        # Extract table names from CREATE TABLE statements
        table_names = []
        create_table_pattern = r"CREATE TABLE/s+(/w+)"
        matches = re.finditer(create_table_pattern, schema_detail, re.IGNORECASE)
        for match in matches:
            table_names.append(match.group(1))
            
        return DBSchema(
            schema_name=schema_name,
            schema_description=self.db_description[schema_name],
            schema_tables=table_names,
            schema_detail=schema_detail,
            table_description=self.get_table_description(schema_name)
        )
    
    def get_table_description(self, schema_name: str) -> str:
        table_description = ""
        description_dir = self.__storage_dir / "dev_databases" / schema_name / "database_description"
        list_of_files = os.listdir(description_dir)

        for file in list_of_files:
            file_path = description_dir / file
            with open(file_path, mode="r", encoding="utf-8") as f:
                reader = csv.reader(f)
                table_description += f"Table: {file.split('.')[0]}\n"
                for row in reader:
                    if len(row) >= 5:
                        table_description += f"Column Name: {row[1]}\n"
                        table_description += f"Column Description: {row[2]}\n"
                        table_description += f"Data Format: {row[3]}\n"
                        table_description += f"Value Description: {row[4]}\n"
                        table_description += "\n"
        return table_description
    
    def get_db_description(self) -> str:
        return str(self.db_description)

    def query_db(self, query: str) -> str:
        pass