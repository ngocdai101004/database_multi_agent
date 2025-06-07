from typing import List
from pathlib import Path

class DBSchema:
    schema_name: str
    schema_description: str
    schema_tables: List[str]
    schema_detail: str
    def __init__(self, schema_name: str, schema_description: str, schema_tables: List[str], schema_detail: str):
        self.schema_name = schema_name
        self.schema_description = schema_description
        self.schema_tables = schema_tables
        self.schema_detail = schema_detail
        

    def __repr__(self):
        return f"DBSchema(schema_name={self.schema_name}, schema_description={self.schema_description}, schema_tables={self.schema_tables}, schema_detail={self.schema_detail})"