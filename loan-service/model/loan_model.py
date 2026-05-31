from pydantic import BaseModel
from datetime import date
from typing import Optional


class Loan(BaseModel):
    id: int
    member_id: int
    book_id: int
    tanggal_pinjam: date
    tanggal_kembali: Optional[date] = None
    dikembalikan: bool = False
