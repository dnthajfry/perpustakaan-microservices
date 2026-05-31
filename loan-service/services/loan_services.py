from datetime import date
from typing import Optional
from fastapi import HTTPException
import httpx

from model.loan_model import Loan
from schema.loan_schema import LoanCreate

# URL service lain (bisa diubah lewat environment variable di produksi)
BOOK_SERVICE_URL = "http://127.0.0.1:8001"
MEMBER_SERVICE_URL = "http://127.0.0.1:8002"

# In-memory database
database: list[Loan] = []
counter_id: int = 0


def _ambil_member(member_id: int) -> dict:
    """Komunikasi ke member-service via HTTP untuk memastikan anggota valid."""
    try:
        r = httpx.get(f"{MEMBER_SERVICE_URL}/members/{member_id}", timeout=5.0)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Member Service tidak dapat dihubungi",
        )
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()


def _ambil_buku(book_id: int) -> dict:
    """Komunikasi ke book-service via HTTP untuk memastikan buku valid."""
    try:
        r = httpx.get(f"{BOOK_SERVICE_URL}/books/{book_id}", timeout=5.0)
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Book Service tidak dapat dihubungi",
        )
    if r.status_code == 404:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()


def _ubah_stok_buku(book_id: int, perubahan: int) -> None:
    """Minta book-service mengubah stok (negatif=pinjam, positif=kembali)."""
    try:
        r = httpx.patch(
            f"{BOOK_SERVICE_URL}/books/{book_id}/stok",
            json={"perubahan": perubahan},
            timeout=5.0,
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Book Service tidak dapat dihubungi",
        )
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.json())


def create_loan(data: LoanCreate) -> dict:
    global counter_id

    # Validasi anggota lewat member-service
    member = _ambil_member(data.member_id)
    if not member.get("aktif", True):
        raise HTTPException(
            status_code=400,
            detail="Anggota tidak aktif, tidak bisa meminjam buku",
        )

    # Validasi buku lewat book-service
    book = _ambil_buku(data.book_id)
    if book.get("stok", 0) <= 0:
        raise HTTPException(
            status_code=400,
            detail="Stok buku habis",
        )

    # Kurangi stok buku
    _ubah_stok_buku(data.book_id, -1)

    counter_id += 1
    loan = Loan(
        id=counter_id,
        member_id=data.member_id,
        book_id=data.book_id,
        tanggal_pinjam=date.today(),
        tanggal_kembali=None,
        dikembalikan=False,
    )
    database.append(loan)

    return {
        "pesan": "Peminjaman berhasil dicatat",
        "data": loan,
        "anggota": {"id": member["id"], "nama": member["nama"]},
        "buku": {"id": book["id"], "judul": book["judul"]},
    }


def return_loan(loan_id: int) -> dict:
    for loan in database:
        if loan.id == loan_id:
            if loan.dikembalikan:
                raise HTTPException(
                    status_code=400,
                    detail="Buku ini sudah dikembalikan sebelumnya",
                )
            # Tambah kembali stok buku
            _ubah_stok_buku(loan.book_id, 1)
            loan.dikembalikan = True
            loan.tanggal_kembali = date.today()
            return {"pesan": "Pengembalian berhasil dicatat", "data": loan}
    raise HTTPException(status_code=404, detail="Data peminjaman tidak ditemukan")


def get_all_loans(
    halaman: int = 1,
    jumlah: int = 10,
    dikembalikan: Optional[bool] = None,
) -> dict:
    hasil = database.copy()

    if dikembalikan is not None:
        hasil = [l for l in hasil if l.dikembalikan == dikembalikan]

    start = (halaman - 1) * jumlah
    end = start + jumlah

    return {
        "halaman": halaman,
        "jumlah": jumlah,
        "total": len(hasil),
        "data": hasil[start:end],
    }


def get_loan_by_id(loan_id: int) -> dict:
    for loan in database:
        if loan.id == loan_id:
            # Enrich dengan data dari service lain
            member = _ambil_member(loan.member_id)
            book = _ambil_buku(loan.book_id)
            return {
                "data": loan,
                "anggota": {"id": member["id"], "nama": member["nama"]},
                "buku": {"id": book["id"], "judul": book["judul"]},
            }
    raise HTTPException(status_code=404, detail="Data peminjaman tidak ditemukan")


def get_loans_by_member(member_id: int) -> dict:
    hasil = [l for l in database if l.member_id == member_id]
    return {"member_id": member_id, "total": len(hasil), "data": hasil}
