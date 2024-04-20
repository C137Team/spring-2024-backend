from datetime import datetime

from sqlalchemy import UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from random_coffee.domain.core.models import Employee
from random_coffee.infrastructure.relational_entity import BaseRelationalEntity


class WanderingEmployee(BaseRelationalEntity):
    __tablename__ = "wandering_employee"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    employee: Mapped[Employee] = relationship(lazy='selectin')
