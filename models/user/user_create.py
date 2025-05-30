from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str
    confirm_password: str
    custom_fields: dict[str, str] = {}

    class Config:
        from_attributes = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.custom_fields:
            self.custom_fields = {}