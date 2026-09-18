from pydantic import BaseModel,ConfigDict
from datetime import datetime
# from pgvector.sqlalchemy import Vector

class DocumentResponse(BaseModel):
    id:int
    name:str
    content:str
    word_count:int
    uploaded_at: datetime

    model_config=ConfigDict(
        from_attributes=True
    )