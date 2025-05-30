from datetime import datetime
from typing import List
from sqlmodel import SQLModel, Field, Relationship
import uuid

class User(SQLModel, table=True):

    __tablename__ = "user"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    email: str = Field(index=True, unique=True)
    password: str = Field(default=None, nullable=False)
    is_active: bool = Field(default=True)
    last_active: datetime | None = Field(default=datetime.now())
    created_at: datetime | None = Field(default=datetime.now())
    last_updated_at: datetime | None = Field(default=None, nullable=True)

    custom_fields: List["UserFieldValue"] = Relationship(back_populates="user") # type: ignore