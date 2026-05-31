from fastapi import FastAPI, Query
from typing import Optional

from schema.member_schema import MemberCreate, MemberUpdate
from services import member_services

app = FastAPI(
    title="Member Service",
    description="Microservice untuk mengelola data anggota perpustakaan",
    version="1.0.0",
)


@app.get("/")
def root():
    return {"pesan": "Selamat datang di Member Service"}


@app.post("/members/")
def tambah_anggota(member: MemberCreate):
    return member_services.create_member(member)


@app.get("/members/")
def daftar_anggota(
    halaman: int = Query(1, ge=1, description="Nomor halaman"),
    jumlah: int = Query(10, ge=1, le=100, description="Jumlah data per halaman"),
    aktif: Optional[bool] = Query(None, description="Filter berdasarkan status aktif"),
):
    return member_services.get_all_members(halaman, jumlah, aktif)


@app.get("/members/cari/")
def cari_anggota(
    q: str = Query(..., min_length=1, max_length=100, description="Kata kunci pencarian"),
):
    return member_services.search_members(q)


@app.get("/members/{member_id}")
def baca_anggota(member_id: int):
    return member_services.get_member_by_id(member_id)


@app.put("/members/{member_id}")
def perbarui_anggota(member_id: int, data: MemberUpdate):
    return member_services.update_member(member_id, data)


@app.delete("/members/{member_id}")
def hapus_anggota(member_id: int):
    return member_services.delete_member(member_id)
