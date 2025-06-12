from pydantic import BaseModel
from typing import List, Optional


class Text2SQLRequest(BaseModel):
    query: str
    
class Text2SQLResponse(BaseModel):
    sql_query: str
    sql_candidates: Optional[List[str]]
    sql_candidates_confidence_scores: Optional[List[float]]
    selected_sql: Optional[str]
    confidence_score: Optional[float]