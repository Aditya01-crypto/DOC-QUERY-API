from .database import Base
from sqlalchemy.orm import Mapped , mapped_column
from pgvector.sqlalchemy import Vector
from sqlalchemy import String,Text,Integer,DateTime,Index
from datetime import datetime

class Document(Base):

    __tablename__='documents'
    id:Mapped[int]=mapped_column(Integer,primary_key=True,autoincrement=True)
    name:Mapped[str]=mapped_column(String,nullable=False)
    content:Mapped[str]=mapped_column(Text,nullable=False)
    word_count:Mapped[int]=mapped_column(Integer,nullable=False)
    uploaded_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.now)
    embedding:Mapped[list[float]]=mapped_column(Vector(1536),nullable=True)

    __table_args__=(
        Index(
            "ix_doc_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgres_with={'m':16,'ef_construction':64},
            postgres_ops={"embedding":"vector_cosine_ops"},
        )
    )

