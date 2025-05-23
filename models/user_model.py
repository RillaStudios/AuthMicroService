from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship
import uuid

class User(SQLModel, table=True):

    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(default=None, nullable=False)
    is_active: bool = Field(default=True, nullable=False)
    last_active: datetime | None = Field(default=datetime.now(), nullable=True)
    created_at: datetime | None = Field(default=datetime.now(), nullable=False)
    last_updated_at: datetime | None = Field(default=None, nullable=False)

    custom_fields: List["UserFieldValue"] = Relationship(back_populates="user") # type: ignore

external_data = {
    "id": "123",
    "username": "izaakford",
}