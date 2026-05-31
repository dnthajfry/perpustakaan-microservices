from fastapi import FastAPI, Query
from typing import Optional

from schema.book_schema import BookCreate, BookUpdate, StokUpdate
from services import book_services

app = FastAPI(
    title="Book Service",
    description="Microservice untuk mengelola data buku di perpustakaan",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"pesan": "Selamat datang di Book Service"}


@app.post("/books/")
def tambah_buku(book: BookCreate):
    return book_services.create_book(book)


@app.get("/books/")
def daftar_buku(
    halaman: int = Query(1, ge=1, description="Nomor halaman"),
    jumlah: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    tersedia: Optional[bool] = Query(None, description="Filter berdasarkan ketersediaan stok"),
):
    return book_services.get_all_books(halaman, jumlah, tersedia)


@app.get("/books/cari/")
def cari_buku(
    q: str = Query(..., min_length=1, max_length=100, description="Kata kunci pencarian (judul/penulis)"),
):
    return book_services.search_books(q)


@app.get("/books/{book_id}")
def baca_buku(book_id: int):
    return book_services.get_book_by_id(book_id)


@app.put("/books/{book_id}")
def perbarui_buku(book_id: int, data: BookUpdate):
    return book_services.update_book(book_id, data)


@app.patch("/books/{book_id}/stok")
def ubah_stok_buku(book_id: int, data: StokUpdate):
    """Endpoint khusus untuk service lain (mis. loan-service) mengubah stok."""
    return book_services.ubah_stok(book_id, data.perubahan)


@app.delete("/books/{book_id}")
def hapus_buku(book_id: int):
    return book_services.delete_book(book_id)
