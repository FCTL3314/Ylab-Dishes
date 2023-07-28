from mixer.backend.sqlalchemy import mixer
from sqlmodel import select


def is_response_match_object_fields(response_data, obj, fields):
    for field in fields:
        response_field = response_data[field]
        obj_field = str(obj[field] if type(obj) is dict else getattr(obj, field))
        if response_field != obj_field:
            return False
    return True


def get_model_objects_count(model, session):
    return len(session.exec(select(model)).all())


def create_test_object(model_path, session, **kwargs):
    obj = mixer.blend(model_path, **kwargs)
    session.add(obj)
    session.commit()
    yield obj
    session.delete(obj)
    session.commit()
