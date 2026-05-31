from pydantic import BaseModel
from typing import Optional


class Book(BaseModel):
    id: int
    judul: str
    penulis: str
    tahun_terbit: Optional[int] = None
    stok: int = 1
