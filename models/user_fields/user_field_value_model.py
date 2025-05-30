import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class UserFieldValue(SQLModel, table=True):

    __tablename__ = "user_field_value"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    field_definition_id: int = Field(foreign_key="user_field_definition.id", ondelete="CASCADE")
    value: str

    # Relationships (optional)
    user: "User" = Relationship() # type: ignore
    field_definition: "UserFieldDefinition" = Relationship() # type: ignore