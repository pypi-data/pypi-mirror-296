import pytest  # noqa: F401
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .main import (
    Base,
    Parent,
    PydanticParent,
    orm_create_input_data,
    orm_create_output_data,
    orm_update_input_data,
    orm_update_output_data,
)

engine = create_engine("sqlite://", echo=False)
Base.metadata.create_all(bind=engine)
DatabaseSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db: Session = DatabaseSession()


def test_orm_create() -> None:
    schema_in = PydanticParent.model_validate(orm_create_input_data)
    db_model = schema_in.orm_create()
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    schema_out = PydanticParent.model_validate(db_model)
    assert schema_out.model_dump(by_alias=True) == orm_create_output_data


def test_orm_update() -> None:  # only works after test_orm_create()
    schema_in = PydanticParent.model_validate(orm_update_input_data)
    db_model = db.query(Parent).get(schema_in.id)
    schema_in.orm_update(db, db_model)
    db.commit()
    db.refresh(db_model)
    schema_out = PydanticParent.model_validate(db_model)
    assert schema_out.model_dump(by_alias=True) == orm_update_output_data
