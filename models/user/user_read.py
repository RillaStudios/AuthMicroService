from sqlmodel import SQLModel
from uuid import UUID

class UserRead(SQLModel):
    id: UUID
    email: str

    class Config:
        from_attributes = True