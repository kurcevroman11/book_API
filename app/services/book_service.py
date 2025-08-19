from typing import Any
from app.models.book import books
from app.schemas.book import BookCreate, BookUpdate
from app.core.database import database
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select, desc, update
import json

async def create_book(book: BookCreate):
    rating = CalculationRatin(book.publish_year, book.genres)
    query = books.insert().values(
        title=book.title,
        author=book.author,
        publish_year=book.publish_year,
        genres=book.genres,
        rating=rating,
    )
    last_record_id = await database.execute(query)
    return  {**book.model_dump(), "id": last_record_id, "rating": rating}

async def list_book():
    query = (
        select(
            books.c.id,
            books.c.title,
            books.c.author,
            books.c.rating,
            books.c.publish_year,
            books.c.genres,
        )
        .order_by(desc(books.c.rating))
        .limit(10)
    )
    rows = await database.fetch_all(query)

    result = []
    for row in rows:
        book = {
            "id": row.id,
            "title": row.title,
            "author": row.author,
            "publish_year": row.publish_year,
            "genres": json.loads(row.genres) if isinstance(row.genres, str) else row.genres,
            "rating": row.rating,
        }
        if row.publish_year < 1950:
            book["rarity"] = True
        result.append(book)
    return result

async def get_book(id: int):
    query = books.select().where(books.c.id == id)
    row = await database.fetch_one(query)
    if not row:
        raise HTTPException(
            status_code=404,
            detail="Книга не найдена"
        )
    book = {
        "id": row.id,
        "title": row.title,
        "author": row.author,
        "publish_year": row.publish_year,
        "genres": json.loads(row.genres) if isinstance(row.genres, str) else row.genres,
        "rating": row.rating,
    }
    if row.publish_year < 1950:
        book["rarity"] = True

    weekday_number = datetime.now().weekday()
    match weekday_number:
        case 1 | 2:
            book["recommendation"] = "Рекомендуем по вторникам и средам"

    return book

async def update_book(id: int, book: BookUpdate, old_data_book: dict[str, Any]):
    updated_data = book.model_dump(exclude_unset=True)

    if ((book.genres is not None) and (book.publish_year is not None)):
        rating = CalculationRatin(updated_data.publish_year, updated_data.genres)
        updated_data["rating"] = rating
    else:
        rating = old_data_book["rating"]
    if(book.publish_year is not None):
        rating = CalculationRatin(book.publish_year, old_data_book["genres"])
        updated_data["rating"] = rating
    if(book.genres is not None):
        rating = CalculationRatin(old_data_book["publish_year"], book.genres)
        updated_data["rating"] = rating

    query = books.update().where(books.c.id == id).values(**updated_data)
    await database.execute(query)

    query = books.select().where(books.c.id == id)
    row = await database.fetch_one(query)
    book = {
        "id": row.id,
        "title": row.title,
        "author": row.author,
        "publish_year": row.publish_year,
        "genres": json.loads(row.genres) if isinstance(row.genres, str) else row.genres,
        "rating": rating,
    }

    if row.publish_year < 1950:
        book["rarity"] = True

    weekday_number = datetime.now().weekday()
    match weekday_number:
        case 1 | 2:
            book["recommendation"] = "Рекомендуем по вторникам и средам"

    return book

async def delete_book(id: int):
    query = books.delete().where(books.c.id == id)
    await database.execute(query)
    return {f"Book with id {id} succesfully deleted"}

def CalculationRatin(publish_year: int, genres: list[str]):
    rating = int((datetime.now().year - publish_year) / 20 + len(genres))
    if (rating < 2):
        raise HTTPException(
            status_code=400,
            detail="Низкий рейтинг: не интересная книга"
        )
    if(rating > 5):
        rating -= 1
    return rating


