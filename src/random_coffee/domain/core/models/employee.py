from typing import Optional

from datetime import datetime

from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.infrastructure.relational_entity import BaseRelationalEntity
from . import Role

from .organisation import Organisation
from .person import Person


class Employee(BaseRelationalEntity):
    __tablename__ = 'employee'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    role: Mapped[Role] = mapped_column(default=Role.EMPLOYEE)
    person_id: Mapped[int] = mapped_column(ForeignKey("person.id"))
    organisation_id: Mapped[int] = mapped_column(ForeignKey("organisation.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    deleted_at: Mapped[Optional[datetime]] = mapped_column()

    organisation: Mapped[Organisation] = relationship(back_populates="employees")
    person: Mapped[Person] = relationship(lazy='selectin')

    __table_args__ = (
        Index(
            "employee_person_id_organisation_id_key",
            "person_id", 'organisation_id',
            postgresql_where=deleted_at.is_(None),
            unique=True,
        ),
    )
    __mapped_args__ = {
        "polymorphic_on": "role",
        "polymorphic_identity": Role.EMPLOYEE,
    }
