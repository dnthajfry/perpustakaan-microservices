from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class MemberCreate(BaseModel):
    nama: str = Field(
        ..., min_length=1, max_length=100,
        description="Nama lengkap anggota"
    )
    email: EmailStr = Field(
        ...,
        description="Email anggota"
    )
    nomor_telepon: Optional[str] = Field(
        None, max_length=20,
        description="Nomor telepon anggota (opsional)"
    )
    aktif: bool = Field(
        True,
        description="Status keaktifan anggota"
    )


class MemberUpdate(BaseModel):
    nama: Optional[str] = Field(
        None, min_length=1, max_length=100,
        description="Nama lengkap anggota"
    )
    email: Optional[EmailStr] = Field(
        None,
        description="Email anggota"
    )
    nomor_telepon: Optional[str] = Field(
        None, max_length=20,
        description="Nomor telepon anggota"
    )
    aktif: Optional[bool] = Field(
        None,
        description="Status keaktifan anggota"
    )
