from pydantic import BaseModel
from typing import Optional


class Member(BaseModel):
    id: int
    nama: str
    email: str
    nomor_telepon: Optional[str] = None
    aktif: bool = True
