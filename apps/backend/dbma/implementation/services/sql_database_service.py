import sqlite3
import tempfile
from pathlib import Path
from typing import Any

from dbma.interface.services.llm_service import ILLMService
from dbma.interface.services.sql_database_service import ISQLDatabaseService
from langchain.tools import BaseTool
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase

DATADIR = Path(__file__).parent.parent.parent / "data" / "bird" / "dev_databases"


class SQLDatabaseService(ISQLDatabaseService):
    def __init__(self, schema_name: str, llm_service: ILLMService):
        self.__db_path = DATADIR / schema_name / f"{schema_name}.sqlite"

        # Tạo kết nối từ file gốc
        original_conn = sqlite3.connect(str(self.__db_path))

        # Tạo kết nối in-memory
        memory_conn = sqlite3.connect(":memory:")
        original_conn.backup(memory_conn)
        original_conn.close()

        # Tạo file tạm để giữ lại dữ liệu cho LangChain
        self._temp_file = tempfile.NamedTemporaryFile(suffix=".sqlite", delete=False)
        disk_conn = sqlite3.connect(self._temp_file.name)
        memory_conn.backup(disk_conn)
        memory_conn.close()
        disk_conn.close()

        # Tạo SQLDatabase từ file tạm
        self.db = SQLDatabase.from_uri(f"sqlite:///{self._temp_file.name}")
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm_service.llm)

        print(f"[INFO] In-memory DB created from: {self.__db_path.name} -> Temp file: {self._temp_file.name}")

    def __del__(self):
        """Ensure temp file is deleted when object is destroyed."""
        try:
            if hasattr(self.db, "engine"):
                self.db.engine.dispose()  # Giải phóng file trước
            self._temp_file.close()
            Path(self._temp_file.name).unlink(missing_ok=True)
            print(f"[INFO] Temp DB file deleted: {self._temp_file.name}")
        except Exception as e:
            print(f"[WARN] Failed to delete temp file: {e}")


    def get_query_tool(self) -> BaseTool:
        return self.toolkit.get_tools()[0]

    def get_schema_info_tool(self) -> BaseTool:
        return self.toolkit.get_tools()[1]

    def get_list_tables_tool(self) -> BaseTool:
        return self.toolkit.get_tools()[2]

    def get_query_checker_tool(self) -> BaseTool:
        return self.toolkit.get_tools()[3]

    def execute_query(self, query: str) -> Any:
        try:
            return self.db.run(query)
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")

    def validate_query(self, query: str) -> bool:
        try:
            self.db.run(query)
            return True
        except Exception:
            return False
