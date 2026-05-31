from typing import Optional
from fastapi import HTTPException

from model.member_model import Member
from schema.member_schema import MemberCreate, MemberUpdate

# In-memory database
database: list[Member] = []
counter_id: int = 0


def _seed():
    """Isi data awal supaya langsung bisa dicoba."""
    global counter_id
    if database:
        return
    contoh = [
        ("Budi Santoso", "budi@example.com", "081234567890"),
        ("Siti Aminah", "siti@example.com", "081298765432"),
    ]
    for nama, email, telp in contoh:
        counter_id += 1
        database.append(Member(
            id=counter_id,
            nama=nama,
            email=email,
            nomor_telepon=telp,
            aktif=True,
        ))


_seed()


def create_member(member: MemberCreate) -> dict:
    global counter_id
    # email harus unik
    for m in database:
        if m.email.lower() == member.email.lower():
            raise HTTPException(
                status_code=400,
                detail="Email sudah terdaftar",
            )
    counter_id += 1
    data = Member(
        id=counter_id,
        nama=member.nama,
        email=member.email,
        nomor_telepon=member.nomor_telepon,
        aktif=member.aktif,
    )
    database.append(data)
    return {"pesan": "Anggota berhasil ditambahkan", "data": data}


def get_all_members(
    halaman: int = 1,
    jumlah: int = 10,
    aktif: Optional[bool] = None,
) -> dict:
    hasil = database.copy()

    if aktif is not None:
        hasil = [m for m in hasil if m.aktif == aktif]

    start = (halaman - 1) * jumlah
    end = start + jumlah

    return {
        "halaman": halaman,
        "jumlah": jumlah,
        "total": len(hasil),
        "data": hasil[start:end],
    }


def search_members(q: str) -> dict:
    hasil = [
        m for m in database
        if q.lower() in m.nama.lower()
        or q.lower() in m.email.lower()
    ]
    return {"kata_kunci": q, "total": len(hasil), "data": hasil}


def get_member_by_id(member_id: int) -> Member:
    for member in database:
        if member.id == member_id:
            return member
    raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")


def update_member(member_id: int, data: MemberUpdate) -> dict:
    for member in database:
        if member.id == member_id:
            if data.nama is not None:
                member.nama = data.nama
            if data.email is not None:
                member.email = data.email
            if data.nomor_telepon is not None:
                member.nomor_telepon = data.nomor_telepon
            if data.aktif is not None:
                member.aktif = data.aktif
            return {"pesan": "Anggota berhasil diperbarui", "data": member}
    raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")


def delete_member(member_id: int) -> dict:
    for i, member in enumerate(database):
        if member.id == member_id:
            data = database.pop(i)
            return {"pesan": "Anggota berhasil dihapus", "data": data}
    raise HTTPException(status_code=404, detail="Anggota tidak ditemukan")
