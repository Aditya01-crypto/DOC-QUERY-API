from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select , delete
from doc_query_api.models import Document
from fastapi import UploadFile
from pathlib import Path
from doc_processor.scanx import Scanner

import asyncio

async def get_file_content(f_path:Path):
    text_data=None
    sc=Scanner(f_path.parent)
    if f_path.suffix=='.pdf':
        text_data=await sc.extract_pdf_text(f_path)
    elif f_path.suffix =='.docx':
        text_data=await sc.extract_docx_text(f_path)

    return text_data[:50] if type(text_data) is str and len(text_data)>0 else None
    
                       
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
    query= select(Document.id==)

async def embed_document(session:AsyncSession,id:int,embed:list[float]):
    pass

async def query_document(session:AsyncSession,query_embedding:list[float]):
    pass

if __name__ =="__main__":
    async def main():#testing some functions
        l=['src/doc_query_api/uploaded_files/a.pdf','src/doc_query_api/uploaded_files/c.pdf','src/doc_query_api/uploaded_files/p.docx','src/doc_query_api/uploaded_files/pc.odt']
        r=[]
        for p in l:
            p=Path(p)
            r.append(await get_file_content(p))

        return r

    print(asyncio.run(main()))

