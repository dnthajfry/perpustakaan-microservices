from pydantic import BaseModel, Field
from typing import Optional


class BookCreate(BaseModel):
    judul: str = Field(
        ..., min_length=1, max_length=200,
        description="Judul buku"
    )
    penulis: str = Field(
        ..., min_length=1, max_length=100,
        description="Nama penulis buku"
    )
    tahun_terbit: Optional[int] = Field(
        None, ge=1000, le=9999,
        description="Tahun terbit buku"
    )
    stok: int = Field(
        1, ge=0,
        description="Jumlah stok buku"
    )


class BookUpdate(BaseModel):
    judul: Optional[str] = Field(
        None, min_length=1, max_length=200,
        description="Judul buku"
    )
    penulis: Optional[str] = Field(
        None, min_length=1, max_length=100,
        description="Nama penulis buku"
    )
    tahun_terbit: Optional[int] = Field(
        None, ge=1000, le=9999,
        description="Tahun terbit buku"
    )
    stok: Optional[int] = Field(
        None, ge=0,
        description="Jumlah stok buku"
    )


class StokUpdate(BaseModel):
    perubahan: int = Field(
        ...,
        description="Perubahan stok (negatif untuk pinjam, positif untuk kembali)"
    )
