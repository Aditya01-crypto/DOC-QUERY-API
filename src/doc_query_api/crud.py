from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , delete
from doc_query_api.models import Document
from fastapi import UploadFile
from pathlib import Path
import asyncio

    
                       
async def show_document(id:int,session:AsyncSession):
    query= (select(Document).where(Document.id==id))
    result=await session.execute(query)

    return result.scalar_one_or_none()

async def show_documents(session:AsyncSession,limit:int,skip:int):
    query= (select(Document).offset(skip).limit(limit))
    results= await session.execute(query)

    return results.scalars().all()

async def create_document(session:AsyncSession,filename:str,content:str,word_count:int):
    doc= Document(name=filename,content=content,word_count=word_count)
    session.add(doc)
    await session.flush()
    return doc
    

async def delete_document(session:AsyncSession,doc_id:int):
    query= delete(Document).where(Document.id==doc_id).returning(Document)
    result=await session.execute(query)
    doc=result.scalar_one_or_none()
    return doc

async def embed_document(session:AsyncSession,id:int,embed:list[float]):
    select_query=(select(Document).where(Document.id==id))
    result=await session.execute(select_query)
    doc=result.scalar_one_or_none()
    if doc:
        doc.embedding=embed
    await session.flush()

    return doc
    

async def query_document(session:AsyncSession,query_embedding:list[float],limit:int):
    query=select(Document,Document.embedding.cosine_distance(query_embedding).label("distance")
    ).where(Document.embedding.isnot(None)).order_by(Document.embedding.cosine_distance(query_embedding)).limit(limit)

    results=await session.execute(query)

    return results.scalars().all()



