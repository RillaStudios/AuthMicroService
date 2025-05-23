from typing import Optional
from sqlmodel import SQLModel, Field

class UserFieldDefinition(SQLModel, table=True):

    __tablename__ = "user_field_definition"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    field_type: str = Field(default="string")
    required: bool = Field(default=False)
    description: Optional[str] = Field(default=None)