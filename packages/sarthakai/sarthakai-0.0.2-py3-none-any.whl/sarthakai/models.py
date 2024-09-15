from pydantic import BaseModel
from typing import List, Dict, Union
from datetime import datetime


class Chunk(BaseModel):
    text: str
    embedding: List
    page_no: int = 0
    file_source: str = ""
    article_id: str
    metadata: Dict[str, Union[str, datetime]]


class VectorSearchResponse(BaseModel):
    document: str
    distance: float
    metadata: Dict[str, str]
