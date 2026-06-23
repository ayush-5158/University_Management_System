from fastapi import FastAPI,Depends,HTTPException
from database import get_db,engine
from sqlalchemy.orm import Session
import model
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Bookstore(BaseModel):
    id : int
    title : str
    author : str
    publish_date : str


#creation of books
@app.post("/create_books")
def create_books(book:Bookstore,db:Session = Depends(get_db)):
    new_book = model.Book(id = book.id, title=book.title,author = book.author,publish_date = book.publish_date)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


#get all books
@app.get("/books")
def get_books(db:Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books

#update book

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str]=None
    publish_date : Optional[str] = None

@app.patch("/update_book/{id}")
def update_book(book_update:BookUpdate,id:int,db:Session=Depends(get_db)):
    book = db.query(model.Book).filter(model.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404,detail="Book not Found.")
    
    update_data = book_update.model_dump(exclude_unset=True)

    for key,value in update_data.items():
        setattr(book,key,value)

    db.commit()
    db.refresh(book)

    return book

@app.delete("/delete/{book_id}")
def delete_books(book_id:int,db:Session=Depends(get_db)):

    book = db.query(model.Book).filter(
        model.Book.id == book_id
    ).first()

    if not book:
        raise HTTPException(status_code=404,detail="Book not Found.")
    
    db.delete(book)
    db.commit()

    return{
        "message":f"The book {book.title} is succesfully deleted."
    }
    

    