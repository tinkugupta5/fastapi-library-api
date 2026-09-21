from fastapi import FastAPI , Body
from pydantic import BaseModel , Field
from typing import Optional

app = FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:float
    
    def __init__(self, id:int, title:str, author:str, description:str, rating:float):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title:str = Field(min_length=3)
    author:str = Field(min_length=1)
    description:str = Field(min_length=1, max_length=100)
    rating:float = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Author name",
                "description": "A new description of a book",
                "rating": 5,
            }
        }
    }
        
    
BOOKS = [
    Book(1, "Title One", "Author One", "Description One", 4.5),
    Book(2, "Title Two", "Author Two", "Description Two", 4.0),
    Book(3, "Title Three", "Author Three", "Description Three", 3.5),
    Book(4, "Title Four", "Author Four", "Description Four", 5.0),
    Book(5, "Title Five", "Author Five", "Description Five", 4.8),
    Book(6, "Title Six", "Author Six", "Description Six", 4.2),
]

@app.get("/books")
async def read_all_books():
    return BOOKS

@app.put("/books/update_book")
async def update_book(book: BookRequest):
    if book.id is None:
        return {"error": "Book ID is required for update"}

    updated_book = Book(**book.model_dump())
    for index, existing_book in enumerate(BOOKS):
        if existing_book.id == book.id:
            BOOKS[index] = updated_book
            return updated_book
    return {"error": "Book not found"}

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index in range(len(BOOKS)):
        if BOOKS[index].id == book_id:
            BOOKS.pop(index)
            return {"message": "Book deleted successfully"}

    return {"error": "Book not found"}

@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"error": "Book not found"}


@app.get("/books/")
async def read_book_by_rating(rating:float):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book.rating:
            books_to_return.append(book)
    return books_to_return
    
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(id=book_request.id or 0, **book_request.model_dump(exclude={"id"}))
    BOOKS.append(find_book_id(new_book))
    return new_book

def find_book_id(book: Book) -> Book:
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book
