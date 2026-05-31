from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    member_id: int = Field(
        ..., ge=1,
        description="ID anggota yang meminjam"
    )
    book_id: int = Field(
        ..., ge=1,
        description="ID buku yang dipinjam"
    )
