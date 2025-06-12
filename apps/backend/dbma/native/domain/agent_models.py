import uuid
from datetime import datetime
from typing import Any, Dict, List

from dbma.native.domain.enum.intent_type import IntentType
from dbma.native.domain.enum.language_type import LanguageType
from dbma.native.domain.enum.sender_type import SenderType
from dbma.native.domain.message import Message


class AgentResponse:
    pass

class AgentInput:
    pass

class PlannerAgentInput(AgentInput):
    query: Message | str
    context: Dict[str, Any]
    
    def __init__(self, query: Message | str, context: Dict[str, Any]):
        if isinstance(query, str):
            self.query = Message(
                id=str(uuid.uuid4()),
                content=query, 
                sender_type=SenderType.USER, 
                created_at=datetime.now(), 
                created_by="user",
            )
        else:
            self.query = query
            
        self.context = context
        
class ContextAgentInput(AgentInput):
    query: str
    def __init__(self, query: str):
        self.query = query
        

class SQLGeneratorAgentInput(AgentInput):
    query: str
    schema_name: str
    schema_description: str
    used_tables: List[str]
    
    def __init__(self, query: str, schema_name: str, schema_description: str, used_tables: List[str]):
        self.query = query
        self.schema_name = schema_name
        self.schema_description = schema_description
        self.used_tables = used_tables

class PlannerAgentResponse(AgentResponse):
    detected_language: LanguageType
    intent_type: IntentType
    entities: List[str]
    complexity_score: int
    rewritten_query: str
    
    def __init__(self, detected_language: LanguageType, intent_type: IntentType, entities: List[str], complexity_score: int, rewritten_query: str):
        self.detected_language = detected_language
        self.intent_type = intent_type
        self.entities = entities
        self.complexity_score = complexity_score
        self.rewritten_query = rewritten_query
           
class ContextAgentResponse(AgentResponse):
    schema_name: str
    schema_description: str
    used_tables: List[str]
    enrich_query: str
    
    def __init__(self, schema_name: str, schema_description: str, used_tables: List[str], enrich_query: str):
        self.schema_name = schema_name
        self.schema_description = schema_description
        self.used_tables = used_tables
        self.enrich_query = enrich_query
        
class SQLGeneratorAgentResponse(AgentResponse):
    sql_query: str
    sql_candidates: List[str]
    sql_candidates_confidence_scores: List[float]
    selected_sql: str
    confidence_score: float
    
    def __init__(self, sql_query: str, sql_candidates: List[str], sql_candidates_confidence_scores: List[float], selected_sql: str, confidence_score: float):
        self.sql_query = sql_query
        self.sql_candidates = sql_candidates
        self.sql_candidates_confidence_scores = sql_candidates_confidence_scores
        self.selected_sql = selected_sql
        self.confidence_score = confidence_score
    
class MultiAgentResponse(AgentResponse):
    sql_query: str
    sql_candidates: List[str]
    sql_candidates_confidence_scores: List[float]
    selected_sql: str
    confidence_score: float
    
    def __init__(self, sql_query: str, sql_candidates: List[str], sql_candidates_confidence_scores: List[float], selected_sql: str, confidence_score: float):
        self.sql_query = sql_query
        self.sql_candidates = sql_candidates
        self.sql_candidates_confidence_scores = sql_candidates_confidence_scores
        self.selected_sql = selected_sql
        self.confidence_score = confidence_score