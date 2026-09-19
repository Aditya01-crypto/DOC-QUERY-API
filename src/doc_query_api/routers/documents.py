from fastapi import APIRouter,HTTPException,Depends,UploadFile ,File
from doc_query_api.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
import doc_query_api.crud as crud
from pathlib import Path
import shutil
from doc_query_api.schemas import DocumentResponse
from math import ceil
from doc_query_api.embeddings import generate_embedding

router=APIRouter(tags=['documents'],prefix='/documents')

UPLOAD_DIR=Path("uploaded_files")
UPLOAD_DIR.mkdir(exist_ok=True,parents=True)

#helper function check File object
async def valid_file(file:UploadFile):
    valid_types={".pdf",".docx"}
    
    filename_var=file.filename
    if not filename_var:
        raise HTTPException(400,"Got None")
        
    filename=Path(filename_var)#using Path object to check valid file types
    if filename.suffix not in valid_types:
        raise HTTPException(400,"Uploaded unsupported filetype.\n(Supported files: Pdf and Word file)")

    content=await file.read()#checking file size , threshold upto 10mb
    size_mb=ceil(len(content)/1048576)
    if size_mb >10:
        raise HTTPException(400,"File size should be less than 10mb")
    await file.seek(0)
    return file


@router.get('/',response_model=list[DocumentResponse])
async def get_documents(limit:int=10,skip:int=0,db:AsyncSession=Depends(get_db)):
    docs=await crud.show_documents(session=db,limit=limit,skip=skip)
    if not docs:
        raise HTTPException(404,'No Documents Found')

    return docs

@router.post('/search',response_model=list[DocumentResponse])
async def search_document(query:str,limit:int=5,db:AsyncSession=Depends(get_db)):
    query_embedding= generate_embedding(query) #get embedding for query's content
    result=await crud.query_document(db,query_embedding=query_embedding,limit=limit)
    return result

@router.post('/upload',response_model=DocumentResponse)
async def add_document(db:AsyncSession=Depends(get_db),file:UploadFile=File(...)):
    checked_file=await valid_file(file)
    filename=str(checked_file.filename) #type: ignore
        
    file_path=UPLOAD_DIR/filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(checked_file.file,buffer)

    content=await crud.get_file_content(f_path=file_path) 
    if not content:
        raise HTTPException(400,'No content found!')

    word_count=len(content.split())
    doc=await crud.create_document(session=db,filename=filename,content=content,word_count=word_count)

    if not doc:
        raise HTTPException(500,"Some Error in Server")
    return doc

@router.get('/{id}',response_model=DocumentResponse)
async def get_document(id:int,db:AsyncSession=Depends(get_db)):
    docs=await crud.show_document(session=db,id=id)
    if not docs:
        raise HTTPException(404,'No Documents Found')

    return docs


@router.delete('/{id}',response_model=DocumentResponse)
async def remove_doc(id:int,db:AsyncSession=Depends(get_db)):
    doc=await crud.delete_document(session=db,doc_id=id)
    if not doc:
        raise HTTPException(404,"Document Not Found")
    return doc

@router.post('/{id}/embed')
async def add_embedding(id:int,db:AsyncSession=Depends(get_db)):
    doc=await crud.show_document(id=id,session=db)
    if not doc:
        raise HTTPException(404,"Document Not Found")
    # get embedding from document's content
    embed=generate_embedding(doc.content)
    result=await crud.embed_document(db,id=id,embed=embed)
    if not result:
        raise HTTPException(500,"Internal Server Error")
    return {"Status":f"Document {id} successfully embedded"}


