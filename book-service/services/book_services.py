from typing import Optional
from fastapi import HTTPException

from model.book_model import Book
from schema.book_schema import BookCreate, BookUpdate

# In-memory database
database: list[Book] = []
counter_id: int = 0


def _seed():
    """Isi data awal supaya langsung bisa dicoba."""
    global counter_id
    if database:
        return
    contoh = [
        ("Laskar Pelangi", "Andrea Hirata", 2005, 3),
        ("Bumi Manusia", "Pramoedya Ananta Toer", 1980, 2),
        ("Negeri 5 Menara", "Ahmad Fuadi", 2009, 4),
    ]
    for judul, penulis, tahun, stok in contoh:
        counter_id += 1
        database.append(Book(
            id=counter_id,
            judul=judul,
            penulis=penulis,
            tahun_terbit=tahun,
            stok=stok,
        ))


_seed()


def create_book(book: BookCreate) -> dict:
    global counter_id
    counter_id += 1
    data = Book(
        id=counter_id,
        judul=book.judul,
        penulis=book.penulis,
        tahun_terbit=book.tahun_terbit,
        stok=book.stok,
    )
    database.append(data)
    return {"pesan": "Buku berhasil ditambahkan", "data": data}


def get_all_books(
    halaman: int = 1,
    jumlah: int = 10,
    tersedia: Optional[bool] = None,
) -> dict:
    hasil = database.copy()

    if tersedia is True:
        hasil = [b for b in hasil if b.stok > 0]
    elif tersedia is False:
        hasil = [b for b in hasil if b.stok == 0]

    start = (halaman - 1) * jumlah
    end = start + jumlah

    return {
        "halaman": halaman,
        "jumlah": jumlah,
        "total": len(hasil),
        "data": hasil[start:end],
    }


def search_books(q: str) -> dict:
    hasil = [
        b for b in database
        if q.lower() in b.judul.lower()
        or q.lower() in b.penulis.lower()
    ]
    return {"kata_kunci": q, "total": len(hasil), "data": hasil}


def get_book_by_id(book_id: int) -> Book:
    for book in database:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")


def update_book(book_id: int, data: BookUpdate) -> dict:
    for book in database:
        if book.id == book_id:
            if data.judul is not None:
                book.judul = data.judul
            if data.penulis is not None:
                book.penulis = data.penulis
            if data.tahun_terbit is not None:
                book.tahun_terbit = data.tahun_terbit
            if data.stok is not None:
                book.stok = data.stok
            return {"pesan": "Buku berhasil diperbarui", "data": book}
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")


def ubah_stok(book_id: int, perubahan: int) -> dict:
    for book in database:
        if book.id == book_id:
            stok_baru = book.stok + perubahan
            if stok_baru < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Stok buku tidak mencukupi",
                )
            book.stok = stok_baru
            return {"pesan": "Stok berhasil diperbarui", "data": book}
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")


def delete_book(book_id: int) -> dict:
    for i, book in enumerate(database):
        if book.id == book_id:
            data = database.pop(i)
            return {"pesan": "Buku berhasil dihapus", "data": data}
    raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
