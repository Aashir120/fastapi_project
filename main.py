import json
from fastapi import FastAPI,HTTPException,Depends,status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Annotated
import models 
from database import engine,sessionLocal
from sqlalchemy.orm import Session
from service import getBookContent, getBookMetaData, getGroqResponse

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Allow all origins (change to specific domain in production)
origins = [
    "http://localhost:5173",  # React local dev
    "https://gutenberg-app.vercel.app",  # Your deployed frontend
    "*",  # Allow all (use with caution)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

@app.get("/books", status_code=status.HTTP_200_OK)
async def getContent(db: db_dependency):
    db_post =  db.query(models.Book).all()
    return {"response": jsonable_encoder(db_post)}


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def getContent(book_id:int,db: db_dependency):
    content = await getBookContent(book_id)
    meta_data = await getBookMetaData(book_id)
    db_post =  db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_post is None:
        db_book = models.Book(book_id=book_id,title="unknown",author="unknown",content=json.dumps(content),meta_data=json.dumps(meta_data))
        db.add(db_book)
        db.commit()
        db.refresh(db_book)  # Refresh to return updated instance
        return {"response": jsonable_encoder(db_book)}
    return {"response": jsonable_encoder(db_post)}

@app.get("/analyze/{book_id}", status_code=status.HTTP_200_OK)
async def getContent(book_id:int,db: db_dependency):
    db_book =  db.query(models.Book).filter(models.Book.book_id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    llm_response = getGroqResponse(db_book.content)
    return {"response": jsonable_encoder(llm_response)}