from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.database import SessionDep
from models import UserFieldDefinition

user_field_router = APIRouter(prefix="/user-field", tags=["user-field"])

@user_field_router.get("/")
async def get_user_fields(session: SessionDep):
    """
    Get all user fields.

    This endpoint retrieves all user-defined fields that can be used in user profiles.
    It returns a list of user fields with their definitions, such as name, type, and whether they are required.

    :param session: The database session dependency.

    :return: A list of user fields.

    @author: IFD
    @since 2025-05-28
    """

    statement = select(UserFieldDefinition)
    result = session.exec(statement).all()

    if not result:
        raise HTTPException(status_code=404, detail="No user fields found")

    return result

@user_field_router.get("/{field_id}")
async def get_user_field_by_id(field_id: int, session: SessionDep):
    """
    Get a user field by its ID.

    This endpoint retrieves a specific user-defined field by its ID. It returns the field's details, such as name, type, and whether it is required.

    :param session:
    :param field_id:
    :return:

    @author: IFD
    @since: 2025-05-28
    """
    if not isinstance(field_id, int) or field_id is None:
        raise HTTPException(status_code=400, detail="Invalid field ID")

    statement = select(UserFieldDefinition).where(UserFieldDefinition.id == field_id)
    result = session.exec(statement).first()

    if not result:
        raise HTTPException(status_code=404, detail="User field not found")

    return result

@user_field_router.post("/")
async def create_user_field(field: dict, session: SessionDep):
    """
    Create a new user field.

    This endpoint allows the creation of a new user-defined field. The field must have a name and a type.

    :param session:
    :param field:
    :return:

    @author: IFD
    @since: 2025-05-28
    """
    if not field.get("name") or not field.get("type"):
        raise HTTPException(status_code=400, detail="Field name and type are required")

    if not isinstance(field.get("name"), str) or not isinstance(field.get("field_type"), str)\
            or not isinstance(field.get("required"), bool) or not isinstance(field.get("description"), (str, type(None))):
        raise HTTPException(status_code=400, detail="Field attributes must be of correct types")

    new_field = UserFieldDefinition.create(**field)

    session.add(new_field)
    session.commit()
    session.refresh(new_field)

    return {"message": "User field created successfully", "field_id": new_field.id, "field": new_field}

@user_field_router.patch("/")
async def update_user_field(field_id: int, field: dict, session: SessionDep):
    """
    Update an existing user field.

    This endpoint allows updating an existing user-defined field. At least one of the field's attributes (name or type) must be provided for the update.

    :param session:
    :param field_id:
    :param field:
    :return:

    @author: IFD
    @since: 2025-05-28
    """
    if not isinstance(field_id, int) or field_id is None:
        raise HTTPException(status_code=400, detail="Invalid field ID")

    if not field.get("name") and not field.get("type"):
        raise HTTPException(status_code=400, detail="At least one field to update is required")

    statement = select(UserFieldDefinition).where(UserFieldDefinition.id == field_id)

    existing_field = session.exec(statement).first()

    if not existing_field:
        raise HTTPException(status_code=404, detail="User field not found")

    # Update the existing field with provided attributes
    if "name" in field:
        existing_field.name = field["name"]
    if "field_type" in field:
        existing_field.field_type = field["field_type"]
    if "required" in field:
        existing_field.required = field["required"]
    if "description" in field:
        existing_field.description = field.get("description")

    session.commit()
    session.refresh(existing_field)

    return {
        "message": "User field updated successfully",
        "field_id": existing_field.id,
        "field": existing_field
    }

@user_field_router.delete("/")
async def delete_user_field(field_id: int, session: SessionDep):
    """
    Delete a user field.

    This endpoint allows the deletion of a user-defined field by its ID. If the field does not exist, it returns an error.

    :param session:
    :param field_id:
    :return:

    @author: IFD
    @since: 2025-05-28
    """
    if not isinstance(field_id, int) or field_id is None:
        raise HTTPException(status_code=400, detail="Invalid field ID")

    statement = select(UserFieldDefinition).where(UserFieldDefinition.id == field_id)
    existing_field = SessionDep.exec(statement).first()

    if not existing_field:
        raise HTTPException(status_code=404, detail="User field not found")

    session.delete(existing_field)
    session.commit()

    return {"message": "User field deleted successfully", "field_id": field_id}
