from pathlib import Path
from typing import List, Dict, Any
from langchain.tools import BaseTool
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from dbma.interface.services.sql_database_service import ISQLDatabaseService
from langchain_core.language_models import BaseChatModel
from dbma.interface.services.llm_service import ILLMService

DATADIR = Path(__file__).parent.parent.parent / "data" / "spider_data" / "database"

class SQLDatabaseService(ISQLDatabaseService):
    def __init__(self, schema_name: str, llm_service: ILLMService):
        """
        Initialize SQL database service
        
        Args:
            schema_name: Name of the schema to use
            llm_service: Language model service for generating SQL queries
        """
        self.__db_path = DATADIR / schema_name / f"{schema_name}.sqlite"
        print(self.__db_path)
        self.db: SQLDatabase = SQLDatabase.from_uri(f"sqlite:///{self.__db_path}")
        self.toolkit = SQLDatabaseToolkit(db=self.db, llm=llm_service.llm)
    
    def get_query_tool(self) -> BaseTool:
        """Get the tool for executing SQL queries"""
        return self.toolkit.get_tools()[0]  # query_sql_database_tool
    
    def get_schema_info_tool(self) -> BaseTool:
        """Get the tool for retrieving schema information"""
        return self.toolkit.get_tools()[1]  # info_sql_database_tool
    
    def get_list_tables_tool(self) -> BaseTool:
        """Get the tool for listing tables"""
        return self.toolkit.get_tools()[2]  # list_sql_database_tool
    
    def get_query_checker_tool(self) -> BaseTool:
        """Get the tool for checking SQL queries"""
        return self.toolkit.get_tools()[3]  # query_sql_database_tool
    
    def execute_query(self, query: str) -> Any:
        """Execute a SQL query and return results"""
        try:
            return self.db.run(query)
        except Exception as e:
            raise Exception(f"Error executing query: {str(e)}")
    
    def validate_query(self, query: str) -> bool:
        """Validate if a SQL query is valid"""
        try:
            self.db.run(query)
            return True
        except Exception:
            return False 