from pydantic import BaseModel, model_serializer
from fastapi import FastAPI, HTTPException
from typing import List, Optional


class BookCreate(BaseModel):
    title: str
    author: str
    publish_year: int
    genres: List[str]

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publish_year: Optional[int] = None
    genres: Optional[list[str]] = None

    model_config = {
        "extra": "forbid"
    }

class BookRead(BaseModel):
    id: int
    title: str
    author: str
    publish_year: int
    genres: List[str]
    rating: int
    rarity: Optional[bool] = False
    recommendation: Optional[str] = ""

    class Config:
        from_attributes = True

    @model_serializer
    def serialize_model(self):
        data = self.__dict__.copy()
        # убираем пустые поля
        return {k: v for k, v in data.items() if v not in (None, False, "")}