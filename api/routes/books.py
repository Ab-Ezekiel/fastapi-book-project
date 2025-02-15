from typing import Dict
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    if book.id in db.books:
        raise HTTPException(status_code=400, detail="Book with this ID already exists")
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )

@router.get("/", response_model=Dict[int, Book], status_code=status.HTTP_200_OK)
async def get_books() -> Dict[int, Book]:
    return db.get_books()

@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    book = db.books.get(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book) -> Book:
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = db.update_book(book_id, book)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_book.model_dump(),
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    if book_id not in db.books:
        raise HTTPException(status_code=404, detail="Book not found")
    
    del db.books[book_id]  # Properly delete the book from memory
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

