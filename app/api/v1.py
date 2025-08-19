from fastapi import APIRouter, HTTPException
from app.schemas.book import BookCreate, BookRead, BookUpdate
from app.services.book_service import create_book, list_book, get_book, update_book, delete_book
from datetime import datetime

router = APIRouter()

@router.get("/books", response_model=list[BookRead])
async def get_books():
    return await list_book()

@router.post("/book", response_model=BookRead)
async def add_book(book: BookCreate):
    validate_fields(book)
    return await create_book(book)

@router.get("/book/{book_id}", response_model=BookRead)
async def get_by_id(book_id: int):
    return await get_book(book_id)

@router.put("/book/{book_id}", response_model=BookRead)
async def new_data_book(book_id: int, new_data: BookUpdate):
    old_data_book = await get_book(book_id)
    if not old_data_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    if(new_data.publish_year):
        if (new_data.publish_year < old_data_book["publish_year"]):
            raise HTTPException(status_code=404, detail="publish_year нельзя менять на значение старше исходного")
    validate_fields(new_data)
    return await update_book(book_id, new_data, old_data_book)

@router.delete("/book/{book_id}")
async def remove_book(book_id: int):
    old_data_book = await get_book(book_id)
    if not old_data_book:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    elif(old_data_book["rating"] >= 3):
        raise HTTPException(status_code=404, detail="Нельзя удалить книгу с высоким рейтингом")
    return await delete_book(book_id)

def validate_fields(book: BookCreate | BookUpdate):
    # Проверка жанров
    if book.genres:
        if len(book.genres) > 3:
            raise HTTPException(
                status_code=400,
                detail="Жанров не должно быть больше 3"
            )
        elif len(book.genres) == 0:
            raise HTTPException(
                status_code=400,
                detail="Поле жанр не может быть пустым"
            )

    # Проверка publish_year
    if book.publish_year is not None:
        if book.publish_year < 1931 or book.publish_year >= datetime.now().year:
            raise HTTPException(
                status_code=400,
                detail="publish_year должен быть не раньше 1931 и не позже текущего года"
            )