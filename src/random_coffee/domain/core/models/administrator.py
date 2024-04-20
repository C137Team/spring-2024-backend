from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from random_coffee.domain.core.models import Role
from random_coffee.domain.core.models.employee import Employee


class Administrator(Employee):
    __tablename__ = 'administrator'

    administrator_created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    __mapped_args__ = {
        "polymorphic_identity": Role.ADMINISTRATOR,
    }
