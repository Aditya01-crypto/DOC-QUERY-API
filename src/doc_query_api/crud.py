from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , delete
from .models import Document

async def show_document(id:int,session:AsyncSession):
    query= (select(Document).where(Document.id==id))
    result=await session.execute(query)

    return result.scalar_one_or_none()

async def show_documents(session:AsyncSession,limit:int,skip:int):
    query= (select(Document).offset(skip).limit(limit))
    results= await session.execute(query)

    return results.scalars().all()

async def create_document(session:AsyncSession):
    pass

async def delete_document(session:AsyncSession):
    pass

async def embed_document(session:AsyncSession,id:int,embed:list[float]):
    pass

async def query_document(session:AsyncSession,query_embedding:list[float]):
    pass