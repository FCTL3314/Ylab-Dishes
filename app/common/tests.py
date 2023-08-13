from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select
from sqlmodel import SQLModel, select


def is_response_match_object_fields(
    response_data: dict, obj: dict | object, fields: tuple | list
) -> bool:
    """
    Checks whether the fields of the obj are equal to the
    fields of the response_data parameter.
    """
    for field in fields:
        response_field = response_data[field]
        obj_field = str(obj[field] if type(obj) is dict else getattr(obj, field))
        if response_field != obj_field:
            return False
    return True


async def get_model_objects_count(model: type[SQLModel], session: AsyncSession) -> int:
    """Returns the number of objects for the passed model."""
    result = await session.execute(select(model))
    return len(result.all())


async def delete_first_object(query: Select, session: AsyncSession) -> None:
    """Removes the first object from the received query."""
    objs = await session.execute(query)
    obj = objs.first()[0]  # type: ignore
    await session.delete(obj)
    await session.commit()
