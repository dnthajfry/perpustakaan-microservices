from fastapi import FastAPI, Query
from typing import Optional

from schema.loan_schema import LoanCreate
from services import loan_services

app = FastAPI(
    title="Loan Service",
    description=(
        "Microservice untuk mencatat peminjaman & pengembalian buku. "
        "Service ini berkomunikasi via HTTP dengan Book Service dan Member Service."
    ),
    version="1.0.0",
)


@app.get("/")
def root():
    return {"pesan": "Selamat datang di Loan Service"}


@app.post("/loans/")
def pinjam_buku(data: LoanCreate):
    return loan_services.create_loan(data)


@app.post("/loans/{loan_id}/kembalikan")
def kembalikan_buku(loan_id: int):
    return loan_services.return_loan(loan_id)


@app.get("/loans/")
def daftar_peminjaman(
    halaman: int = Query(1, ge=1, description="Nomor halaman"),
    jumlah: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    dikembalikan: Optional[bool] = Query(None, description="Filter status pengembalian"),
):
    return loan_services.get_all_loans(halaman, jumlah, dikembalikan)


@app.get("/loans/{loan_id}")
def detail_peminjaman(loan_id: int):
    return loan_services.get_loan_by_id(loan_id)


@app.get("/loans/anggota/{member_id}")
def peminjaman_per_anggota(member_id: int):
    return loan_services.get_loans_by_member(member_id)
