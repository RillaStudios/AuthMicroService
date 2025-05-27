from typing import Any
from fastapi import APIRouter, HTTPException
from sqlmodel import select
from app.database import SessionDep
from app.utils.password import hash_password
from models import User, UserFieldDefinition, UserFieldValue
from models.user_create import UserCreate

user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/")
async def get_user():
    return {"message": "Get all users"}

@user_router.get("/id/{uid}")
async def get_user_by_id(uid, session: SessionDep):

    if not isinstance(uid, int) or uid is None:
        return HTTPException(status_code=400, detail="Invalid user ID")

    statement = select(User).where(User.id == uid)
    user = session.exec(statement).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user

@user_router.get('/email/{email}')
async def get_user_by_username(email, session: SessionDep):

    if not isinstance(email, str) or email is None:
        return HTTPException(status_code=400, detail="Invalid username")

    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user:
        return HTTPException(status_code=404, detail="User not found")

    return user


@user_router.post('/register')
async def register_user(user: UserCreate, session: SessionDep):
    # Step 1: Validate email & password
    if not user.email or not user.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Step 2: Validate required custom fields
    custom_fields: dict[str, Any] = user.custom_fields or {}

    field_defs = session.exec(select(UserFieldDefinition)).all()

    required_fields = [fd for fd in field_defs if fd.required]

    missing_fields = [fd.name for fd in required_fields if custom_fields.get(fd.name) is None]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required custom fields: {', '.join(missing_fields)}"
        )

    # Step 3: Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Step 4: Create the user
    new_user = User(email=user.email, password=hashed_password)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Step 5: Store custom field values
    for field_name, value in custom_fields.items():
        field_def = next((fd for fd in field_defs if fd.name == field_name), None)
        if field_def:
            session.add(UserFieldValue(user_id=new_user.id, field_id=field_def.id, value=value))

    session.commit()

    return {"message": "User registered successfully", "user": new_user}