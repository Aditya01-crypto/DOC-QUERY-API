from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine,async_sessionmaker
import os
# from dotenv import load_dotenv #(using   docker no longer needed)  
from typing import AsyncGenerator
# load_dotenv()
 #no longer needed since docker initializes it automatically 
DATABASE_URL=os.getenv('DATABASE_URL')

engine=create_async_engine(DATABASE_URL,echo=True) # type: ignore

LocalAsycnSession=async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False)

async def get_db() ->AsyncGenerator[AsyncSession,None]:
    async with LocalAsycnSession() as session:
        try:
            yield session
            await session.commit()
        except:
            await session.rollback()
            raise

class Base(DeclarativeBase):
    pass